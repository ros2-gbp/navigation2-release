// Copyright (c) 2019 Intel Corporation
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

#ifndef NAV2_RVIZ_PLUGINS__NAV2_PANEL_HPP_
#define NAV2_RVIZ_PLUGINS__NAV2_PANEL_HPP_

#include <QtWidgets>
#include <QBasicTimer>

#include <memory>
#include <string>
#include <vector>

#include "nav2_lifecycle_manager/lifecycle_manager_client.hpp"
#include "nav2_msgs/action/navigate_to_pose.hpp"
#include "nav2_msgs/action/follow_waypoints.hpp"
#include "nav2_rviz_plugins/ros_action_qevent.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "rviz_common/panel.hpp"
#include "tf2_geometry_msgs/tf2_geometry_msgs.h"
#include "visualization_msgs/msg/marker_array.hpp"
#include "nav2_util/geometry_utils.hpp"

class QPushButton;

namespace nav2_rviz_plugins
{

class InitialThread;

/// Panel to interface to the nav2 stack
class Nav2Panel : public rviz_common::Panel
{
  Q_OBJECT

public:
  explicit Nav2Panel(QWidget * parent = 0);
  virtual ~Nav2Panel();

  void onInitialize() override;

  /// Load and save configuration data
  void load(const rviz_common::Config & config) override;
  void save(rviz_common::Config config) const override;

private Q_SLOTS:
  void startThread();
  void onStartup();
  void onShutdown();
  void onCancel();
  void onPause();
  void onResume();
  void onAccumulated();
  void onAccumulating();
  void onNewGoal(double x, double y, double theta, QString frame);

private:
  void loadLogFiles();
  void onCancelButtonPressed();
  void timerEvent(QTimerEvent * event) override;

  // Call to send NavigateToPose action request for goal poses
  void startWaypointFollowing(std::vector<geometry_msgs::msg::PoseStamped> poses);
  void startNavigation(geometry_msgs::msg::PoseStamped);
  using NavigationGoalHandle =
    rclcpp_action::ClientGoalHandle<nav2_msgs::action::NavigateToPose>;
  using WaypointFollowerGoalHandle =
    rclcpp_action::ClientGoalHandle<nav2_msgs::action::FollowWaypoints>;

  // The (non-spinning) client node used to invoke the action client
  rclcpp::Node::SharedPtr client_node_;

  // A timer used to check on the completion status of the action
  QBasicTimer timer_;

  // The NavigateToPose action client
  rclcpp_action::Client<nav2_msgs::action::NavigateToPose>::SharedPtr navigation_action_client_;
  rclcpp_action::Client<nav2_msgs::action::FollowWaypoints>::SharedPtr
    waypoint_follower_action_client_;

  // Goal-related state
  nav2_msgs::action::NavigateToPose::Goal navigation_goal_;
  nav2_msgs::action::FollowWaypoints::Goal waypoint_follower_goal_;
  NavigationGoalHandle::SharedPtr navigation_goal_handle_;
  WaypointFollowerGoalHandle::SharedPtr waypoint_follower_goal_handle_;

  // The client used to control the nav2 stack
  nav2_lifecycle_manager::LifecycleManagerClient client_;

  QPushButton * start_reset_button_{nullptr};
  QPushButton * pause_resume_button_{nullptr};
  QPushButton * navigation_mode_button_{nullptr};

  QStateMachine state_machine_;
  InitialThread * initial_thread_;

  QState * pre_initial_{nullptr};
  QState * initial_{nullptr};
  QState * idle_{nullptr};
  QState * reset_{nullptr};
  QState * paused_{nullptr};
  QState * resumed_{nullptr};
  // The following states are added to allow for the state of the button to only expose reset
  // while the NavigateToPoses action is not active. While running, the user will be allowed to
  // cancel the action. The ROSActionTransition allows for the state of the action to be detected
  // and the button state to change automatically.
  QState * running_{nullptr};
  QState * canceled_{nullptr};
  // The following states are added to allow to collect several poses to perform a waypoint-mode
  // navigation
  QState * accumulating_{nullptr};
  QState * accumulated_{nullptr};

  std::vector<geometry_msgs::msg::PoseStamped> acummulated_poses_;

  // Publish the visual markers with the waypoints
  void updateWpNavigationMarkers();
  // Waypoint navigation visual markers publisher
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr wp_navigation_markers_pub_;
};

class InitialThread : public QThread
{
  Q_OBJECT

public:
  using SystemStatus = nav2_lifecycle_manager::SystemStatus;

  explicit InitialThread(nav2_lifecycle_manager::LifecycleManagerClient & client)
  : client_(client)
  {}

  void run() override
  {
    SystemStatus status = SystemStatus::TIMEOUT;
    while (status == SystemStatus::TIMEOUT) {
      status = client_.is_active(std::chrono::seconds(1));
    }
    if (status == SystemStatus::ACTIVE) {
      emit activeSystem();
    } else {
      emit inactiveSystem();
    }
  }

signals:
  void activeSystem();
  void inactiveSystem();

private:
  nav2_lifecycle_manager::LifecycleManagerClient client_;
};

}  // namespace nav2_rviz_plugins

#endif  //  NAV2_RVIZ_PLUGINS__NAV2_PANEL_HPP_
