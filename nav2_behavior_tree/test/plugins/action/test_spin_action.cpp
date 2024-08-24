// Copyright (c) 2018 Intel Corporation
// Copyright (c) 2020 Sarthak Mittal
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

#include <gtest/gtest.h>
#include <memory>
#include <set>
#include <string>

#include "behaviortree_cpp/bt_factory.h"

#include "utils/test_action_server.hpp"
#include "nav2_behavior_tree/plugins/action/spin_action.hpp"

class SpinActionServer : public TestActionServer<nav2_msgs::action::Spin>
{
public:
  SpinActionServer()
  : TestActionServer("spin")
  {}

protected:
  void execute(
    const typename std::shared_ptr<rclcpp_action::ServerGoalHandle<nav2_msgs::action::Spin>>
    goal_handle)
  override
  {
    nav2_msgs::action::Spin::Result::SharedPtr result =
      std::make_shared<nav2_msgs::action::Spin::Result>();
    bool return_success = getReturnSuccess();
    if (return_success) {
      goal_handle->succeed(result);
    } else {
      goal_handle->abort(result);
    }
  }
};

class SpinActionTestFixture : public ::testing::Test
{
public:
  static void SetUpTestCase()
  {
    node_ = std::make_shared<rclcpp::Node>("spin_action_test_fixture");
    factory_ = std::make_shared<BT::BehaviorTreeFactory>();
    config_ = new BT::NodeConfiguration();

    // Create the blackboard that will be shared by all of the nodes in the tree
    config_->blackboard = BT::Blackboard::create();
    // Put items on the blackboard
    config_->blackboard->set(
      "node",
      node_);
    config_->blackboard->set<std::chrono::milliseconds>(
      "server_timeout",
      std::chrono::milliseconds(20));
    config_->blackboard->set<std::chrono::milliseconds>(
      "bt_loop_duration",
      std::chrono::milliseconds(10));
    config_->blackboard->set<std::chrono::milliseconds>(
      "wait_for_service_timeout",
      std::chrono::milliseconds(1000));
    config_->blackboard->set("initial_pose_received", false);
    config_->blackboard->set("number_recoveries", 0);

    BT::NodeBuilder builder =
      [](const std::string & name, const BT::NodeConfiguration & config)
      {
        return std::make_unique<nav2_behavior_tree::SpinAction>(
          name, "spin", config);
      };

    factory_->registerBuilder<nav2_behavior_tree::SpinAction>("Spin", builder);
  }

  static void TearDownTestCase()
  {
    delete config_;
    config_ = nullptr;
    node_.reset();
    action_server_.reset();
    factory_.reset();
  }

  void SetUp() override
  {
    config_->blackboard->set("number_recoveries", 0);
  }

  void TearDown() override
  {
    tree_.reset();
  }

  static std::shared_ptr<SpinActionServer> action_server_;

protected:
  static rclcpp::Node::SharedPtr node_;
  static BT::NodeConfiguration * config_;
  static std::shared_ptr<BT::BehaviorTreeFactory> factory_;
  static std::shared_ptr<BT::Tree> tree_;
};

rclcpp::Node::SharedPtr SpinActionTestFixture::node_ = nullptr;
std::shared_ptr<SpinActionServer> SpinActionTestFixture::action_server_ = nullptr;
BT::NodeConfiguration * SpinActionTestFixture::config_ = nullptr;
std::shared_ptr<BT::BehaviorTreeFactory> SpinActionTestFixture::factory_ = nullptr;
std::shared_ptr<BT::Tree> SpinActionTestFixture::tree_ = nullptr;

TEST_F(SpinActionTestFixture, test_ports)
{
  std::string xml_txt =
    R"(
      <root BTCPP_format="4">
        <BehaviorTree ID="MainTree">
            <Spin server_name="spin"/>
        </BehaviorTree>
      </root>)";

  tree_ = std::make_shared<BT::Tree>(factory_->createTreeFromText(xml_txt, config_->blackboard));
  EXPECT_EQ(tree_->rootNode()->getInput<double>("spin_dist"), 1.57);

  xml_txt =
    R"(
      <root BTCPP_format="4">
        <BehaviorTree ID="MainTree">
            <Spin spin_dist="3.14" />
        </BehaviorTree>
      </root>)";

  tree_ = std::make_shared<BT::Tree>(factory_->createTreeFromText(xml_txt, config_->blackboard));
  EXPECT_EQ(tree_->rootNode()->getInput<double>("spin_dist"), 3.14);
}

TEST_F(SpinActionTestFixture, test_tick)
{
  std::string xml_txt =
    R"(
      <root BTCPP_format="4">
        <BehaviorTree ID="MainTree">
            <Spin spin_dist="3.14" />
        </BehaviorTree>
      </root>)";

  tree_ = std::make_shared<BT::Tree>(factory_->createTreeFromText(xml_txt, config_->blackboard));
  EXPECT_EQ(config_->blackboard->get<int>("number_recoveries"), 0);

  while (tree_->rootNode()->status() != BT::NodeStatus::SUCCESS) {
    tree_->rootNode()->executeTick();
  }

  EXPECT_EQ(tree_->rootNode()->status(), BT::NodeStatus::SUCCESS);
  EXPECT_EQ(config_->blackboard->get<int>("number_recoveries"), 1);
  EXPECT_EQ(action_server_->getCurrentGoal()->target_yaw, 3.14f);
}

TEST_F(SpinActionTestFixture, test_failure)
{
  std::string xml_txt =
    R"(
      <root BTCPP_format="4">
        <BehaviorTree ID="MainTree">
            <Spin spin_dist="3.14" />
        </BehaviorTree>
      </root>)";

  tree_ = std::make_shared<BT::Tree>(factory_->createTreeFromText(xml_txt, config_->blackboard));
  action_server_->setReturnSuccess(false);

  EXPECT_EQ(config_->blackboard->get<int>("number_recoveries"), 0);
  while (tree_->rootNode()->status() != BT::NodeStatus::SUCCESS &&
    tree_->rootNode()->status() != BT::NodeStatus::FAILURE)
  {
    tree_->rootNode()->executeTick();
  }

  std::cout << tree_->rootNode()->status();

  EXPECT_EQ(tree_->rootNode()->status(), BT::NodeStatus::FAILURE);
  EXPECT_EQ(config_->blackboard->get<int>("number_recoveries"), 1);
  EXPECT_EQ(action_server_->getCurrentGoal()->target_yaw, 3.14f);
}

int main(int argc, char ** argv)
{
  ::testing::InitGoogleTest(&argc, argv);

  // initialize ROS
  rclcpp::init(argc, argv);

  // initialize action server and spin on new thread
  SpinActionTestFixture::action_server_ = std::make_shared<SpinActionServer>();
  std::thread server_thread([]() {
      rclcpp::spin(SpinActionTestFixture::action_server_);
    });

  int all_successful = RUN_ALL_TESTS();

  // shutdown ROS
  rclcpp::shutdown();
  server_thread.join();

  return all_successful;
}
