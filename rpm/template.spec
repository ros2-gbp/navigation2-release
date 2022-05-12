%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/galactic/.*$
%global __requires_exclude_from ^/opt/ros/galactic/.*$

Name:           ros-galactic-nav2-waypoint-follower
Version:        1.0.11
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS nav2_waypoint_follower package

License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-galactic-cv-bridge
Requires:       ros-galactic-image-transport
Requires:       ros-galactic-nav-msgs
Requires:       ros-galactic-nav2-common
Requires:       ros-galactic-nav2-core
Requires:       ros-galactic-nav2-msgs
Requires:       ros-galactic-nav2-util
Requires:       ros-galactic-pluginlib
Requires:       ros-galactic-rclcpp
Requires:       ros-galactic-rclcpp-action
Requires:       ros-galactic-rclcpp-lifecycle
Requires:       ros-galactic-tf2-ros
Requires:       ros-galactic-ros-workspace
BuildRequires:  ros-galactic-ament-cmake
BuildRequires:  ros-galactic-cv-bridge
BuildRequires:  ros-galactic-image-transport
BuildRequires:  ros-galactic-nav-msgs
BuildRequires:  ros-galactic-nav2-common
BuildRequires:  ros-galactic-nav2-core
BuildRequires:  ros-galactic-nav2-msgs
BuildRequires:  ros-galactic-nav2-util
BuildRequires:  ros-galactic-pluginlib
BuildRequires:  ros-galactic-rclcpp
BuildRequires:  ros-galactic-rclcpp-action
BuildRequires:  ros-galactic-rclcpp-lifecycle
BuildRequires:  ros-galactic-tf2-ros
BuildRequires:  ros-galactic-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-galactic-ament-cmake-gtest
BuildRequires:  ros-galactic-ament-cmake-pytest
BuildRequires:  ros-galactic-ament-lint-auto
BuildRequires:  ros-galactic-ament-lint-common
%endif

%description
A waypoint follower navigation server

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
* Thu May 12 2022 Steve Macenski <stevenmacenski@gmail.com> - 1.0.11-1
- Autogenerated by Bloom

* Mon May 09 2022 Steve Macenski <stevenmacenski@gmail.com> - 1.0.10-1
- Autogenerated by Bloom

* Fri May 06 2022 Steve Macenski <stevenmacenski@gmail.com> - 1.0.9-1
- Autogenerated by Bloom

