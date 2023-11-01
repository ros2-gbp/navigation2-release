%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/iron/.*$
%global __requires_exclude_from ^/opt/ros/iron/.*$

Name:           ros-iron-navigation2
Version:        1.2.5
Release:        2%{?dist}%{?release_suffix}
Summary:        ROS navigation2 package

License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-iron-nav2-amcl
Requires:       ros-iron-nav2-behavior-tree
Requires:       ros-iron-nav2-behaviors
Requires:       ros-iron-nav2-bt-navigator
Requires:       ros-iron-nav2-collision-monitor
Requires:       ros-iron-nav2-constrained-smoother
Requires:       ros-iron-nav2-controller
Requires:       ros-iron-nav2-core
Requires:       ros-iron-nav2-costmap-2d
Requires:       ros-iron-nav2-dwb-controller
Requires:       ros-iron-nav2-lifecycle-manager
Requires:       ros-iron-nav2-map-server
Requires:       ros-iron-nav2-mppi-controller
Requires:       ros-iron-nav2-msgs
Requires:       ros-iron-nav2-navfn-planner
Requires:       ros-iron-nav2-planner
Requires:       ros-iron-nav2-regulated-pure-pursuit-controller
Requires:       ros-iron-nav2-rotation-shim-controller
Requires:       ros-iron-nav2-rviz-plugins
Requires:       ros-iron-nav2-simple-commander
Requires:       ros-iron-nav2-smac-planner
Requires:       ros-iron-nav2-smoother
Requires:       ros-iron-nav2-theta-star-planner
Requires:       ros-iron-nav2-util
Requires:       ros-iron-nav2-velocity-smoother
Requires:       ros-iron-nav2-voxel-grid
Requires:       ros-iron-nav2-waypoint-follower
Requires:       ros-iron-ros-workspace
BuildRequires:  ros-iron-ament-cmake
BuildRequires:  ros-iron-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
ROS2 Navigation Stack

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/iron" \
    -DAMENT_PREFIX_PATH="/opt/ros/iron" \
    -DCMAKE_PREFIX_PATH="/opt/ros/iron" \
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
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/iron

%changelog
* Wed Nov 01 2023 Steve Macenski <stevenmacenski@gmail.com> - 1.2.5-2
- Autogenerated by Bloom

