// Copyright (c) 2019 Intel Corporation
// Copyright (c) 2023 Open Navigation LLC
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

#ifndef NAV2_UTIL__NODE_UTILS_HPP_
#define NAV2_UTIL__NODE_UTILS_HPP_

#include <vector>
#include <string>
#include "rclcpp/rclcpp.hpp"
#include "rcl_interfaces/srv/list_parameters.hpp"

namespace nav2_util
{

/// Replace invalid characters in a potential node name
/**
 * There is frequently a need to create internal nodes. They must have a name,
 * and commonly the name is based on some parameter related to the node's
 * purpose. However, only alphanumeric characters and '_' are allowed in node
 * names. This function replaces any invalid character with a '_'
 *
 * \param[in] potential_node_name Potential name but possibly with invalid charaters.
 * \return A copy of the input string but with non-alphanumeric characters replaced with '_'
 */
std::string sanitize_node_name(const std::string & potential_node_name);

/// Concatenate two namespaces to produce an absolute namespace
/**
 * \param[in] top_ns The namespace to place first
 * \param[in] sub_ns The namespace to place after top_ns
 * \return An absolute namespace starting with "/"
*/
std::string add_namespaces(const std::string & top_ns, const std::string & sub_ns = "");

/// Add some random characters to a node name to ensure it is unique in the system
/**
 * There are utility classes that create an internal private node to interact
 * with the system. These private nodes are given a generated name. If multiple
 * clients end up using the same service, there is the potential for node name
 * conflicts. To ensure node names are globally unique, this appends some random
 * numbers to the end of the prefix.
 *
 * \param[in] prefix A string to help understand the purpose of the node.
 * \return A copy of the prefix + '_' + 8 random digits. eg. prefix_12345678
 */
std::string generate_internal_node_name(const std::string & prefix = "");

/// Creates a node with a name as generated by generate_internal_node_name
/**
 *  Creates a node with the following settings:
 *  - name generated by generate_internal_node_name
 *  - no parameter services
 *  - no parameter event publisher
 *
 * \param[in] prefix A string to help understand the purpose of the node.
 * \return A shared_ptr to the node.
 */
rclcpp::Node::SharedPtr generate_internal_node(const std::string & prefix = "");

/// Generates a pseudo random string of digits.
/**
 * Generates pseudo random digits by converting the current system time to a
 * string. This means that any length more than 8 or so digits will just get
 * padded with zeros and doesn't add any additional randomness.
 *
 * \param[in] len Length of the output string
 * \return A string containing random digits
 */
std::string time_to_string(size_t len);

/// Declares static ROS2 parameter and sets it to a given value if it was not already declared
/* Declares static ROS2 parameter and sets it to a given value
 * if it was not already declared.
 *
 * \param[in] node A node in which given parameter to be declared
 * \param[in] param_name The name of parameter
 * \param[in] default_value Parameter value to initialize with
 * \param[in] parameter_descriptor Parameter descriptor (optional)
 */
template<typename NodeT>
void declare_parameter_if_not_declared(
  NodeT node,
  const std::string & param_name,
  const rclcpp::ParameterValue & default_value,
  const rcl_interfaces::msg::ParameterDescriptor & parameter_descriptor =
  rcl_interfaces::msg::ParameterDescriptor())
{
  if (!node->has_parameter(param_name)) {
    node->declare_parameter(param_name, default_value, parameter_descriptor);
  }
}

/// Declares static ROS2 parameter with given type if it was not already declared
/* Declares static ROS2 parameter with given type if it was not already declared.
 *
 * \param[in] node A node in which given parameter to be declared
 * \param[in] param_type The type of parameter
 * \param[in] default_value Parameter value to initialize with
 * \param[in] parameter_descriptor Parameter descriptor (optional)
 */
template<typename NodeT>
void declare_parameter_if_not_declared(
  NodeT node,
  const std::string & param_name,
  const rclcpp::ParameterType & param_type,
  const rcl_interfaces::msg::ParameterDescriptor & parameter_descriptor =
  rcl_interfaces::msg::ParameterDescriptor())
{
  if (!node->has_parameter(param_name)) {
    node->declare_parameter(param_name, param_type, parameter_descriptor);
  }
}

/// Gets the type of plugin for the selected node and its plugin
/**
 * Gets the type of plugin for the selected node and its plugin.
 * Actually seeks for the value of "<plugin_name>.plugin" parameter.
 *
 * \param[in] node Selected node
 * \param[in] plugin_name The name of plugin the type of which is being searched for
 * \return A string containing the type of plugin (the value of "<plugin_name>.plugin" parameter)
 */
template<typename NodeT>
std::string get_plugin_type_param(
  NodeT node,
  const std::string & plugin_name)
{
  declare_parameter_if_not_declared(node, plugin_name + ".plugin", rclcpp::PARAMETER_STRING);
  std::string plugin_type;
  try {
    if (!node->get_parameter(plugin_name + ".plugin", plugin_type)) {
      RCLCPP_FATAL(
        node->get_logger(), "Can not get 'plugin' param value for %s", plugin_name.c_str());
      throw std::runtime_error("No 'plugin' param for param ns!");
    }
  } catch (rclcpp::exceptions::ParameterUninitializedException & ex) {
    RCLCPP_FATAL(node->get_logger(), "'plugin' param not defined for %s", plugin_name.c_str());
    throw std::runtime_error("No 'plugin' param for param ns!");
  }

  return plugin_type;
}

/**
 * @brief Sets the caller thread to have a soft-realtime prioritization by
 * increasing the priority level of the host thread.
 * May throw exception if unable to set prioritization successfully
 */
void setSoftRealTimePriority();

}  // namespace nav2_util

#endif  // NAV2_UTIL__NODE_UTILS_HPP_
