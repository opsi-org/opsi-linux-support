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
License:        AGPL-3.0+
Group:          Productivity/Networking/Opsi
Version:        1.0
Release:        1
Source:		%{name}_{%version}-{%release}.tar.gz
Summary:        Configure a system to be able to deploy Linux with opsi.
%if %{?suse_version: %{suse_version} >= 1120} %{!?suse_version:1}
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

# ===[ description ]================================
%description
This package configures the system that a deployment
of Linux distributions via opsi is possible

# ===[ prep ]=======================================
%prep

# ===[ setup ]======================================
%setup -n %{name}-%{version}

# ===[ build ]======================================
%build

# ===[ install ]====================================
%install
%if 0%{?suse_version}
mkdir -p $RPM_BUILD_ROOT/etc/opsi/ || true
touch $RPM_BUILD_ROOT/etc/opsi/.shut_up_sles
%endif


# ===[ clean ]======================================
%clean
rm -rf $RPM_BUILD_ROOT

# ===[ post ]=======================================
%post
[ -e "/etc/exports" ] || touch /etc/exports

[ -d "/var/lib/opsi/depot/opsi_nfs_share" ] || mkdir -p "/var/lib/opsi/depot/opsi_nfs_share"

set +e
grep opsi_nfs_share /etc/exports >/dev/null 2>&1
res=$?
set -e
if [ $res -ne 0 ]; then
	echo '/var/lib/opsi/depot/opsi_nfs_share *(ro,no_root_squash,insecure,async,subtree_check,fsid=0)' >> /etc/exports
fi

%if 0%{?centos_version} == 600 || 0%{?rhel_version} == 600 || 0%{?suse_version} == 1110
service nfs restart && showmount -e localhost || echo "Restarting nfs failed. Please check logs."
%else
%if 0%{?suse_version}
service nfsserver restart && showmount -e localhost || echo "Restarting nfsserver failed. Please check logs."
%else
service nfs-server restart && showmount -e localhost || echo "Restarting nfs-server failed. Please check logs."
%endif
%endif

# ===[ files ]======================================
%files

%if 0%{?suse_version}
%defattr(-,root,root)

%config(noreplace) /etc/opsi/.shut_up_sles

%dir /etc/opsi/
%endif

# ===[ changelog ]==================================
%changelog
