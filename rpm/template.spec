%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/iron/.*$
%global __requires_exclude_from ^/opt/ros/iron/.*$

Name:           ros-iron-nav2-constrained-smoother
Version:        1.2.8
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS nav2_constrained_smoother package

License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       ceres-solver-devel
Requires:       flexiblas-devel
Requires:       ros-iron-angles
Requires:       ros-iron-nav2-common
Requires:       ros-iron-nav2-core
Requires:       ros-iron-nav2-costmap-2d
Requires:       ros-iron-nav2-msgs
Requires:       ros-iron-nav2-util
Requires:       ros-iron-pluginlib
Requires:       ros-iron-rclcpp
Requires:       suitesparse-devel
Requires:       ros-iron-ros-workspace
BuildRequires:  ceres-solver-devel
BuildRequires:  flexiblas-devel
BuildRequires:  ros-iron-ament-cmake
BuildRequires:  ros-iron-angles
BuildRequires:  ros-iron-nav2-common
BuildRequires:  ros-iron-nav2-core
BuildRequires:  ros-iron-nav2-costmap-2d
BuildRequires:  ros-iron-nav2-msgs
BuildRequires:  ros-iron-nav2-util
BuildRequires:  ros-iron-pluginlib
BuildRequires:  ros-iron-rclcpp
BuildRequires:  suitesparse-devel
BuildRequires:  ros-iron-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-iron-ament-cmake-gtest
BuildRequires:  ros-iron-ament-cmake-pytest
BuildRequires:  ros-iron-ament-lint-auto
BuildRequires:  ros-iron-ament-lint-common
%endif

%description
Ceres constrained smoother

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
* Thu May 23 2024 Matej Vargovcik <vargovcik@robotechvision.com> - 1.2.8-1
- Autogenerated by Bloom

* Thu Apr 04 2024 Matej Vargovcik <vargovcik@robotechvision.com> - 1.2.7-1
- Autogenerated by Bloom

* Tue Jan 23 2024 Matej Vargovcik <vargovcik@robotechvision.com> - 1.2.6-1
- Autogenerated by Bloom

* Wed Nov 01 2023 Matej Vargovcik <vargovcik@robotechvision.com> - 1.2.5-2
- Autogenerated by Bloom

