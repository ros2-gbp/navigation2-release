%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/jazzy/.*$
%global __requires_exclude_from ^/opt/ros/jazzy/.*$

Name:           ros-jazzy-navigation2
Version:        1.3.6
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS navigation2 package

License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-jazzy-nav2-amcl
Requires:       ros-jazzy-nav2-behavior-tree
Requires:       ros-jazzy-nav2-behaviors
Requires:       ros-jazzy-nav2-bt-navigator
Requires:       ros-jazzy-nav2-collision-monitor
Requires:       ros-jazzy-nav2-constrained-smoother
Requires:       ros-jazzy-nav2-controller
Requires:       ros-jazzy-nav2-core
Requires:       ros-jazzy-nav2-costmap-2d
Requires:       ros-jazzy-nav2-dwb-controller
Requires:       ros-jazzy-nav2-graceful-controller
Requires:       ros-jazzy-nav2-lifecycle-manager
Requires:       ros-jazzy-nav2-map-server
Requires:       ros-jazzy-nav2-mppi-controller
Requires:       ros-jazzy-nav2-msgs
Requires:       ros-jazzy-nav2-navfn-planner
Requires:       ros-jazzy-nav2-planner
Requires:       ros-jazzy-nav2-regulated-pure-pursuit-controller
Requires:       ros-jazzy-nav2-rotation-shim-controller
Requires:       ros-jazzy-nav2-rviz-plugins
Requires:       ros-jazzy-nav2-simple-commander
Requires:       ros-jazzy-nav2-smac-planner
Requires:       ros-jazzy-nav2-smoother
Requires:       ros-jazzy-nav2-theta-star-planner
Requires:       ros-jazzy-nav2-util
Requires:       ros-jazzy-nav2-velocity-smoother
Requires:       ros-jazzy-nav2-voxel-grid
Requires:       ros-jazzy-nav2-waypoint-follower
Requires:       ros-jazzy-opennav-docking
Requires:       ros-jazzy-opennav-docking-bt
Requires:       ros-jazzy-opennav-docking-core
Requires:       ros-jazzy-ros-workspace
BuildRequires:  ros-jazzy-ament-cmake
BuildRequires:  ros-jazzy-ros-workspace
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
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/jazzy" \
    -DAMENT_PREFIX_PATH="/opt/ros/jazzy" \
    -DCMAKE_PREFIX_PATH="/opt/ros/jazzy" \
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
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/jazzy

%changelog
* Tue Apr 15 2025 Steve Macenski <stevenmacenski@gmail.com> - 1.3.6-1
- Autogenerated by Bloom

* Wed Feb 05 2025 Steve Macenski <stevenmacenski@gmail.com> - 1.3.5-1
- Autogenerated by Bloom

* Fri Dec 13 2024 Steve Macenski <stevenmacenski@gmail.com> - 1.3.4-1
- Autogenerated by Bloom

* Fri Nov 08 2024 Steve Macenski <stevenmacenski@gmail.com> - 1.3.3-1
- Autogenerated by Bloom

* Tue Jun 25 2024 Steve Macenski <stevenmacenski@gmail.com> - 1.3.1-1
- Autogenerated by Bloom

* Tue Jun 25 2024 Steve Macenski <stevenmacenski@gmail.com> - 1.3.0-2
- Autogenerated by Bloom

