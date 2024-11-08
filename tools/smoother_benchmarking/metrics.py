#! /usr/bin/env python3
# Copyright (c) 2022 Samsung R&D Institute Russia
# Copyright (c) 2022 Joshua Wallace
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math
import os
import pickle
from random import randint, seed, uniform

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import numpy as np
import rclpy
from transforms3d.euler import euler2quat


# Note: Map origin is assumed to be (0,0)


def getPlannerResults(navigator, initial_pose, goal_pose, planner):
    result = navigator._getPathImpl(initial_pose, goal_pose, planner, use_start=True)
    if result is None or result.error_code != 0:
        print(planner, 'planner failed to produce the path')
        return None
    return result


def getSmootherResults(navigator, path, smoothers):
    smoothed_results = []
    for smoother in smoothers:
        smoothed_result = navigator._smoothPathImpl(path, smoother)
        if smoothed_result is not None:
            smoothed_results.append(smoothed_result)
        else:
            print(smoother, 'failed to smooth the path')
            return None
    return smoothed_results


def getRandomStart(costmap, max_cost, side_buffer, time_stamp, res):
    start = PoseStamped()
    start.header.frame_id = 'map'
    start.header.stamp = time_stamp
    while True:
        row = randint(side_buffer, costmap.shape[0] - side_buffer)
        col = randint(side_buffer, costmap.shape[1] - side_buffer)

        if costmap[row, col] < max_cost:
            start.pose.position.x = col * res
            start.pose.position.y = row * res

            yaw = uniform(0, 1) * 2 * math.pi
            quad = euler2quat(0.0, 0.0, yaw)
            start.pose.orientation.w = quad[0]
            start.pose.orientation.x = quad[1]
            start.pose.orientation.y = quad[2]
            start.pose.orientation.z = quad[3]
            break
    return start


def getRandomGoal(costmap, start, max_cost, side_buffer, time_stamp, res):
    goal = PoseStamped()
    goal.header.frame_id = 'map'
    goal.header.stamp = time_stamp
    while True:
        row = randint(side_buffer, costmap.shape[0] - side_buffer)
        col = randint(side_buffer, costmap.shape[1] - side_buffer)

        start_x = start.pose.position.x
        start_y = start.pose.position.y
        goal_x = col * res
        goal_y = row * res
        x_diff = goal_x - start_x
        y_diff = goal_y - start_y
        dist = math.sqrt(x_diff ** 2 + y_diff ** 2)

        if costmap[row, col] < max_cost and dist > 3.0:
            goal.pose.position.x = goal_x
            goal.pose.position.y = goal_y

            yaw = uniform(0, 1) * 2 * math.pi
            quad = euler2quat(0.0, 0.0, yaw)
            goal.pose.orientation.w = quad[0]
            goal.pose.orientation.x = quad[1]
            goal.pose.orientation.y = quad[2]
            goal.pose.orientation.z = quad[3]
            break
    return goal


def main():
    rclpy.init()

    navigator = BasicNavigator()

    # Wait for planner and smoother to fully activate
    print('Waiting for planner and smoother servers to activate')
    navigator.waitUntilNav2Active('smoother_server', 'planner_server')

    # Get the costmap for start/goal validation
    costmap_msg = navigator.getGlobalCostmap()
    costmap = np.asarray(costmap_msg.data)
    costmap.resize(costmap_msg.metadata.size_y, costmap_msg.metadata.size_x)

    planner = 'SmacHybrid'
    smoothers = ['simple_smoother', 'constrained_smoother', 'sg_smoother']
    max_cost = 210
    side_buffer = 10
    time_stamp = navigator.get_clock().now().to_msg()
    results = []
    seed(33)

    random_pairs = 100
    i = 0
    res = costmap_msg.metadata.resolution
    while i < random_pairs:
        print('Cycle: ', i, 'out of: ', random_pairs)
        start = getRandomStart(costmap, max_cost, side_buffer, time_stamp, res)
        goal = getRandomGoal(costmap, start, max_cost, side_buffer, time_stamp, res)
        print('Start', start)
        print('Goal', goal)
        result = getPlannerResults(navigator, start, goal, planner)
        if result is not None:
            smoothed_results = getSmootherResults(navigator, result.path, smoothers)
            if smoothed_results is not None:
                results.append(result)
                results.append(smoothed_results)
                i += 1

    print('Write Results...')
    benchmark_dir = os.getcwd()
    with open(os.path.join(benchmark_dir, 'results.pickle'), 'wb') as f:
        pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

    with open(os.path.join(benchmark_dir, 'costmap.pickle'), 'wb') as f:
        pickle.dump(costmap_msg, f, pickle.HIGHEST_PROTOCOL)

    smoothers.insert(0, planner)
    with open(os.path.join(benchmark_dir, 'methods.pickle'), 'wb') as f:
        pickle.dump(smoothers, f, pickle.HIGHEST_PROTOCOL)
    print('Write Complete')

    exit(0)


if __name__ == '__main__':
    main()
