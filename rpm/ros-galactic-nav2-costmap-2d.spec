%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/galactic/.*$
%global __requires_exclude_from ^/opt/ros/galactic/.*$

Name:           ros-galactic-nav2-costmap-2d
Version:        1.0.10
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS nav2_costmap_2d package

License:        BSD-3-Clause and Apache-2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-galactic-angles
Requires:       ros-galactic-geometry-msgs
Requires:       ros-galactic-laser-geometry
Requires:       ros-galactic-map-msgs
Requires:       ros-galactic-message-filters
Requires:       ros-galactic-nav-msgs
Requires:       ros-galactic-nav2-msgs
Requires:       ros-galactic-nav2-util
Requires:       ros-galactic-nav2-voxel-grid
Requires:       ros-galactic-pluginlib
Requires:       ros-galactic-rclcpp
Requires:       ros-galactic-rclcpp-lifecycle
Requires:       ros-galactic-sensor-msgs
Requires:       ros-galactic-std-msgs
Requires:       ros-galactic-tf2
Requires:       ros-galactic-tf2-geometry-msgs
Requires:       ros-galactic-tf2-ros
Requires:       ros-galactic-tf2-sensor-msgs
Requires:       ros-galactic-visualization-msgs
Requires:       ros-galactic-ros-workspace
BuildRequires:  ros-galactic-ament-cmake
BuildRequires:  ros-galactic-angles
BuildRequires:  ros-galactic-geometry-msgs
BuildRequires:  ros-galactic-laser-geometry
BuildRequires:  ros-galactic-map-msgs
BuildRequires:  ros-galactic-message-filters
BuildRequires:  ros-galactic-nav-msgs
BuildRequires:  ros-galactic-nav2-common
BuildRequires:  ros-galactic-nav2-msgs
BuildRequires:  ros-galactic-nav2-util
BuildRequires:  ros-galactic-nav2-voxel-grid
BuildRequires:  ros-galactic-pluginlib
BuildRequires:  ros-galactic-rclcpp
BuildRequires:  ros-galactic-rclcpp-lifecycle
BuildRequires:  ros-galactic-sensor-msgs
BuildRequires:  ros-galactic-std-msgs
BuildRequires:  ros-galactic-tf2
BuildRequires:  ros-galactic-tf2-geometry-msgs
BuildRequires:  ros-galactic-tf2-ros
BuildRequires:  ros-galactic-tf2-sensor-msgs
BuildRequires:  ros-galactic-visualization-msgs
BuildRequires:  ros-galactic-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-galactic-ament-cmake-gtest
BuildRequires:  ros-galactic-ament-lint-auto
BuildRequires:  ros-galactic-ament-lint-common
BuildRequires:  ros-galactic-launch
BuildRequires:  ros-galactic-launch-testing
BuildRequires:  ros-galactic-nav2-lifecycle-manager
BuildRequires:  ros-galactic-nav2-map-server
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
if [ -f "/opt/ros/galactic/setup.sh" ]; then . "/opt/ros/galactic/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/galactic" \
    -DAMENT_PREFIX_PATH="/opt/ros/galactic" \
    -DCMAKE_PREFIX_PATH="/opt/ros/galactic" \
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
if [ -f "/opt/ros/galactic/setup.sh" ]; then . "/opt/ros/galactic/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/galactic/setup.sh" ]; then . "/opt/ros/galactic/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/galactic

%changelog
* Mon May 09 2022 Steve Macenski <stevenmacenski@gmail.com> - 1.0.10-1
- Autogenerated by Bloom

* Fri May 06 2022 Steve Macenski <stevenmacenski@gmail.com> - 1.0.9-1
- Autogenerated by Bloom

