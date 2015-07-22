#
# spec file for package opsi-linux-support 
#
# Copyright (c) 2015 uib GmbH.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
Name:           opsi-linux-support
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?fedora_version}
Requires:       nfs-utils
%else
Requires:       nfs-kernel-server
%endif
Url:            http://www.opsi.org
License:        AGPLv3+
Group:          Productivity/Networking/Opsi
Version:        1.0
Release:        1
Source:		%{name}_{%version}-{%release}.tar.gz
Summary:        Configure a system to be able to deploy Linux with opsi.
%if %{?suse_version: %{suse_version} >= 1120} %{!?suse_version:1}
BuildArch:      noarch
%endif

# ===[ description ]================================
%description
This package configures the system that a deployment
of Linux distributions via opsi is possible.

# ===[ prep ]=======================================
%prep

# ===[ setup ]======================================
%setup -n %{name}-%{version}

# ===[ build ]======================================
%build

# ===[ install ]====================================
%install
%if %{?suse_version}
mkdir -p $RPM_BUILD_ROOT/etc/opsi/ || true
touch $RPM_BUILD_ROOT/etc/opsi/.shut_up_sles
%endif


# ===[ clean ]======================================
%clean
rm -rf $RPM_BUILD_ROOT

# ===[ post ]=======================================
%post
[ -e "/etc/exports" ] || touch /etc/exports

set +e
grep opsi_nfs_share /etc/exports >/dev/null 2>&1
res=$?
set -e
if [ $res -ne 0 ]; then
	echo '/var/lib/opsi/depot/opsi_nfs_share *(ro,no_root_squash,insecure,async,subtree_check,fsid=0)' >> /etc/exports
fi 

# ===[ files ]======================================
%files

%if %{?suse_version}
%config(noreplace) /etc/opsi/.shut_up_sles
%endif

# ===[ changelog ]==================================
%changelog
