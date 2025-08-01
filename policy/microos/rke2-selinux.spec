# vim: sw=4:ts=4:et

%define rke2_relabel_files() \
umask 0022; \
mkdir -p /etc/cni; \
mkdir -p /opt/cni; \
mkdir -p /var/lib/cni; \
mkdir -p /var/lib/kubelet; \
mkdir -p /var/lib/rancher/rke2/data; \
mkdir -p /var/run/flannel; \
umask 0027; \
mkdir -p /var/lib/kubelet/pods; \
mkdir -p /var/lib/rancher/rke2/agent; \
umask 0066; \
mkdir -p /var/run/k3s; \
umask 0077; \
mkdir -p /var/lib/rancher/rke2/agent/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots; \
mkdir -p /var/lib/rancher/rke2/server; \
restorecon -R -i /etc/systemd/system/rke2*; \
restorecon -R -i /usr/lib/systemd/system/rke2*; \
restorecon -R /var/lib/cni; \
restorecon -R /opt/cni; \
restorecon -R /etc/cni; \
restorecon -R /var/lib/kubelet; \
restorecon -R /var/lib/rancher; \
restorecon -R /var/run/k3s; \
restorecon -R /var/run/flannel

%define selinux_policyver 20210716-3.1
%define container_policyver 2.164.2-1.1

Name:       rke2-selinux
Version:    %{rke2_selinux_version}
Release:    %{rke2_selinux_release}.sle
Summary:    SELinux policy module for rke2

Group:      System Environment/Base
License:    Apache-2.0
URL:        https://rke2.io
Source0:    rke2.pp
Source1:    rke2.if

BuildArch:      noarch
BuildRequires:  container-selinux >= %{container_policyver}
BuildRequires:  git
BuildRequires:  selinux-policy >= %{selinux_policyver}
BuildRequires:  selinux-policy-devel >= %{selinux_policyver}

Requires: policycoreutils, selinux-tools
Requires(post): selinux-policy-base >= %{selinux_policyver}
Requires(post): policycoreutils
Requires(post): container-selinux >= %{container_policyver}
Requires(postun): policycoreutils

Provides: %{name} = %{version}-%{release}
Obsoletes: rke2-selinux < 0.9
Conflicts: k3s-selinux

%description
This package installs and sets up the SELinux policy security module for rke2.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}/etc/selinux/targeted/contexts/users/

%pre
%selinux_relabel_pre

%post
semodule -n -i %{_datadir}/selinux/packages/rke2.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %rke2_relabel_files
fi;

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall rke2
fi;

%posttrans
%selinux_relabel_post

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/rke2.pp
%{_datadir}/selinux/devel/include/contrib/rke2.if

%changelog
