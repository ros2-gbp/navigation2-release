%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/humble/.*$
%global __requires_exclude_from ^/opt/ros/humble/.*$

Name:           ros-humble-nav2-costmap-2d
Version:        1.1.6
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS nav2_costmap_2d package

License:        BSD-3-Clause and Apache-2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-humble-angles
Requires:       ros-humble-geometry-msgs
Requires:       ros-humble-laser-geometry
Requires:       ros-humble-map-msgs
Requires:       ros-humble-message-filters
Requires:       ros-humble-nav-msgs
Requires:       ros-humble-nav2-msgs
Requires:       ros-humble-nav2-util
Requires:       ros-humble-nav2-voxel-grid
Requires:       ros-humble-pluginlib
Requires:       ros-humble-rclcpp
Requires:       ros-humble-rclcpp-lifecycle
Requires:       ros-humble-sensor-msgs
Requires:       ros-humble-std-msgs
Requires:       ros-humble-std-srvs
Requires:       ros-humble-tf2
Requires:       ros-humble-tf2-geometry-msgs
Requires:       ros-humble-tf2-ros
Requires:       ros-humble-tf2-sensor-msgs
Requires:       ros-humble-visualization-msgs
Requires:       ros-humble-ros-workspace
BuildRequires:  ros-humble-ament-cmake
BuildRequires:  ros-humble-angles
BuildRequires:  ros-humble-geometry-msgs
BuildRequires:  ros-humble-laser-geometry
BuildRequires:  ros-humble-map-msgs
BuildRequires:  ros-humble-message-filters
BuildRequires:  ros-humble-nav-msgs
BuildRequires:  ros-humble-nav2-common
BuildRequires:  ros-humble-nav2-msgs
BuildRequires:  ros-humble-nav2-util
BuildRequires:  ros-humble-nav2-voxel-grid
BuildRequires:  ros-humble-pluginlib
BuildRequires:  ros-humble-rclcpp
BuildRequires:  ros-humble-rclcpp-lifecycle
BuildRequires:  ros-humble-sensor-msgs
BuildRequires:  ros-humble-std-msgs
BuildRequires:  ros-humble-std-srvs
BuildRequires:  ros-humble-tf2
BuildRequires:  ros-humble-tf2-geometry-msgs
BuildRequires:  ros-humble-tf2-ros
BuildRequires:  ros-humble-tf2-sensor-msgs
BuildRequires:  ros-humble-visualization-msgs
BuildRequires:  ros-humble-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-humble-ament-cmake-gtest
BuildRequires:  ros-humble-ament-lint-auto
BuildRequires:  ros-humble-ament-lint-common
BuildRequires:  ros-humble-launch
BuildRequires:  ros-humble-launch-testing
BuildRequires:  ros-humble-nav2-lifecycle-manager
BuildRequires:  ros-humble-nav2-map-server
%endif

%description
This package provides an implementation of a 2D costmap that takes in sensor
data from the world, builds a 2D or 3D occupancy grid of the data (depending on
whether a voxel based implementation is used), and inflates costs in a 2D
costmap based on the occupancy grid and a user specified inflation radius. This
package also provides support for map_server based initialization of a costmap,
rolling window based costmaps, and parameter based subscription to and
configuration of sensor topics.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/humble" \
    -DAMENT_PREFIX_PATH="/opt/ros/humble" \
    -DCMAKE_PREFIX_PATH="/opt/ros/humble" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/humble

%changelog
* Fri Feb 10 2023 Steve Macenski <stevenmacenski@gmail.com> - 1.1.6-1
- Autogenerated by Bloom

* Thu Dec 22 2022 Steve Macenski <stevenmacenski@gmail.com> - 1.1.5-1
- Autogenerated by Bloom

* Tue Dec 20 2022 Steve Macenski <stevenmacenski@gmail.com> - 1.1.4-1
- Autogenerated by Bloom

* Tue Nov 08 2022 Steve Macenski <stevenmacenski@gmail.com> - 1.1.3-1
- Autogenerated by Bloom

* Wed Aug 24 2022 Steve Macenski <stevenmacenski@gmail.com> - 1.1.2-1
- Autogenerated by Bloom

* Mon Jun 06 2022 Steve Macenski <stevenmacenski@gmail.com> - 1.1.0-2
- Autogenerated by Bloom

