// Copyright (c) 2018 Intel Corporation
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
// limitations under the License.

#ifndef NAV2_RECOVERIES__PLUGINS__BACK_UP_HPP_
#define NAV2_RECOVERIES__PLUGINS__BACK_UP_HPP_

#include <chrono>
#include <memory>

#include "nav2_recoveries/recovery.hpp"
#include "nav2_msgs/action/back_up.hpp"

namespace nav2_recoveries
{
using BackUpAction = nav2_msgs::action::BackUp;

/**
 * @class nav2_recoveries::BackUp
 * @brief An action server recovery for spinning in
 */
class BackUp : public Recovery<BackUpAction>
{
public:
  /**
   * @brief A constructor for nav2_recoveries::BackUp
   */
  BackUp();
  ~BackUp();

  /**
   * @brief Initialization to run behavior
   * @param command Goal to execute
   * @return Status of recovery
   */
  Status onRun(const std::shared_ptr<const BackUpAction::Goal> command) override;

  /**
   * @brief Loop function to run behavior
   * @return Status of recovery
   */
  Status onCycleUpdate() override;

protected:
  /**
   * @brief Check if pose is collision free
   * @param distance Distance to check forward
   * @param cmd_vel current commanded velocity
   * @param pose2d Current pose
   * @return is collision free or not
   */
  bool isCollisionFree(
    const double & distance,
    geometry_msgs::msg::Twist * cmd_vel,
    geometry_msgs::msg::Pose2D & pose2d);

  /**
   * @brief Configuration of recovery action
   */
  void onConfigure() override;

  double min_linear_vel_;
  double max_linear_vel_;
  double linear_acc_lim_;

  geometry_msgs::msg::PoseStamped initial_pose_;
  double command_x_;
  double command_speed_;
  double simulate_ahead_time_;

  BackUpAction::Feedback::SharedPtr feedback_;
};

}  // namespace nav2_recoveries

#endif  // NAV2_RECOVERIES__PLUGINS__BACK_UP_HPP_
