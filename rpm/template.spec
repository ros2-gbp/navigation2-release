%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/jazzy/.*$
%global __requires_exclude_from ^/opt/ros/jazzy/.*$

Name:           ros-jazzy-nav2-loopback-sim
Version:        1.3.6
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS nav2_loopback_sim package

License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-jazzy-geometry-msgs
Requires:       ros-jazzy-nav-msgs
Requires:       ros-jazzy-rclpy
Requires:       ros-jazzy-tf-transformations
Requires:       ros-jazzy-tf2-ros
Requires:       ros-jazzy-ros-workspace
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  ros-jazzy-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  ros-jazzy-ament-copyright
BuildRequires:  ros-jazzy-ament-flake8
BuildRequires:  ros-jazzy-ament-pep257
%endif

%description
A loopback simulator to replace physics simulation

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
%py3_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
%py3_install -- --prefix "/opt/ros/jazzy"

%if 0%{?with_tests}
%check
# Look for a directory with a name indicating that it contains tests
TEST_TARGET=$(ls -d * | grep -m1 "\(test\|tests\)" ||:)
if [ -n "$TEST_TARGET" ] && %__python3 -m pytest --version; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
%__python3 -m pytest $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/jazzy

%changelog
* Tue Apr 15 2025 steve macenski <steve@opennav.org> - 1.3.6-1
- Autogenerated by Bloom

* Wed Feb 05 2025 steve macenski <steve@opennav.org> - 1.3.5-1
- Autogenerated by Bloom

* Fri Dec 13 2024 steve macenski <steve@opennav.org> - 1.3.4-1
- Autogenerated by Bloom

* Fri Nov 08 2024 steve macenski <steve@opennav.org> - 1.3.3-1
- Autogenerated by Bloom

