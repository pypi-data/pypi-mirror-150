/*!
 * Copyright 2014-2022 by XGBoost Contributors
 * \file updater_basemaker-inl.h
 * \brief implement a common tree constructor
 * \author Tianqi Chen
 */
#ifndef XGBOOST_TREE_UPDATER_BASEMAKER_INL_H_
#define XGBOOST_TREE_UPDATER_BASEMAKER_INL_H_

#include <rabit/rabit.h>


#include <vector>
#include <algorithm>
#include <string>
#include <limits>
#include <utility>

#include "xgboost/base.h"
#include "xgboost/json.h"
#include "xgboost/tree_updater.h"
#include "param.h"
#include "constraints.h"

#include "../common/io.h"
#include "../common/random.h"
#include "../common/quantile.h"
#include "../common/threading_utils.h"

namespace xgboost {
namespace tree {
/*!
 * \brief base tree maker class that defines common operation
 *  needed in tree making
 */
class BaseMaker: public TreeUpdater {
 public:
  void Configure(const Args& args) override {
    param_.UpdateAllowUnknown(args);
  }

  void LoadConfig(Json const& in) override {
    auto const& config = get<Object const>(in);
    FromJson(config.at("train_param"), &this->param_);
  }
  void SaveConfig(Json* p_out) const override {
    auto& out = *p_out;
    out["train_param"] = ToJson(param_);
  }

 protected:
  // helper to collect and query feature meta information
  struct FMetaHelper {
   public:
    /*! \brief find type of each feature, use column format */
    inline void InitByCol(DMatrix* p_fmat,
                          const RegTree& tree) {
      fminmax_.resize(tree.param.num_feature * 2);
      std::fill(fminmax_.begin(), fminmax_.end(),
                -std::numeric_limits<bst_float>::max());
      // start accumulating statistics
      for (const auto &batch : p_fmat->GetBatches<SortedCSCPage>()) {
        auto page = batch.GetView();
        for (bst_uint fid = 0; fid < batch.Size(); ++fid) {
          auto c = page[fid];
          if (c.size() != 0) {
            CHECK_LT(fid * 2, fminmax_.size());
            fminmax_[fid * 2 + 0] =
                std::max(-c[0].fvalue, fminmax_[fid * 2 + 0]);
            fminmax_[fid * 2 + 1] =
                std::max(c[c.size() - 1].fvalue, fminmax_[fid * 2 + 1]);
          }
        }
      }
    }
    /*! \brief synchronize the information */
    inline void SyncInfo() {
      rabit::Allreduce<rabit::op::Max>(dmlc::BeginPtr(fminmax_), fminmax_.size());
    }
    // get feature type, 0:empty 1:binary 2:real
    inline int Type(bst_uint fid) const {
      CHECK_LT(fid * 2 + 1, fminmax_.size())
          << "FeatHelper fid exceed query bound ";
      bst_float a = fminmax_[fid * 2];
      bst_float b = fminmax_[fid * 2 + 1];
      if (a == -std::numeric_limits<bst_float>::max()) return 0;
      if (-a == b) {
        return 1;
      } else {
        return 2;
      }
    }
    bst_float MaxValue(bst_uint fid) const {
      return fminmax_[fid *2 + 1];
    }

    void SampleCol(float p, std::vector<bst_feature_t> *p_findex) const {
      std::vector<bst_feature_t> &findex = *p_findex;
      findex.clear();
      for (size_t i = 0; i < fminmax_.size(); i += 2) {
        const auto fid = static_cast<bst_uint>(i / 2);
        if (this->Type(fid) != 0) findex.push_back(fid);
      }
      auto n = static_cast<unsigned>(p * findex.size());
      std::shuffle(findex.begin(), findex.end(), common::GlobalRandom());
      findex.resize(n);
      // sync the findex if it is subsample
      std::string s_cache;
      common::MemoryBufferStream fc(&s_cache);
      dmlc::Stream& fs = fc;
      if (rabit::GetRank() == 0) {
        fs.Write(findex);
      }
      rabit::Broadcast(&s_cache, 0);
      fs.Read(&findex);
    }

   private:
    std::vector<bst_float> fminmax_;
  };
  // ------static helper functions ------
  // helper function to get to next level of the tree
  /*! \brief this is  helper function for row based data*/
  inline static int NextLevel(const SparsePage::Inst &inst, const RegTree &tree, int nid) {
    const RegTree::Node &n = tree[nid];
    bst_uint findex = n.SplitIndex();
    for (const auto& ins : inst) {
      if (findex == ins.index) {
        if (ins.fvalue < n.SplitCond()) {
          return n.LeftChild();
        } else {
          return n.RightChild();
        }
      }
    }
    return n.DefaultChild();
  }
  //  ------class member helpers---------
  /*! \brief initialize temp data structure */
  inline void InitData(const std::vector<GradientPair> &gpair,
                       const DMatrix &fmat,
                       const RegTree &tree) {
    {
      // setup position
      position_.resize(gpair.size());
      std::fill(position_.begin(), position_.end(), 0);
      // mark delete for the deleted datas
      for (size_t i = 0; i < position_.size(); ++i) {
        if (gpair[i].GetHess() < 0.0f) position_[i] = ~position_[i];
      }
      // mark subsample
      if (param_.subsample < 1.0f) {
        CHECK_EQ(param_.sampling_method, TrainParam::kUniform)
          << "Only uniform sampling is supported, "
          << "gradient-based sampling is only support by GPU Hist.";
        std::bernoulli_distribution coin_flip(param_.subsample);
        auto& rnd = common::GlobalRandom();
        for (size_t i = 0; i < position_.size(); ++i) {
          if (gpair[i].GetHess() < 0.0f) continue;
          if (!coin_flip(rnd)) position_[i] = ~position_[i];
        }
      }
    }
    {
      // expand query
      qexpand_.reserve(256); qexpand_.clear();
      qexpand_.push_back(0);
      this->UpdateNode2WorkIndex(tree);
    }
    this->interaction_constraints_.Configure(param_, fmat.Info().num_col_);
  }
  /*! \brief update queue expand add in new leaves */
  inline void UpdateQueueExpand(const RegTree &tree) {
    std::vector<int> newnodes;
    for (int nid : qexpand_) {
      if (!tree[nid].IsLeaf()) {
        newnodes.push_back(tree[nid].LeftChild());
        newnodes.push_back(tree[nid].RightChild());
      }
    }
    // use new nodes for qexpand
    qexpand_ = newnodes;
    this->UpdateNode2WorkIndex(tree);
  }
  // return decoded position
  inline int DecodePosition(bst_uint ridx) const {
    const int pid = position_[ridx];
    return pid < 0 ? ~pid : pid;
  }
  // encode the encoded position value for ridx
  inline void SetEncodePosition(bst_uint ridx, int nid) {
    if (position_[ridx] < 0) {
      position_[ridx] = ~nid;
    } else {
      position_[ridx] = nid;
    }
  }
  /*!
   * \brief This is a helper function that uses a column based data structure
   *        and reset the positions to the latest one
   * \param nodes the set of nodes that contains the split to be used
   * \param p_fmat feature matrix needed for tree construction
   * \param tree the regression tree structure
   */
  inline void ResetPositionCol(const std::vector<int> &nodes,
                               DMatrix *p_fmat,
                               const RegTree &tree) {
    // set the positions in the nondefault
    this->SetNonDefaultPositionCol(nodes, p_fmat, tree);
    this->SetDefaultPostion(p_fmat, tree);
  }
  /*!
   * \brief helper function to set the non-leaf positions to default direction.
   *  This function can be applied multiple times and will get the same result.
   * \param p_fmat feature matrix needed for tree construction
   * \param tree the regression tree structure
   */
  inline void SetDefaultPostion(DMatrix *p_fmat,
                                const RegTree &tree) {
    // set default direct nodes to default
    // for leaf nodes that are not fresh, mark then to ~nid,
    // so that they are ignored in future statistics collection
    common::ParallelFor(p_fmat->Info().num_row_, ctx_->Threads(), [&](auto ridx) {
      const int nid = this->DecodePosition(ridx);
      if (tree[nid].IsLeaf()) {
        // mark finish when it is not a fresh leaf
        if (tree[nid].RightChild() == -1) {
          position_[ridx] = ~nid;
        }
      } else {
        // push to default branch
        if (tree[nid].DefaultLeft()) {
          this->SetEncodePosition(ridx, tree[nid].LeftChild());
        } else {
          this->SetEncodePosition(ridx, tree[nid].RightChild());
        }
      }
    });
  }
  /*!
   * \brief this is helper function uses column based data structure,
   *  to CORRECT the positions of non-default directions that WAS set to default
   *  before calling this function.
   * \param batch The column batch
   * \param sorted_split_set The set of index that contains split solutions.
   * \param tree the regression tree structure
   */
  inline void CorrectNonDefaultPositionByBatch(
      const SparsePage &batch, const std::vector<bst_uint> &sorted_split_set,
      const RegTree &tree) {
    auto page = batch.GetView();
    for (size_t fid = 0; fid < batch.Size(); ++fid) {
      auto col = page[fid];
      auto it = std::lower_bound(sorted_split_set.begin(), sorted_split_set.end(), fid);

      if (it != sorted_split_set.end() && *it == fid) {
        common::ParallelFor(col.size(), ctx_->Threads(), [&](auto j) {
          const bst_uint ridx = col[j].index;
          const bst_float fvalue = col[j].fvalue;
          const int nid = this->DecodePosition(ridx);
          CHECK(tree[nid].IsLeaf());
          int pid = tree[nid].Parent();

          // go back to parent, correct those who are not default
          if (!tree[nid].IsRoot() && tree[pid].SplitIndex() == fid) {
            if (fvalue < tree[pid].SplitCond()) {
              this->SetEncodePosition(ridx, tree[pid].LeftChild());
            } else {
              this->SetEncodePosition(ridx, tree[pid].RightChild());
            }
          }
        });
      }
    }
  }
  /*!
   * \brief this is helper function uses column based data structure,
   * \param nodes the set of nodes that contains the split to be used
   * \param tree the regression tree structure
   * \param out_split_set The split index set
   */
  inline void GetSplitSet(const std::vector<int> &nodes,
                          const RegTree &tree,
                          std::vector<unsigned>* out_split_set) {
    std::vector<unsigned>& fsplits = *out_split_set;
    fsplits.clear();
    // step 1, classify the non-default data into right places
    for (int nid : nodes) {
      if (!tree[nid].IsLeaf()) {
        fsplits.push_back(tree[nid].SplitIndex());
      }
    }
    std::sort(fsplits.begin(), fsplits.end());
    fsplits.resize(std::unique(fsplits.begin(), fsplits.end()) - fsplits.begin());
  }
  /*!
   * \brief this is helper function uses column based data structure,
   *        update all positions into nondefault branch, if any, ignore the default branch
   * \param nodes the set of nodes that contains the split to be used
   * \param p_fmat feature matrix needed for tree construction
   * \param tree the regression tree structure
   */
  virtual void SetNonDefaultPositionCol(const std::vector<int> &nodes,
                                        DMatrix *p_fmat,
                                        const RegTree &tree) {
    std::vector<unsigned> fsplits;
    this->GetSplitSet(nodes, tree, &fsplits);
    for (const auto &batch : p_fmat->GetBatches<SortedCSCPage>()) {
      auto page = batch.GetView();
      for (auto fid : fsplits) {
        auto col = page[fid];
        common::ParallelFor(col.size(), ctx_->Threads(), [&](auto j) {
          const bst_uint ridx = col[j].index;
          const bst_float fvalue = col[j].fvalue;
          const int nid = this->DecodePosition(ridx);
          // go back to parent, correct those who are not default
          if (!tree[nid].IsLeaf() && tree[nid].SplitIndex() == fid) {
            if (fvalue < tree[nid].SplitCond()) {
              this->SetEncodePosition(ridx, tree[nid].LeftChild());
            } else {
              this->SetEncodePosition(ridx, tree[nid].RightChild());
            }
          }
        });
      }
    }
  }
  /*! \brief helper function to get statistics from a tree */
  template<typename TStats>
  inline void GetNodeStats(const std::vector<GradientPair> &gpair,
                           const DMatrix &fmat,
                           const RegTree &tree,
                           std::vector< std::vector<TStats> > *p_thread_temp,
                           std::vector<TStats> *p_node_stats) {
    std::vector< std::vector<TStats> > &thread_temp = *p_thread_temp;
    thread_temp.resize(ctx_->Threads());
    p_node_stats->resize(tree.param.num_nodes);
    dmlc::OMPException exc;
#pragma omp parallel num_threads(ctx_->Threads())
    {
      exc.Run([&]() {
        const int tid = omp_get_thread_num();
        thread_temp[tid].resize(tree.param.num_nodes, TStats());
        for (unsigned int nid : qexpand_) {
          thread_temp[tid][nid] = TStats();
        }
      });
    }
    exc.Rethrow();
    // setup position
    common::ParallelFor(fmat.Info().num_row_, ctx_->Threads(), [&](auto ridx) {
      const int nid = position_[ridx];
      const int tid = omp_get_thread_num();
      if (nid >= 0) {
        thread_temp[tid][nid].Add(gpair[ridx]);
      }
    });
    // sum the per thread statistics together
    for (int nid : qexpand_) {
      TStats &s = (*p_node_stats)[nid];
      s = TStats();
      for (size_t tid = 0; tid < thread_temp.size(); ++tid) {
        s.Add(thread_temp[tid][nid]);
      }
    }
  }
  using SketchEntry = common::SortedQuantile;
  /*! \brief training parameter of tree grower */
  TrainParam param_;
  /*! \brief queue of nodes to be expanded */
  std::vector<int> qexpand_;
  /*!
   * \brief map active node to is working index offset in qexpand,
   *   can be -1, which means the node is node actively expanding
   */
  std::vector<int> node2workindex_;
  /*!
   * \brief position of each instance in the tree
   *   can be negative, which means this position is no longer expanding
   *   see also Decode/EncodePosition
   */
  std::vector<int> position_;

  FeatureInteractionConstraintHost interaction_constraints_;

 private:
  inline void UpdateNode2WorkIndex(const RegTree &tree) {
    // update the node2workindex
    std::fill(node2workindex_.begin(), node2workindex_.end(), -1);
    node2workindex_.resize(tree.param.num_nodes);
    for (size_t i = 0; i < qexpand_.size(); ++i) {
      node2workindex_[qexpand_[i]] = static_cast<int>(i);
    }
  }
};
}  // namespace tree
}  // namespace xgboost
#endif  // XGBOOST_TREE_UPDATER_BASEMAKER_INL_H_
