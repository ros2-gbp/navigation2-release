// Copyright (c) 2020, Samsung Research America
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License. Reserved.

#ifndef NAV2_SMAC_PLANNER__NODE_HYBRID_HPP_
#define NAV2_SMAC_PLANNER__NODE_HYBRID_HPP_

#include <math.h>
#include <vector>
#include <cmath>
#include <iostream>
#include <functional>
#include <queue>
#include <memory>
#include <utility>
#include <limits>

#include "ompl/base/StateSpace.h"

#include "nav2_smac_planner/constants.hpp"
#include "nav2_smac_planner/types.hpp"
#include "nav2_smac_planner/collision_checker.hpp"
#include "nav2_smac_planner/costmap_downsampler.hpp"

namespace nav2_smac_planner
{

typedef std::vector<float> LookupTable;
typedef std::pair<double, double> TrigValues;

// Need seperate pose struct for motion table operations

/**
 * @struct nav2_smac_planner::MotionPose
 * @brief A struct for poses in motion primitives
 */
struct MotionPose
{
  /**
   * @brief A constructor for nav2_smac_planner::MotionPose
   */
  MotionPose() {}

  /**
   * @brief A constructor for nav2_smac_planner::MotionPose
   * @param x X pose
   * @param y Y pose
   * @param theta Angle of pose
   */
  MotionPose(const float & x, const float & y, const float & theta)
  : _x(x), _y(y), _theta(theta)
  {}

  float _x;
  float _y;
  float _theta;
};

typedef std::vector<MotionPose> MotionPoses;

// Must forward declare
class NodeHybrid;

/**
 * @struct nav2_smac_planner::HybridMotionTable
 * @brief A table of motion primitives and related functions
 */
struct HybridMotionTable
{
  /**
   * @brief A constructor for nav2_smac_planner::HybridMotionTable
   */
  HybridMotionTable() {}

  /**
   * @brief Initializing using Dubin model
   * @param size_x_in Size of costmap in X
   * @param size_y_in Size of costmap in Y
   * @param angle_quantization_in Size of costmap in bin sizes
   * @param search_info Parameters for searching
   */
  void initDubin(
    unsigned int & size_x_in,
    unsigned int & size_y_in,
    unsigned int & angle_quantization_in,
    SearchInfo & search_info);

  /**
   * @brief Initializing using Reeds-Shepp model
   * @param size_x_in Size of costmap in X
   * @param size_y_in Size of costmap in Y
   * @param angle_quantization_in Size of costmap in bin sizes
   * @param search_info Parameters for searching
   */
  void initReedsShepp(
    unsigned int & size_x_in,
    unsigned int & size_y_in,
    unsigned int & angle_quantization_in,
    SearchInfo & search_info);

  /**
   * @brief Get projections of motion models
   * @param node Ptr to NodeHybrid
   * @return A set of motion poses
   */
  MotionPoses getProjections(const NodeHybrid * node);

  MotionModel motion_model = MotionModel::UNKNOWN;
  MotionPoses projections;
  unsigned int size_x;
  unsigned int num_angle_quantization;
  float num_angle_quantization_float;
  float min_turning_radius;
  float bin_size;
  float change_penalty;
  float non_straight_penalty;
  float cost_penalty;
  float reverse_penalty;
  ompl::base::StateSpacePtr state_space;
  std::vector<std::vector<double>> delta_xs;
  std::vector<std::vector<double>> delta_ys;
  std::vector<TrigValues> trig_values;
};

/**
 * @class nav2_smac_planner::NodeHybrid
 * @brief NodeHybrid implementation for graph, Hybrid-A*
 */
class NodeHybrid
{
public:
  typedef NodeHybrid * NodePtr;
  typedef std::unique_ptr<std::vector<NodeHybrid>> Graph;
  typedef std::vector<NodePtr> NodeVector;

  /**
   * @class nav2_smac_planner::NodeHybrid::Coordinates
   * @brief NodeHybrid implementation of coordinate structure
   */
  struct Coordinates
  {
    /**
     * @brief A constructor for nav2_smac_planner::NodeHybrid::Coordinates
     */
    Coordinates() {}

    /**
     * @brief A constructor for nav2_smac_planner::NodeHybrid::Coordinates
     * @param x_in X coordinate
     * @param y_in Y coordinate
     * @param theta_in Theta coordinate
     */
    Coordinates(const float & x_in, const float & y_in, const float & theta_in)
    : x(x_in), y(y_in), theta(theta_in)
    {}

    inline bool operator==(const Coordinates & rhs)
    {
      return this->x == rhs.x && this->y == rhs.y && this->theta == rhs.theta;
    }

    inline bool operator!=(const Coordinates & rhs)
    {
      return !(*this == rhs);
    }

    float x, y, theta;
  };

  typedef std::vector<Coordinates> CoordinateVector;

  /**
   * @brief A constructor for nav2_smac_planner::NodeHybrid
   * @param index The index of this node for self-reference
   */
  explicit NodeHybrid(const unsigned int index);

  /**
   * @brief A destructor for nav2_smac_planner::NodeHybrid
   */
  ~NodeHybrid();

  /**
   * @brief operator== for comparisons
   * @param NodeHybrid right hand side node reference
   * @return If cell indicies are equal
   */
  bool operator==(const NodeHybrid & rhs)
  {
    return this->_index == rhs._index;
  }

  /**
   * @brief setting continuous coordinate search poses (in partial-cells)
   * @param Pose pose
   */
  inline void setPose(const Coordinates & pose_in)
  {
    pose = pose_in;
  }

  /**
   * @brief Reset method for new search
   */
  void reset();

  /**
   * @brief Gets the accumulated cost at this node
   * @return accumulated cost
   */
  inline float & getAccumulatedCost()
  {
    return _accumulated_cost;
  }

  /**
   * @brief Sets the accumulated cost at this node
   * @param reference to accumulated cost
   */
  inline void setAccumulatedCost(const float & cost_in)
  {
    _accumulated_cost = cost_in;
  }

  /**
   * @brief Sets the motion primitive index used to achieve node in search
   * @param reference to motion primitive idx
   */
  inline void setMotionPrimitiveIndex(const unsigned int & idx)
  {
    _motion_primitive_index = idx;
  }

  /**
   * @brief Gets the motion primitive index used to achieve node in search
   * @return reference to motion primitive idx
   */
  inline unsigned int & getMotionPrimitiveIndex()
  {
    return _motion_primitive_index;
  }

  /**
   * @brief Gets the costmap cost at this node
   * @return costmap cost
   */
  inline float & getCost()
  {
    return _cell_cost;
  }

  /**
   * @brief Gets if cell has been visited in search
   * @param If cell was visited
   */
  inline bool & wasVisited()
  {
    return _was_visited;
  }

  /**
   * @brief Sets if cell has been visited in search
   */
  inline void visited()
  {
    _was_visited = true;
  }

  /**
   * @brief Gets cell index
   * @return Reference to cell index
   */
  inline unsigned int & getIndex()
  {
    return _index;
  }

  /**
   * @brief Check if this node is valid
   * @param traverse_unknown If we can explore unknown nodes on the graph
   * @return whether this node is valid and collision free
   */
  bool isNodeValid(const bool & traverse_unknown, GridCollisionChecker * collision_checker);

  /**
   * @brief Get traversal cost of parent node to child node
   * @param child Node pointer to child
   * @return traversal cost
   */
  float getTraversalCost(const NodePtr & child);

  /**
   * @brief Get index at coordinates
   * @param x X coordinate of point
   * @param y Y coordinate of point
   * @param angle Theta coordinate of point
   * @param width Width of costmap
   * @param angle_quantization Number of theta bins
   * @return Index
   */
  static inline unsigned int getIndex(
    const unsigned int & x, const unsigned int & y, const unsigned int & angle,
    const unsigned int & width, const unsigned int & angle_quantization)
  {
    return angle + x * angle_quantization + y * width * angle_quantization;
  }

  /**
   * @brief Get index at coordinates
   * @param x X coordinate of point
   * @param y Y coordinate of point
   * @param angle Theta coordinate of point
   * @return Index
   */
  static inline unsigned int getIndex(
    const unsigned int & x, const unsigned int & y, const unsigned int & angle)
  {
    return getIndex(
      x, y, angle, motion_table.size_x,
      motion_table.num_angle_quantization);
  }

  /**
   * @brief Get coordinates at index
   * @param index Index of point
   * @param width Width of costmap
   * @param angle_quantization Theta size of costmap
   * @return Coordinates
   */
  static inline Coordinates getCoords(
    const unsigned int & index,
    const unsigned int & width, const unsigned int & angle_quantization)
  {
    return Coordinates(
      (index / angle_quantization) % width,    // x
      index / (angle_quantization * width),    // y
      index % angle_quantization);    // theta
  }

  /**
   * @brief Get cost of heuristic of node
   * @param node Node index current
   * @param node Node index of new
   * @param costmap Costmap ptr to use
   * @return Heuristic cost between the nodes
   */
  static float getHeuristicCost(
    const Coordinates & node_coords,
    const Coordinates & goal_coordinates,
    const nav2_costmap_2d::Costmap2D * costmap);

  /**
   * @brief Initialize motion models
   * @param motion_model Motion model enum to use
   * @param size_x Size of X of graph
   * @param size_y Size of y of graph
   * @param angle_quantization Size of theta bins of graph
   * @param search_info Search info to use
   */
  static void initMotionModel(
    const MotionModel & motion_model,
    unsigned int & size_x,
    unsigned int & size_y,
    unsigned int & angle_quantization,
    SearchInfo & search_info);

  /**
   * @brief Compute the SE2 distance heuristic
   * @param lookup_table_dim Size, in costmap pixels, of the
   * each lookup table dimension to populate
   * @param motion_model Motion model to use for state space
   * @param dim_3_size Number of quantization bins for caching
   * @param search_info Info containing minimum radius to use
   */
  static void precomputeDistanceHeuristic(
    const float & lookup_table_dim,
    const MotionModel & motion_model,
    const unsigned int & dim_3_size,
    const SearchInfo & search_info);

  /**
   * @brief Compute the Obstacle heuristic
   * @param node_coords Coordinates to get heuristic at
   * @param goal_coords Coordinates to compute heuristic to
   * @return heuristic Heuristic value
   */
  static float getObstacleHeuristic(
    const Coordinates & node_coords,
    const Coordinates & goal_coords);

  /**
   * @brief Compute the Distance heuristic
   * @param node_coords Coordinates to get heuristic at
   * @param goal_coords Coordinates to compute heuristic to
   * @param obstacle_heuristic Value of the obstacle heuristic to compute
   * additional motion heuristics if required
   * @return heuristic Heuristic value
   */
  static float getDistanceHeuristic(
    const Coordinates & node_coords,
    const Coordinates & goal_coords,
    const float & obstacle_heuristic);

  /**
   * @brief reset the obstacle heuristic state
   * @param costmap Costmap to use
   * @param goal_coords Coordinates to start heuristic expansion at
   */
  static void resetObstacleHeuristic(
    nav2_costmap_2d::Costmap2D * costmap,
    const unsigned int & goal_x, const unsigned int & goal_y);

  /**
   * @brief Retrieve all valid neighbors of a node.
   * @param validity_checker Functor for state validity checking
   * @param collision_checker Collision checker to use
   * @param traverse_unknown If unknown costs are valid to traverse
   * @param neighbors Vector of neighbors to be filled
   */
  void getNeighbors(
    std::function<bool(const unsigned int &, nav2_smac_planner::NodeHybrid * &)> & validity_checker,
    GridCollisionChecker * collision_checker,
    const bool & traverse_unknown,
    NodeVector & neighbors);

  NodeHybrid * parent;
  Coordinates pose;

  // Constants required across all nodes but don't want to allocate more than once
  static double travel_distance_cost;
  static HybridMotionTable motion_table;
  // Wavefront lookup and queue for continuing to expand as needed
  static LookupTable obstacle_heuristic_lookup_table;
  static std::queue<unsigned int> obstacle_heuristic_queue;
  static nav2_costmap_2d::Costmap2D * sampled_costmap;
  static CostmapDownsampler downsampler;
  // Dubin / Reeds-Shepp lookup and size for dereferencing
  static LookupTable dist_heuristic_lookup_table;
  static float size_lookup;

private:
  float _cell_cost;
  float _accumulated_cost;
  unsigned int _index;
  bool _was_visited;
  unsigned int _motion_primitive_index;
};

}  // namespace nav2_smac_planner

#endif  // NAV2_SMAC_PLANNER__NODE_HYBRID_HPP_
