%global             cbq_version v0.7.3

%define rpmversion 4.11.0
%define baserelease 0.el7
%define specrelease 14%{?dist}
%define pkg_release %{specrelease}%{?buildid}

Summary:            Advanced IP routing and network device configuration tools
Name:               iproute
Version:            %{rpmversion}
Release:            %{pkg_release}
Group:              Applications/System
URL:                http://kernel.org/pub/linux/utils/net/%{name}2/
Source0:            %{name}-%{rpmversion}-%{baserelease}.tar.xz
Source1:            cbq-0000.example
Source2:            avpkt
Source3:            rt_dsfield.deprecated
Patch0:             0001-Confirm-success-for-each-tc-batch-command.patch
Patch1:             0002-Really-fix-get_addr-and-get_prefix-error-messages.patch
Patch2:             0003-tc-simple-Fix-documentation.patch
Patch3:             0004-tc-fix-m_simple-usage.patch
Patch4:             0005-bpf-Make-bytecode-file-reading-a-little-more-robust.patch
Patch5:             0006-ss-Fix-for-added-diag-support-check.patch
Patch6:             0007-tc-simple.8-Fix-reference-to-non-existing-tc-actions.patch
Patch7:             0008-lib-bpf-Fix-bytecode-file-parsing.patch
Patch8:             0009-tc-simple.8-Fix-one-more-reference-to-non-existing-t.patch
Patch9:             0010-tc-m_xt-Prevent-a-segfault-in-libipt.patch
Patch10:            0011-link_gre6-really-support-encaplimit-option.patch
Patch11:            0012-tc-fix-typo-in-manpage.patch
Patch12:            0013-ip-neigh-allow-flush-FAILED-neighbour-entry.patch
Patch13:            0014-netns-avoid-directory-traversal.patch
Patch14:            0015-utils-return-default-family-when-rtm_family-is-not-R.patch
Patch15:            0016-link_gre6-Fix-for-changing-tclass-flowlabel.patch
Patch16:            0017-netlink-Change-rtnl_dump_done-to-always-show-error.patch
Patch17:            0018-libnetlink-drop-unused-parameter-to-rtnl_dump_done.patch
Patch18:            0019-iproute-Add-support-for-extended-ack-to-rtnl_talk.patch
Patch19:            0020-iplink-check-for-message-truncation-in-iplink_get.patch
Patch20:            0021-iplink-double-the-buffer-size-also-in-iplink_get.patch
Patch21:            0022-lib-libnetlink-re-malloc-buff-if-size-is-not-enough.patch
Patch22:            0023-lib-libnetlink-update-rtnl_talk-to-support-malloc-bu.patch
Patch23:            0024-Update-linux-headers.patch
Patch24:            0025-devlink-Change-netlink-attribute-validation.patch
Patch25:            0026-devlink-Add-support-for-pipeline-debug-dpipe.patch
Patch26:            0027-tc-Reflect-HW-offload-status.patch
Patch27:            0028-pedit-Fix-a-typo-in-warning.patch
Patch28:            0029-pedit-Do-not-allow-using-retain-for-too-big-fields.patch
Patch29:            0030-pedit-Check-for-extended-capability-in-protocol-pars.patch
Patch30:            0031-pedit-Introduce-ipv6-support.patch
Patch31:            0032-devlink-Add-option-to-set-and-show-eswitch-encapsula.patch
Patch32:            0033-tc-flower-add-support-for-tcp-flags.patch
Patch33:            0034-iplink-Update-usage-in-help-message.patch
Patch34:            0035-tc-flower-add-support-for-matching-on-ip-tos-and-ttl.patch
Patch35:            0036-iproute-build-more-easily-on-Android.patch
Patch36:            0037-uapi-add-include-linux-vm_sockets_diag.h.patch
Patch37:            0038-ss-allow-AF_FAMILY-constants-32.patch
Patch38:            0039-ss-add-AF_VSOCK-support.patch
Patch39:            0040-link_gre6-Detect-invalid-encaplimit-values.patch
Patch40:            0041-man-tc-csum.8-Fix-inconsistency-in-example-descripti.patch
Patch41:            0042-tc-fix-command-tc-actions-del-hang-issue.patch
Patch42:            0043-ip-link-Fix-use-after-free-in-nl_get_ll_addr_len.patch
License:            GPLv2+ and Public Domain
BuildRequires:      bison
BuildRequires:      flex
BuildRequires:      iptables-devel >= 1.4.5
BuildRequires:      libdb-devel
BuildRequires:      libmnl-devel
BuildRequires:      libselinux-devel
BuildRequires:      linuxdoc-tools
BuildRequires:      pkgconfig
BuildRequires:      psutils
BuildRequires:      tex(cm-super-t1.enc)
BuildRequires:      tex(dvips)
BuildRequires:      tex(ecrm1000.tfm)
BuildRequires:      tex(latex)
BuildRequires:      tex(fullpage.sty)
%if 0%{?fedora}
BuildRequires:      linux-atm-libs-devel
%endif
# For the UsrMove transition period
Conflicts:          filesystem < 3
Provides:           /sbin/ip

%description
The iproute package contains networking utilities (ip and rtmon, for example)
which are designed to use the advanced networking capabilities of the Linux
kernel.

%package doc
Summary:            ip and tc documentation with examples
Group:              Applications/System
License:            GPLv2+
Requires:           %{name} = %{version}-%{release}

%description doc
The iproute documentation contains howtos and examples of settings.

%package devel
Summary:            iproute development files
Group:              Development/Libraries
License:            GPLv2+
Requires:           %{name} = %{version}-%{release}
Provides:           iproute-static = %{version}-%{release}

%description devel
The libnetlink static library.

%prep
%autosetup -p1 -n %{name}-%{version}-%{baserelease}
sed -i 's/iproute-doc/%{name}-%{version}/' man/man8/lnstat.8

%build
export LIBDIR=/%{_libdir}
export IPT_LIB_DIR=/%{_lib}/xtables
export CFLAGS="${CFLAGS:-%optflags} -fno-exceptions"
./configure
make %{?_smp_mflags}
make -C doc

%install
export SBINDIR=%{_sbindir}
export MANDIR=%{_mandir}
export LIBDIR=%{_libdir}
export CONFDIR=%{_sysconfdir}/iproute2
export DOCDIR=%{_docdir}
%make_install
# libnetlink for iproute-devel
install -m644 include/libnetlink.h %{buildroot}%{_includedir}
install -m644 lib/libnetlink.a %{buildroot}%{_libdir}
# RHEL7 ships cbq tool in standard location
install -m755 examples/cbq.init-%{cbq_version} %{buildroot}%{_sbindir}/cbq
echo '.so man8/tc-cbq.8' > %{buildroot}%{_mandir}/man8/cbq.8
install -d -m755 %{buildroot}%{_sysconfdir}/sysconfig/cbq
install -m644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/cbq
# These man pages are missing in respective Makefile
for manpage in genl ifcfg ip-vrf; do
	install -m644 man/man8/${manpage}.8 %{buildroot}%{_mandir}/man8
done
# files in here are extracted manually from %{_builddir}
rm -rf %{buildroot}%{_docdir}
# RHEL7 does not support TIPC so remove tipc tool and its man pages
rm -f %{buildroot}%{_sbindir}/tipc
rm -rf %{buildroot}%{_mandir}/man8/tipc*
# Append deprecated values to rt_dsfield for compatibility reasons
cat %{SOURCE3} >>%{buildroot}%{_sysconfdir}/iproute2/rt_dsfield

%files
%dir %{_sysconfdir}/iproute2
%doc COPYING
%doc README README.decnet README.iproute2+tc README.distribution README.lnstat
%{_mandir}/man7/*
%{_mandir}/man8/*
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/iproute2/*
%{_sbindir}/*
%dir %{_libdir}/tc/
%{_libdir}/tc/*
%dir %{_sysconfdir}/sysconfig/cbq
%config(noreplace) %{_sysconfdir}/sysconfig/cbq/*
%{_datadir}/bash-completion/completions/tc

%files doc
%doc COPYING
%doc doc/*.ps
%doc examples

%files devel
%doc COPYING
%{_mandir}/man3/*
%{_libdir}/libnetlink.a
%{_includedir}/libnetlink.h
%{_includedir}/iproute2/bpf_elf.h

%changelog
* Tue Mar 06 2018 Phil Sutter <psutter@redhat.com> [4.11.0-14.el7]
- ip-link: Fix use after free in nl_get_ll_addr_len() (Phil Sutter) [1550097]

* Fri Dec 15 2017 Phil Sutter <psutter@redhat.com> [4.11.0-13.el7]
- tc: fix command "tc actions del" hang issue (Phil Sutter) [1526394]

* Wed Dec 06 2017 Phil Sutter <psutter@redhat.com> [4.11.0-12.el7]
- man: tc-csum.8: Fix inconsistency in example description (Phil Sutter) [1417162]
- link_gre6: Detect invalid encaplimit values (Phil Sutter) [1459600]

* Mon Nov 13 2017 Phil Sutter <psutter@redhat.com> [4.11.0-11.el7]
- ss: add AF_VSOCK support (Stefano Brivio) [1472759]
- ss: allow AF_FAMILY constants >32 (Stefano Brivio) [1472759]
- uapi: add include linux/vm_sockets_diag.h (Stefano Brivio) [1472759]
- iproute: build more easily on Android (Phil Sutter) [1472759]

* Fri Nov 10 2017 Phil Sutter <psutter@redhat.com> [4.11.0-10.el7]
- tc: flower: add support for matching on ip tos and ttl (Kamal Heib) [1456539]
- iplink: Update usage in help message (Kamal Heib) [1456539]
- tc: flower: add support for tcp flags (Kamal Heib) [1456539]
- devlink: Add option to set and show eswitch encapsulation support (Kamal Heib) [1456539]
- pedit: Introduce ipv6 support (Kamal Heib) [1456539]
- pedit: Check for extended capability in protocol parser (Kamal Heib) [1456539]
- pedit: Do not allow using retain for too big fields (Kamal Heib) [1456539]
- pedit: Fix a typo in warning (Kamal Heib) [1456539]
- tc: Reflect HW offload status (Kamal Heib) [1456539]
- devlink: Add support for pipeline debug (dpipe) (Kamal Heib) [1456539]
- devlink: Change netlink attribute validation (Kamal Heib) [1456539]
- Update linux headers (Phil Sutter) [1456539]

* Wed Nov 08 2017 Phil Sutter <psutter@redhat.com> [4.11.0-9.el7]
- lib/libnetlink: update rtnl_talk to support malloc buff at run time (Hangbin Liu) [1380803]
- lib/libnetlink: re malloc buff if size is not enough (Hangbin Liu) [1380803]
- iplink: double the buffer size also in iplink_get() (Hangbin Liu) [1380803]
- iplink: check for message truncation in iplink_get() (Hangbin Liu) [1380803]
- iproute: Add support for extended ack to rtnl_talk (Hangbin Liu) [1380803]
- libnetlink: drop unused parameter to rtnl_dump_done (Hangbin Liu) [1380803]
- netlink: Change rtnl_dump_done to always show error (Hangbin Liu) [1380803]

* Fri Oct 20 2017 Phil Sutter <psutter@redhat.com> [4.11.0-8.el7]
- Fix subpackage dependencies (don't require base package ARCH) (Phil Sutter) [1489548]

* Wed Oct 18 2017 Phil Sutter <psutter@redhat.com> [4.11.0-7.el7]
- Make sub-packages depend on base package (Phil Sutter) [1489548]

* Fri Oct 06 2017 Phil Sutter <psutter@redhat.com> [4.11.0-6.el7]
- link_gre6: Fix for changing tclass/flowlabel (Phil Sutter) [1487486]
- utils: return default family when rtm_family is not RTNL_FAMILY_IPMR/IP6MR (Stefano Brivio) [1475762]
- netns: avoid directory traversal (Phil Sutter) [1468529]
- Disable -fexceptions CFLAG passed by build system (Phil Sutter) [1418715]

* Thu Sep 28 2017 Phil Sutter <psutter@redhat.com> [4.11.0-5.el7]
- ip neigh: allow flush FAILED neighbour entry (Matteo Croce) [1469945]
- tc: fix typo in manpage (Phil Sutter) [1417162]
- link_gre6: really support encaplimit option (Phil Sutter) [1459600]
- tc: m_xt: Prevent a segfault in libipt (Phil Sutter) [1465599]

* Wed Sep 06 2017 Phil Sutter <psutter@redhat.com> [4.11.0-4.el7]
- tc-simple.8: Fix one more reference to non-existing tc-actions.8 (Phil Sutter) [1477523]

* Wed Sep 06 2017 Phil Sutter <psutter@redhat.com> [4.11.0-3.el7]
- lib/bpf: Fix bytecode-file parsing (Phil Sutter) [1477491]
- tc-simple.8: Fix reference to non-existing tc-actions.8 (Phil Sutter) [1477523]
- ss: Fix for added diag support check (Phil Sutter) [1487152]

* Fri Aug 11 2017 Phil Sutter <psutter@redhat.com> [4.11.0-2.el7]
- rt_dsfield: Ship deprecated values for compatibility (Phil Sutter) [1480136]
- bpf: Make bytecode-file reading a little more robust (Phil Sutter) [1477491]
- tc: fix m_simple usage (Phil Sutter) [1477523]
- tc-simple: Fix documentation (Phil Sutter) [1477523]
- Really fix get_addr() and get_prefix() error messages (Phil Sutter) [1477206]

* Tue Jun 27 2017 Phil Sutter <psutter@redhat.com> [4.11.0-1.el7]
- Rebase onto upstream version 4.11.0 (Phil Sutter) [1418715]

* Tue Jun 13 2017 Sabrina Dubroca <sdubroca@redhat.com> [3.10.0-87.el7]
- devlink: Add e-switch support (Sabrina Dubroca) [1459772]
- devlink: whitespace cleanup (Sabrina Dubroca) [1459772]
- devlink: Convert conditional in dl_argv_handle_port() to switch() (Sabrina Dubroca) [1459772]
- devlink: write usage help messages to stderr (Sabrina Dubroca) [1459772]
- devlink: Add usage help for eswitch subcommand (Sabrina Dubroca) [1459772]
- devlink: Call dl_free in early exit case (Sabrina Dubroca) [1459772]

* Mon Jun 12 2017 Eric Garver <egarver@redhat.com> [3.10.0-86.el7]
- Revert "ip-route man: add usage and description for lwtunnel encap attributes" (Eric Garver) [1459975]
- Revert "lwtunnel: implement support for ip6 encap" (Eric Garver) [1459975]
- Revert "lwtunnel: fix argument parsing" (Eric Garver) [1459975]
- Revert "lwtunnel: Add encapsulation support to ip route" (Eric Garver) [1459975]

* Mon Jun 12 2017 Eric Garver <egarver@redhat.com> [3.10.0-85.el7]
- Revert "vxlan: Add support for remote checksum offload" (Eric Garver) [1459975]

* Wed May 31 2017 Ivan Vecera <ivecera@redhat.com> [3.10.0-84.el7]
- tc: Add support for the matchall traffic classifier. (Ivan Vecera) [1435624]
- tc: man: Add man entry for the matchall classifier. (Ivan Vecera) [1435624]
- tc: add missing limits.h header (Ivan Vecera) [1435624]
- tc: man: matchall: Fix example indentation (Ivan Vecera) [1435624]
- tc: matchall: Print skip flags when dumping a filter (Ivan Vecera) [1435624]
- tc, clsact: add clsact frontend (Ivan Vecera) [1435624]

* Thu May 18 2017 Phil Sutter <psutter@redhat.com> [3.10.0-83.el7]
- vxlan: Add support for remote checksum offload (Phil Sutter) [1446363]

* Thu Apr 20 2017 Phil Sutter <psutter@redhat.com> [3.10.0-82.el7]
- ip-route: Prevent some other double spaces in output (Phil Sutter) [1374446]

* Wed Apr 05 2017 Phil Sutter <psutter@redhat.com> [3.10.0-81.el7]
- man: ip-link: Specify min/max values for bridge slave priority and cost (Phil Sutter) [1374360]
- man: ip-link.8: document bridge options (Phil Sutter) [1373869]

* Tue Apr 04 2017 Phil Sutter <psutter@redhat.com> [3.10.0-80.el7]
- tc: m_xt: Drop needless parentheses from #if checks (Phil Sutter) [1326726]
- tc: m_xt: Fix segfault with iptables-1.6.0 (Phil Sutter) [1326726]
- m_xt: whitespace cleanup (Phil Sutter) [1326726]
- tc: m_xt: Introduce get_xtables_target_opts() (Phil Sutter) [1326726]
- tc: m_xt: Simplify argc adjusting in parse_ipt() (Phil Sutter) [1326726]
- tc: m_xt: Get rid of iargc variable in parse_ipt() (Phil Sutter) [1326726]
- tc: m_xt: Get rid of rargc in parse_ipt() (Phil Sutter) [1326726]
- tc: m_xt: Drop unused variable fw in parse_ipt() (Phil Sutter) [1326726]
- tc: m_xt: Get rid of one indentation level in parse_ipt() (Phil Sutter) [1326726]
- tc: m_xt: Fix indenting (Phil Sutter) [1326726]
- tc: m_xt: Fix segfault when adding multiple actions at once (Phil Sutter) [1326726]
- tc: m_xt: Prevent segfault with standard targets (Phil Sutter) [1326726]
- man: update doc after support of ESN and anti-replay window (Phil Sutter) [1425059]
- xfrm: add support of ESN and anti-replay window (Phil Sutter) [1425059]

* Fri Mar 17 2017 Phil Sutter <psutter@redhat.com> [3.10.0-79.el7]
- man: ss.8: Add missing protocols to description of -A (Phil Sutter) [1063934]

* Fri Mar 17 2017 Phil Sutter <psutter@redhat.com> [3.10.0-78.el7]
- ip-address: Support filtering by slave type, too (Phil Sutter) [1375434]
- tc: don't accept qdisc 'handle' greater than ffff (Davide Caratti) [1375393]
- macsec: show usage even if the module is not available (Timothy Redaelli) [1367071]
- libgenl: introduce genl_init_handle (Timothy Redaelli) [1367071]
- tc: flower: Fix parsing ip address (Phil Sutter) [1422629]
- tc: flower: support masked ICMP code and type match (Phil Sutter) [1422629]
- tc: flower: provide generic masked u8 print helper (Phil Sutter) [1422629]
- tc: flower: provide generic masked u8 parser helper (Phil Sutter) [1422629]
- tc: flower: Update documentation to indicate ARP takes IPv4 prefixes (Phil Sutter) [1422629]
- tc: flower: use correct type when calling flower_icmp_attr_type (Phil Sutter) [1422629]
- f_flower: don't set TCA_FLOWER_KEY_ETH_TYPE for "protocol all" (Phil Sutter) [1422629]
- tc: flower: Refactor matching flags to be more user friendly (Phil Sutter) [1422629]
- tc: flower: Support matching ARP (Phil Sutter) [1422629]
- kernel headers update (Phil Sutter) [1422629]
- tc: flower: Fix incorrect error msg about eth type (Phil Sutter) [1422629]
- tc: flower: Add missing err check when parsing flower options (Phil Sutter) [1422629]
- tc: flower: Fix flower output for src and dst ports (Phil Sutter) [1422629]
- tc: flower: Update dest UDP port documentation (Phil Sutter) [1422629]
- tc: flower: support matching flags (Phil Sutter) [1422629]
- tc/cls_flower: Add to the usage encapsulation dest UDP port (Phil Sutter) [1422629]
- tc: flower: Allow *_mac options to accept a mask (Phil Sutter) [1422629]
- tc: flower: document that *_ip parameters take a PREFIX as an argument. (Phil Sutter) [1422629]
- tc: flower: Fix typo and style in flower man page (Phil Sutter) [1422629]
- tc/cls_flower: Add dest UDP port to tunnel params (Phil Sutter) [1422629]
- tc: flower: support matching on ICMP type and code (Phil Sutter) [1422629]
- tc: flower: introduce enum flower_endpoint (Phil Sutter) [1422629]
- tc: flower: make use of flower_port_attr_type() safe and silent (Phil Sutter) [1422629]
- tc: flower: correct name of ip_proto parameter to flower_parse_port() (Phil Sutter) [1422629]
- tc: flower: document SCTP ip_proto (Phil Sutter) [1422629]
- tc: flower: remove references to eth_type in manpage (Phil Sutter) [1422629]
- tc/cls_flower: Classify packet in ip tunnels (Phil Sutter) [1422629]
- libnetlink: Introduce rta_getattr_be*() (Phil Sutter) [1422629]
- tc: flower: Support matching on SCTP ports (Phil Sutter) [1422629]
- tc: flower: Fix usage message (Phil Sutter) [1422629]
- tc: flower checkpatch cleanups (Phil Sutter) [1422629]
- tc: flower: Introduce vlan support (Phil Sutter) [1422629]
- tc: flower: Add skip_{hw|sw} support (Phil Sutter) [1422629]
- utils: add get_be{16, 32, 64}, use them where possible (Phil Sutter) [1422629]
- lib/utils: introduce rt_addr_n2a_rta() (Phil Sutter) [1422629]
- utils: make rt_addr_n2a() non-reentrant by default (Phil Sutter) [1422629]
- make format_host non-reentrant by default (Phil Sutter) [1422629]
- tc: flower no need to specify the ethertype (Phil Sutter) [1422629]
- ip6tunnel: print local/remote addresses like iptunnel does (Phil Sutter) [1422629]
- tc: ship filter man pages and refer to them in tc.8 (Phil Sutter) [1422629]
- tc: add a man page for flower filter (Phil Sutter) [1422629]
- tc: improve filter help texts a bit (Phil Sutter) [1422629]
- tc: add support for Flower classifier (Phil Sutter) [1422629]
- ip: make -resolve addr to print names rather than addresses (Phil Sutter) [1422629]

* Tue Feb 28 2017 Phil Sutter <psutter@redhat.com> [3.10.0-77.el7]
- change of rtnetlink to use RTN_F_OFFLOAD (Phil Sutter) [1417289]
- bridge: add support for the multicast flood flag (Phil Sutter) [1417289]
- RH-INTERNAL: Update kernel headers to v4.10.0 (Phil Sutter) [1417289]
- bridge: man: fix STP LISTENING description (Phil Sutter) [1417289]
- bridge: man: fix BPUD typo (Phil Sutter) [1417289]
- bridge: man: fix "brige" typo (Phil Sutter) [1417289]
- bridge: vlan: fix a few "fdb" typos in vlan doc (Phil Sutter) [1417289]
- bridge: vlan: add support to filter by vlan id (Phil Sutter) [1417289]
- bridge: mdb: add support to filter by vlan id (Phil Sutter) [1417289]
- bridge: fdb: add support to filter by vlan id (Phil Sutter) [1417289]
- bridge: code cleanup (Phil Sutter) [1417289]
- bridge: mdb: add support for extended router port information (Phil Sutter) [1417289]
- bridge: mdb: add support for offloaded mdb entries (Phil Sutter) [1417289]
- bridge: mdb: add user-space support for extended attributes (Phil Sutter) [1417289]
- iplink: bridge: remove unnecessary returns (Phil Sutter) [1417289]
- bridge: add support for dynamic fdb entries (Phil Sutter) [1417289]
- iplink: bridge_slave: export read-only values (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_MCAST_STARTUP_QUERY_INTVL (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_MCAST_QUERY_RESPONSE_INTVL (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_MCAST_QUERY_INTVL (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_MCAST_QUERIER_INTVL (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_MCAST_MEMBERSHIP_INTVL (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_MCAST_LAST_MEMBER_INTVL (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_MCAST_STARTUP_QUERY_CNT (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_MCAST_LAST_MEMBER_CNT (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_MCAST_HASH_MAX (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_MCAST_HASH_ELASTICITY (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_MCAST_QUERIER (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_MCAST_QUERY_USE_IFADDR (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_MCAST_SNOOPING (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_MCAST_ROUTER (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_VLAN_DEFAULT_PVID (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_GROUP_ADDR (Phil Sutter) [1417289]
- iplink: bridge: add support for IFLA_BR_GROUP_FWD_MASK (Phil Sutter) [1417289]
- iplink: bridge: export read-only timers (Phil Sutter) [1417289]
- iplink: bridge: export root_(port|path_cost), topology_change and change_detected (Phil Sutter) [1417289]
- iplink: bridge: export bridge_id and designated_root (Phil Sutter) [1417289]
- bridge: support for static fdb entries (Phil Sutter) [1417289]
- bridge.8: minor formatting cleanup (Phil Sutter) [1417289]
- bridge.8: document fdb replace command (Phil Sutter) [1417289]
- bridge: fdb: minor syntax fix in help text (Phil Sutter) [1417289]
- bridge: add calls to fflush in fdb and mdb print functions (Phil Sutter) [1417289]
- ip, bridge: document -timestamp option (Phil Sutter) [1417289]
- bridge: add batch command support (Phil Sutter) [1417289]
- iplink: Add support for IFLA_BR_VLAN_PROTOCOL attribute (Phil Sutter) [1417289]
- iplink: add support for IFLA_BR_VLAN_FILTERING attribute (Phil Sutter) [1417289]
- bridge: mdb: add deleted when monitoring delmdb event (Phil Sutter) [1417289]
- bridge: mdb: add support for vlans (Phil Sutter) [1417289]
- ip link: proto_down config and display. (Phil Sutter) [1417289]
- bridge: mdb: add support for router add/del notifications monitoring (Phil Sutter) [1417289]
- ip: fix all the checkpatch warnings (Phil Sutter) [1417289]
- iproute2: ipa: show switch id (Phil Sutter) [1417289]
- ip: return correct exit code on route failure (Phil Sutter) [1417289]
- iproute2: unify naming for entries offloaded to hardware (Phil Sutter) [1417289]
- route: label externally offloaded routes (Phil Sutter) [1417289]
- fix ip -force -batch to continue on errors (Phil Sutter) [1417289]
- bridge link: add support to specify master (Phil Sutter) [1417289]
- Allow specifying bridge port STP state by name rather than number. (Phil Sutter) [1417289]
- iproute2: bridge vlan show new option to print ranges (Phil Sutter) [1417289]
- iproute2: bridge: support vlan range adds (Phil Sutter) [1417289]
- bridge/link: add learning_sync policy flag (Phil Sutter) [1417289]
- bridge link: add option 'self' (Phil Sutter) [1417289]
- bridge/fdb: add flag/indication for FDB entry synced from offload device (Phil Sutter) [1417289]
- bridge/fdb: fix statistics output spacing (Phil Sutter) [1417289]
- iproute2 bridge: bring to above par with brctl show macs (Phil Sutter) [1417289]
- link dump filter (Phil Sutter) [1417289]
- bridge: Make filter_index match in signedness (Phil Sutter) [1417289]
- bridge: Add learning and flood support (Phil Sutter) [1417289]
- iproute2: ipa: show port id (Phil Sutter) [1417289]
- bridge: fix reporting of IPv6 addresses (Phil Sutter) [1417289]
- iplink: bridge_slave: add support for IFLA_BRPORT_PROXYARP_WIFI (Phil Sutter) [1374360]
- iplink: bridge_slave: add support for IFLA_BRPORT_PROXYARP (Phil Sutter) [1374360]
- Revert "man: ip-link: Remove bits about proxy_arp and proxy_arp_wifi" (Phil Sutter) [1374360]

* Tue Feb 21 2017 Phil Sutter <psutter@redhat.com> [3.10.0-76.el7]
- iplink: add missing link type (Phil Sutter) [1374493]
- man: ip-link: Remove bits about proxy_arp and proxy_arp_wifi (Phil Sutter) [1374360]
- iplink: bridge_slave: add support for IFLA_BRPORT_FAST_LEAVE (Phil Sutter) [1374360]
- iplink: bridge_slave: add support for IFLA_BRPORT_MULTICAST_ROUTER (Phil Sutter) [1374360]
- macsec: fix input range of 'icvlen' parameter (Phil Sutter) [1373121]

* Tue Feb 21 2017 Phil Sutter <psutter@redhat.com> [3.10.0-75.el7]
- ip: vfinfo: remove code duplication for IFLA_VF_RSS_QUERY_EN (Timothy Redaelli) [1264149]
- ipaddress: Print IFLA_VF_QUERY_RSS_EN setting (Timothy Redaelli) [1264149]
- ipaddress: Simplify vf_info parsing (Timothy Redaelli) [1264149]
- ip-route: Prevent some double spaces in output (Timothy Redaelli) [1374446]
- ip-route man: add usage and description for lwtunnel encap attributes (Phil Sutter) [1329730]
- lwtunnel: implement support for ip6 encap (Phil Sutter) [1329730]
- lwtunnel: fix argument parsing (Phil Sutter) [1329730]
- lwtunnel: Add encapsulation support to ip route (Phil Sutter) [1329730]
- libnetlink: introduce rta_nest and u8, u16, u64 helpers for nesting within rtattr (Phil Sutter) [1329730]
- utils: add missing return value (Phil Sutter) [1329730]
- remove unnecessary extern (Phil Sutter) [1329730]
- ss: Add support for SCTP protocol (Phil Sutter) [1063934]
- include: Add linux/sctp.h (Phil Sutter) [1063934]
- update inet_diag.h header (Phil Sutter) [1063934]
- macsec: fix byte ordering on input/display of 'sci' (Davide Caratti) [1355629]
- macsec: fix input of 'port', improve documentation of 'address' (Davide Caratti) [1355629]
- misc/ss: tcp cwnd should be unsigned (Davide Caratti) [1375215]

* Thu Aug 25 2016 Phil Sutter <psutter@redhat.com> [3.10.0-74.el7]
- ip route: restore_handler should check tb[RTA_PREFSRC] for local networks (Phil Sutter) [1362728]

* Thu Aug 18 2016 Phil Sutter <psutter@redhat.com> [3.10.0-73.el7]
- ip-link: add missing {min,max}_tx_rate to help text (Phil Sutter) [1340914]
- man: ip-link.8: Document missing geneve options (Phil Sutter) [1339178]
- iproute.spec: Fix for missing cbq.8 man page (Phil Sutter) [1362551]

* Thu Aug 04 2016 Phil Sutter <psutter@redhat.com> [3.10.0-72.el7]
- macsec: cipher and icvlen can be set separately (Davide Caratti) [1354408]
- ip {link,address}: add 'macsec' item to TYPE list (Davide Caratti) [1354702]
- man: macsec: fix macsec related typos (Davide Caratti) [1354702 1354319]
- Revert "Allow specifying bridge port STP state by name rather than number." (Phil Sutter) [1288042]
- Revert "fix ip -force -batch to continue on errors" (Phil Sutter) [1288042]
- Revert "ip: fix exit code for addrlabel" (Phil Sutter) [1288042]
- Revert "link dump filter" (Phil Sutter) [1288042]
- Revert "ip: return correct exit code on route failure" (Phil Sutter) [1288042]
- Revert "ip: fix exit code for rule failures" (Phil Sutter) [1288042]
- man: ip-link: Drop fou and gue related documentation (Phil Sutter) [1013584]
- man: ip-link, ip-address: Drop references to ipvlan (Phil Sutter) [1013584]
- doc, man: ip-rule: Remove incorrect statement about rule 0 (Phil Sutter) [1362561]

* Sat Jul 30 2016 Phil Sutter <psutter@redhat.com> [3.10.0-71.el7]
- ip: add paren to silence warning (Phil Sutter) [1340914]
- Fix MAC address length check (Jakub Sitnicki) [1253767 1271580]
- iplink: Check address length via netlink (Jakub Sitnicki) [1253767 1271580]
- iplink: Add missing variable initialization (Jakub Sitnicki) [1253767 1271580]
- ip link: Fix crash on older kernels when show VF dev (Jakub Sitnicki) [1340914]
- ip link: Remove unnecessary device checking (Jakub Sitnicki) [1340914]
- ip: check for missing dev arg when doing VF rate (Jakub Sitnicki) [1340914]
- Add support to configure SR-IOV VF minimum and maximum Tx rate through ip tool (Jakub Sitnicki) [1340914]

* Fri Jul 22 2016 Phil Sutter <psutter@redhat.com> [3.10.0-70.el7]
- man: ip-link: Document query_rss option (Phil Sutter) [1264146]
- Document VF link state control in the ip-link man page (Phil Sutter) [1264146]
- ipneigh: List all nud states in help output (Phil Sutter) [1276661]
- iproute2: ip-route.8.in: Add expires option for ip route (Phil Sutter) [1357020]
- ip route: timeout for routes has to be set in seconds (Phil Sutter) [1357020]
- route: allow routes to be configured with expire values (Phil Sutter) [1357020]

* Wed Jul 20 2016 Phil Sutter <psutter@redhat.com> [3.10.0-69.el7]
- ip-address.8: Document autojoin flag (Phil Sutter) [1333513]
- ip-link.8: Fix font choices (Phil Sutter) [1269528]
- ip-link: fix man page warnings (Phil Sutter) [1269528]
- vxlan: fix help and man text (Phil Sutter) [1269528]
- ip-link: fix unterminated string in manpage (Phil Sutter) [1269528]
- ip-link.8: Add slave type option descriptions (Phil Sutter) [1269528]
- ip-link.8: Place 'ip link set' warning more prominently (Phil Sutter) [1269528]
- ip-link.8: Extend type list in synopsis (Phil Sutter) [1269528]
- man ip-link: Remove extra GROUP explanation (Phil Sutter) [1269528]
- man ip-link: Add short description about 'group' (Phil Sutter) [1269528]
- man ip-link: Add deleting links by group (Phil Sutter) [1269528]
- iplink: bond_slave: Add missing help functions (Phil Sutter) [1269528]
- iplink: List valid 'type' argument in ip link help text (Phil Sutter) [1269528]
- ip link: Add group in usage() for 'ip link delete' (Phil Sutter) [1269528]
- iproute: constify rtattr_cmp (Phil Sutter) [1348133]
- ip route: restore route entries in correct order (Phil Sutter) [1348133]

* Sat Jul 09 2016 Phil Sutter <psutter@redhat.com> [3.10.0-68.el7]
- devlink: add manpage for shared buffer (Phil Sutter) [1342515]
- devlink: implement shared buffer occupancy control (Phil Sutter) [1342515]
- devlink: implement shared buffer support (Phil Sutter) [1342515]
- devlink: allow to parse both devlink and port handle in the same time (Phil Sutter) [1342515]
- devlink: introduce dump filtering function (Phil Sutter) [1342515]
- devlink: split dl_argv_parse_put to parse and put parts (Phil Sutter) [1342515]
- devlink: introduce helper to print out nice names (ifnames) (Phil Sutter) [1342515]
- devlink: introduce pr_out_port_handle helper (Phil Sutter) [1342515]
- list: add list_add_tail helper (Phil Sutter) [1342515]
- list: add list_for_each_entry_reverse macro (Phil Sutter) [1342515]
- devlink: fix "devlink port" help message (Phil Sutter) [1342515]
- devlink: ignore build result (Phil Sutter) [1342515]
- add devlink tool (Phil Sutter) [1342515]
- include: add linked list implementation from kernel (Phil Sutter) [1342515]
- configure: cleanup (Phil Sutter) [1342515]
- configure: Check for libmnl (Phil Sutter) [1342515]
- configure: Add check for the doc tools (Phil Sutter) [1342515]
- add if_macsec header (Davide Caratti) [1300765]
- RH-INTERNAL: update kernel headers to v4.6.0 (Davide Caratti) [1300765]
- utils: fix hex digits parsing in hexstring_a2n() (Davide Caratti) [1300765]
- ip: add MACsec support (Davide Caratti) [1300765]
- utils: provide get_hex to read a hex digit from a char (Davide Caratti) [1300765]
- utils: add get_be{16, 32, 64}, use them where possible (Davide Caratti) [1300765]
- utils: make hexstring_a2n provide the number of hex digits parsed (Davide Caratti) [1300765]
- lib/ll_addr: improve ll_addr_n2a() a bit (Davide Caratti) [1300765]
- iproute2: arpd: use ll_addr_a2n and ll_addr_n2a (Davide Caratti) [1300765]
- iproute2: utils: change hexstring_n2a and hexstring_a2n to do not work with ":" (Davide Caratti) [1300765]

* Tue Jul 05 2016 Phil Sutter <psutter@redhat.com> [3.10.0-67.el7]
- geneve: fix IPv6 remote address reporting (Phil Sutter) [1339178]
- geneve: add support to set flow label (Phil Sutter) [1339178]
- geneve: Add support for configuring UDP checksums. (Phil Sutter) [1339178]
- geneve: add support for lwt tunnel creation and dst port selection (Phil Sutter) [1339178]
- geneve: add support for IPv6 link partners (Phil Sutter) [1339178]
- iplink_geneve: add tos configuration at link creation (Phil Sutter) [1339178]
- iplink_geneve: add ttl configuration at link creation (Phil Sutter) [1339178]
- iproute2: update ip-link.8 for geneve tunnels (Phil Sutter) [1339178]
- iproute2: GENEVE support (Phil Sutter) [1339178]
- man: ip-address, ip-link: Document 'type' quirk (Phil Sutter) [1341343]
- man: ip-link.8: Fix 'ip link delete' description (Phil Sutter) [1341343]

* Thu Jun 16 2016 Phil Sutter <psutter@redhat.com> [3.10.0-66.el7]
- ip-link: Support printing VF trust setting (Phil Sutter) [1302119]
- iplink: Support VF Trust (Phil Sutter) [1302119]
- add new IFLA_VF_TRUST netlink attribute (Phil Sutter) [1302119]
- ipaddress: Allow listing addresses by type (Phil Sutter) [1341343]
- man ip-link: Small example of 'ip link show master' (Phil Sutter) [1341343]
- ip link: Show devices by type (Phil Sutter) [1341343]
- ip link: Allow to filter devices by master dev (Phil Sutter) [1341343]

* Fri Jun 03 2016 Phil Sutter <psutter@redhat.com> [3.10.0-65.el7]
- man: ip, ip-link: Fix ip option location (Phil Sutter) [1251186]
- ip: enable configuring multicast group autojoin (Phil Sutter) [1333513]
- ss: Fix accidental state filter override (Phil Sutter) [1318005]
- ss: Drop silly assignment (Phil Sutter) [1318005]
- ss: Fix wrong filter behaviour (Phil Sutter) [1318005]

* Wed Mar 30 2016 Phil Sutter <psutter@redhat.com> [3.10.0-64.el7]
- Add missing build dependency to spec file (Phil Sutter) [1275426]

* Wed Mar 30 2016 Phil Sutter <psutter@redhat.com> [3.10.0-63.el7]
- doc/tc-filters.tex: Drop overly subjective paragraphs (Phil Sutter) [1275426]
- doc: Add my article about tc, filters and actions (Phil Sutter) [1275426]
- gitignore: Ignore 'doc' files generated at runtime (Phil Sutter) [1275426]
- tests: Add runtime generated files to .gitignore (Phil Sutter) [1275426]
- man: ship action man pages (Phil Sutter) [1275426]
- man: tc-skbedit.8: Elaborate a bit on TX queues (Phil Sutter) [1275426]
- man: tc-police.8: Emphasize on the two rate control mechanisms (Phil Sutter) [1275426]
- man: tc-mirred.8: Reword man page a bit, add generic mirror example (Phil Sutter) [1275426]
- man: tc-csum.8: Add an example (Phil Sutter) [1275426]
- tc: connmark, pedit: Rename BRANCH to CONTROL (Phil Sutter) [1275426]
- tc: pedit: document branch control in help output (Phil Sutter) [1275426]
- man: tc-u32: Minor syntax fix (Phil Sutter) [1275426]
- man: Add a man page for the xt action (Phil Sutter) [1275426]
- man: Add a man page for the skbedit action (Phil Sutter) [1275426]
- man: Add a man page for the simple action (Phil Sutter) [1275426]
- man: Add a man page for the police action (Phil Sutter) [1275426]
- man: Add a man page for the pedit action (Phil Sutter) [1275426]
- man: Add a man page for the nat action (Phil Sutter) [1275426]
- man: Add a man page for the mirred action (Phil Sutter) [1275426]
- man: Add a man page for the csum action. (Phil Sutter) [1275426]

* Wed Mar 23 2016 Phil Sutter <psutter@redhat.com> [3.10.0-62.el7]
- tc: fix compilation warning on 32bits arch (Phil Sutter) [1315930]
- whitespace cleanup (Phil Sutter) [1315930]
- tc: minor spelling fixes (Phil Sutter) [1315930]
- simple print newline (Phil Sutter) [1315930]
- tc: introduce simple action (Phil Sutter) [1315930]
- man: rtpr: add minimal manpage (Phil Sutter) [1316059]

* Tue Mar 08 2016 Phil Sutter <psutter@redhat.com> [3.10.0-61.el7]
- fix print_ipt: segfault if more then one filter with action -j MARK. (Phil Sutter) [1314403]
- man: ip-link: Beef up VXLAN csum options a bit (Phil Sutter) [1254625]
- libnetlink: Double the dump buffer size (Phil Sutter) [1304840]

* Mon Mar 07 2016 Phil Sutter <psutter@redhat.com> [3.10.0-60.el7]
- man: ip-neighbour.8: Document all known nud states (Phil Sutter) [1276661]
- fix indentation of ip neighbour man page (Phil Sutter) [1276661]
- man: ip-*.8: drop any reference to generic ip options (Phil Sutter) [1251186]
- man8: scrub trailing whitespace (Phil Sutter) [1251186]
- TBF man page fix (tbf is not classless) (Phil Sutter) [1251186]
- man tc-htb: Fix HRB -> HTB typo (Phil Sutter) [1251186]
- man: Spelling fixes (Phil Sutter) [1251186]
- fix spelling of Kuznetsov (Phil Sutter) [1251186]
- man: ip-l2tp.8: Fix BNF syntax (Phil Sutter) [1251186]
- man: ip.8: Add missing flags and token subcommand description (Phil Sutter) [1251186]
- man: ip: add -h[uman-readable] option (Phil Sutter) [1251186]
- man: ip-xfrm.8: Document missing parameters (Phil Sutter) [1251186]
- man: ip-tunnel.8: Document missing 6rd action (Phil Sutter) [1251186]
- add 'vti'/'vti6' tunnel modes to ip-tunnel manual page (Phil Sutter) [1251186]
- man: ip-token.8: Review synopsis section (Phil Sutter) [1251186]
- man: ip-rule.8: Review synopsis section (Phil Sutter) [1251186]
- man: ip-ntable.8: Review synopsis section (Phil Sutter) [1251186]
- man: ip-netns.8: Clarify synopsis a bit (Phil Sutter) [1251186]
- man: ip-neighbour: Fix for missing NUD_STATE description (Phil Sutter) [1251186]
- man: ip-link.8: Fix and improve synopsis (Phil Sutter) [1251186]
- man: ip-link.8: minor font fix (Phil Sutter) [1251186]
- man: ip-address.8: Minor syntax fixes (Phil Sutter) [1251186]
- iprule: add missing nat keyword to help text (Phil Sutter) [1251186]
- iproute: TYPE keyword is not optional, fix help text accordingly (Phil Sutter) [1251186]
- ipntable: Fix typo in help text (Phil Sutter) [1251186]
- ipneigh: add missing proxy keyword to help text (Phil Sutter) [1251186]
- iplink: fix help text syntax (Phil Sutter) [1251186]
- ipaddrlabel: Improve help text precision (Phil Sutter) [1251186]
- ip: align help text with manpage (Phil Sutter) [1251186]
- ipl2tp: Print help even on systems without l2tp support (Phil Sutter) [1251186]
- iprule: Align help text with man page synopsis (Phil Sutter) [1251186]
- iplink: macvtap: fix man page (Phil Sutter) [1013584]
- man: ip-link: document MACVLAN/MACVTAP interface types (Phil Sutter) [1013584]
- man: ip-link: fix a typo (Phil Sutter) [1013584]
- man ip-link: Add missing link types - vti,ipvlan,nlmon (Phil Sutter) [1013584]
- iproute2: ip-link.8.in: Spelling fixes (Phil Sutter) [1013584]
- ip-link: Document IPoIB link type in the man page (Phil Sutter) [1013584]
- iproute: Descriptions of fou and gue options in ip-link man pages (Phil Sutter) [1013584]
- iproute2: ip6gre: update man pages (Phil Sutter) [1013584]
- ip: macvlan: support MACVLAN_FLAG_NOPROMISC flag (Phil Sutter) [1013584]
- ip: link: consolidate macvlan and macvtap (Phil Sutter) [1013584]

* Wed Feb 24 2016 Phil Sutter <psutter@redhat.com> [3.10.0-59.el7]
- iplink: add ageing_time, stp_state and priority for bridge (Phil Sutter) [1270759]
- iplink: shortify printing the usage of link type (Phil Sutter) [1270759]
- iplink: use the short format to print help info (Phil Sutter) [1270759]
- iplink_bridge: add support for priority (Phil Sutter) [1270759]
- iplink_bridge: add support for stp_state (Phil Sutter) [1270759]
- iplink_bridge: add support for ageing_time (Phil Sutter) [1270759]
- add bridge master device support (Phil Sutter) [1270759]
- add bridge_slave device support (Phil Sutter) [1270759]
- iplink: bond_slave: fix ad_actor/partner_oper_port_state output (Phil Sutter) [1269528]
- ip: remove extra newlines at end-of-file (Phil Sutter) [1269528]
- ip link: missing options in bond usage (Phil Sutter) [1269528]
- bond: fix return after invarg (Phil Sutter) [1269528]
- iplink: bonding: add support for IFLA_BOND_TLB_DYNAMIC_LB (Phil Sutter) [1269528]
- bonding: export 3ad actor and partner port state (Phil Sutter) [1269528]
- iplink_bond: add support for ad_actor and port_key options (Phil Sutter) [1269528]
- ip link: Shortify printing the usage of link type (Phil Sutter) [1269528]
- add help command to bonding master (Phil Sutter) [1269528]
- iproute2: allow to change slave options via type_slave (Phil Sutter) [1269528]
- ip: add nlmon as a device type to help message (Phil Sutter) [1269528]
- iplink: can: fix help text and man page (Phil Sutter) [1269528]
- iplink_bond_slave: show mii_status only once (Phil Sutter) [1269528]
- iplink_bond: fix parameter value matching (Phil Sutter) [1269528]
- iplink_bond: fix arp_all_targets parameter name in output (Phil Sutter) [1269528]
- iplink: add support for bonding slave (Phil Sutter) [1269528]
- introduce support for slave info data (Phil Sutter) [1269528]
- iproute2: finish support for bonding attributes (Phil Sutter) [1269528]
- iplink: add support for bonding netlink (Phil Sutter) [1269528]
- iplink: update available type list (Phil Sutter) [1269528]
- xfrm: revise man page and document ip xfrm policy set (Phil Sutter) [1269528]
- xfrm: add command for configuring SPD hash table (Phil Sutter) [1212026]

* Thu Feb 18 2016 Phil Sutter <psutter@redhat.com> [3.10.0-58.el7]
- tc: ship filter man pages and refer to them in tc.8 (Phil Sutter) [1286711]
- tc: add a man page for u32 filter (Phil Sutter) [1286711]
- tc: add a man page for tcindex filter (Phil Sutter) [1286711]
- tc: add a man page for route filter (Phil Sutter) [1286711]
- tc: add a man page for fw filter (Phil Sutter) [1286711]
- tc: add a man page for flow filter (Phil Sutter) [1286711]
- tc: add a man page for cgroup filter (Phil Sutter) [1286711]
- tc: add a man page for basic filter (Phil Sutter) [1286711]
- batch: support quoted strings (Phil Sutter) [1272593]
- man: fix whatis for fq (Phil Sutter) [1261520]
- man: tc: add man page for fq pacer (Phil Sutter) [1261520]

* Thu Feb 18 2016 Phil Sutter <psutter@redhat.com> [3.10.0-57.el7]
- route: Fix printing of locked entries (Phil Sutter) [1291832]
- route: ignore RTAX_HOPLIMIT of value -1 (Phil Sutter) [1291832]
- ip-link: remove warning message (Phil Sutter) [1291832]
- ip: route: add congestion control metric (Phil Sutter) [1291832]
- ip route: enable per-route ecn settings via 'features' option (Phil Sutter) [1291832]
- iproute2: ip-route.8.in: minor fixes (Phil Sutter) [1291832]
- iproute: restrict hoplimit values to be in range [0; 255] (Phil Sutter) [1291832]
- man ss: Fix explanation when no options specified (Phil Sutter) [1291818]
- libnetlink: don't confuse variables in rtnl_talk() (Phil Sutter) [1288042]
- libnetlink: add size argument to rtnl_talk (Phil Sutter) [1288042]
- ip: fix exit code for rule failures (Phil Sutter) [1288042]
- ip: return correct exit code on route failure (Phil Sutter) [1288042]
- link dump filter (Phil Sutter) [1288042]
- ip: fix exit code for addrlabel (Phil Sutter) [1288042]
- fix ip -force -batch to continue on errors (Phil Sutter) [1288042]
- Allow specifying bridge port STP state by name rather than number. (Phil Sutter) [1288042]
- gre: raising the size of the buffer holding nl messages. (Phil Sutter) [1288042]
- neighbor: check return values (Phil Sutter) [1277094]
- ip-address: fix oneline mode for interfaces with VF (Phil Sutter) [1272405]
- ss: add support for segs_in and segs_out (Phil Sutter) [1269114]
- ss: add support for bytes_acked & bytes_received (Phil Sutter) [1269114]
- ss: return -1 if an unrecognized option was given (Phil Sutter) [1265238]
- man: ip-address: document mngtmpaddr and noprefixroute flags (Phil Sutter) [1231898]
- man: ip-address: align synopsis with help output (Phil Sutter) [1231898]
- ip-address.8.in: fix BNF syntax error (Phil Sutter) [1231898]
- ip-address: fix and extend documentation (Phil Sutter) [1231898]
- ip: extend "ip-address" man page to reflect the recent flag extensions (Phil Sutter) [1231898]
- ip: allow ip address show to list addresses with certain flags not being set (Phil Sutter) [1231898]
- bridge fdb: add 'use' option to set NTF_USE flag in fdb add requests (Phil Sutter) [1075692]
- bridge: drop man page fragment (Phil Sutter) [1075692]
- bridge: drop reference to unused option embedded from manpage (Phil Sutter) [1075692]

* Thu Feb 18 2016 Phil Sutter <psutter@redhat.com> [3.10.0-56.el7]
- ipaddress: fix ipaddr_flush for Linux >= 3.1 (Phil Sutter) [1291825]
- ipaddress: simplify ipaddr_flush() (Phil Sutter) [1291825]
- libnetlink: introduce nc_flags (Phil Sutter) [1291825]
- iproute2: Ignore EADDRNOTAVAIL errors during address flush operation (Phil Sutter) [1291825]
- lnstat: fix header displaying mechanism (Phil Sutter) [1263392]
- man: lnstat: rewrite manpage (Phil Sutter) [1269133]

* Wed Feb 17 2016 Phil Sutter <psutter@redhat.com> [3.10.0-55.el7]
- Resolves: #1290860 - Rework list of patches, replace by upstream backports

* Thu Sep 17 2015 Phil Sutter - 3.10.0-54
- Related: #1241486 - backport: tc: fq scheduler - add missing documentation

* Thu Sep 03 2015 Phil Sutter - 3.10.0-53
- Related: #1212026 - [6wind 7.2 Feat]: backport: ipxfrm: unable to configure
  SPD hash table - reverted this backport due to unmet dependencies

* Mon Aug 24 2015 Phil Sutter - 3.10.0-52
- Resolves: #1254095 - bridge: Add master device name to bridge fdb show
- Resolves: #1255316 - tc does not allow to attach pfifo_fast qdisc
- Related: #1251070 - Fix multiple programming errors in iproute package

* Sun Aug 16 2015 Phil Sutter - 3.10.0-51
- Resolves: bz#1251451 - can't change the remote/local address of tunnel
  interface to "any" in ipip mode
- Related: #1213869 - [6wind 7.2 Feat]: backport: iproute2: various netns
  features
- Related: #1215006 - [RFE] backport current version of the ss command
- Resolves: #1251070 - Fix multiple programming errors in iproute package
- Related: #1198456 - backport: dynamic precision, human readable, and IEC
  output to ip stats
- Related: #1210402 - [6wind 7.2 Feat]: backport: vxlan: unable to configure
  UDP checksums
- Related: #1213869 - [6wind 7.2 Feat]: backport: iproute2: various netns
  features

* Fri Aug 07 2015 Phil Sutter - 3.10.0-50
- Resolves: #1244851 - vti tunnel does not work
- Resolves: #1155116 - iproute2: implement "-d" option for "ip mon"

* Thu Aug 06 2015 Phil Sutter - 3.10.0-49
- Resolves: bz#1241486 - backport: tc: fq scheduler
- Related: #1215006 - backport current version of the ss command

* Wed Aug 05 2015 Phil Sutter - 3.10.0-48
- Related: #1215006 - backport current version of the ss command
- Resolves: #1247315 - Fix limitation in iproute/ss regarding dual-stack sockets

* Mon Aug 03 2015 Phil Sutter - 3.10.0-47
- Related: #1215006 - backport current version of the ss command
- Related: #1219280 - backport: iproute2: vti6 support

* Wed Jul 08 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-46
- Related: #1198456 - add missing parts

* Wed Jul 08 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-45
- Related: #1213869 - add support for 'ip -all netns'

* Wed Jul 08 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-44
- Related: #1176180 - put back addrgenmode docs

* Wed Jul 08 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-43
- Related: #1131928 - make netns docs consistent

* Wed Jul 08 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-42
- Resolves: #1169901 - ip rule help output contains action reject, but this
  action does not work

* Tue Jul 07 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-41
- Resolves: #1169874 - ip rule command allows to remove rule with priority 0

* Tue Jul 07 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-40
- Resolves: #1042802 - make 'ip -d monitor' consistent with 'ip -d link'

* Thu Jun 04 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-39
- Resolves: #1228166 - remove redundant libnl-devel build dependency

* Tue Jun 02 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-38
- Resolves: #1131473 - backport: implement -s option for ip a

* Tue Jun 02 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-37
- Resolves: #1213869 - backport: iproute2: unable to manage nsid

* Fri May 29 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-36
- Resolves: #1224970 - backport: ipv6: support noprefixroute and mngtmpaddr

* Thu May 28 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-35
- Related: #1198456 - refactor patchset thoroughly

* Mon May 25 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-34
- Resolves: #1176684 - backport: ip xfrm monitor all does not work

* Mon May 25 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-33
- Resolves: #1219280 - backport: iproute2: vti6 support

* Wed May 20 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-32
- Resolves: #1198489 - backport: "ip route del" without arguments should print
  help

* Thu May 14 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-31
- Resolves: #1218568 - backport: iproute2: query_rss command is missing

* Thu May 14 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-30
- Resolves: #1212026 - backport: ipxfrm: unable to configure SPD hash table

* Wed May 13 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-29
- Resolves: #1210402 - backport: vxlan: unable to configure UDP checksums

* Wed May 13 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-28
- Resolves: #1131928 - backport: introduce option to ip to operate on a
  different namespace

* Wed May 13 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-27
- Resolves: #1198456 - make sure the patch is applied

* Tue Apr 28 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-26
- Resolves: #1198456 - backport changes in link statistics

* Tue Apr 28 2015 Pavel Šimerda <psimerda@redhat.com>
- Resolves: #1139173 - ip -s xfrm state crashes with segfault

* Tue Apr 28 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-24
- Resolves: #1215006 - backport current version of the ss command

* Fri Apr 17 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-23
- Resolves: #1203646 - backport VXLAN-GBP

* Thu Apr 16 2015 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-22
- Resolves: #1176180 - ip -d link show: print addrgenmode

* Fri Oct 24 2014 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-21
- Related: #1119180 - improve addrgen documentation

* Fri Oct 24 2014 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-20
- Related: #1119180 - document addrgen

* Wed Oct 08 2014 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-19
- Resolves: #1081081 - lnstat man page references iproute-doc when it should
  reference iproute-<ver>

* Fri Oct 03 2014 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-18
- Resolves: #1044535 - tc: add cls_bpf frontend

* Fri Oct 03 2014 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-17
- Resolves: #1044535 - backport tc:

* Fri Oct 03 2014 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-16
- Resolves: #1091010 - [RFE] iproute2: Allow Configurable TCP Delayed Ack in
  RHEL

* Fri Oct 03 2014 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-15
- Resolves: #1100271 - ip -6 addrlabel return incorrect error message

* Fri Oct 03 2014 Pavel Šimerda <psimerda@redhat.com> - 3.10.0-14
- Resolves: #1119180 - iproute2: allow to ipv6 set address generation mode

* Tue Feb 25 2014 Petr Šabata <contyk@redhat.com> - 3.10.0-13
- Add VF link state control mechanisms (#1061593)

* Tue Feb 25 2014 Petr Šabata <contyk@redhat.com> - 3.10.0-12
- Add destination port and IPv6 support to VXLAN (#1067437)

* Wed Jan 29 2014 Petr Šabata <contyk@redhat.com> - 3.10.0-11
- Don't hang on rtnl_send() failure (#1040454)
- Add the dstport option to vxlan (#1039855)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.10.0-10
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.10.0-9
- Mass rebuild 2013-12-27

* Tue Nov 26 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-8
- Document fdb replace and embedded bridge options (#1024697)

* Fri Nov 22 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-7
- Fix the rtt time values (#1032501)

* Fri Nov 08 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-6
- Fix lnstat -i (#1024426)
- Support IPv6 peer addresses (#1017228)
- Add the replace command to bridge fdb (#1024697)
- Document link type vlan (#979326)

* Tue Oct 01 2013 Petr Pisar <ppisar@redhat.com> - 3.10.0-5
- Close file with bridge monitor file (#1011818)

* Tue Sep 24 2013 Petr Pisar <ppisar@redhat.com> - 3.10.0-4
- Document tc -OK option (#977844)
- Document "bridge mdb" and "bridge monitor mdb" (#1009860)

* Wed Sep 18 2013 Marcela Mašláňová <mmaslano@redhat.com> - 3.10.0-3
- Add '-OK' command line option to tc telling it to write an "OK\n" to stdout
- rhbz#977844

* Mon Aug 05 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-2.1
- Add a skeleton manpages for genl and ifstat (#881180)

* Wed Jul 17 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-2
- Fix the XFRM patch

* Wed Jul 17 2013 Petr Šabata <contyk@redhat.com> - 3.10.0-1
- 3.10.0 bump
- Drop the SHAREDIR patch and revert to upstream ways (#966445)
- Fix an XFRM regression with FORTIFY_SOURCE

* Tue Apr 30 2013 Petr Šabata <contyk@redhat.com> - 3.9.0-1
- 3.9.0 bump

* Thu Apr 25 2013 Petr Šabata <contyk@redhat.com> - 3.8.0-4
- ATM is available in Fedora only

* Tue Mar 12 2013 Petr Šabata <contyk@redhat.com> - 3.8.0-3
- Mention the "up" argument in documentation and help outputs (#907468)

* Mon Mar 04 2013 Petr Šabata <contyk@redhat.com> - 3.8.0-2
- Bump for 1.4.18 rebuild

* Tue Feb 26 2013 Petr Šabata <contyk@redhat.com> - 3.8.0-1
- 3.8.0 bump

* Fri Feb 08 2013 Petr Šabata <contyk@redhat.com> - 3.7.0-2
- Don't propogate mounts out of ip (#882047)

* Wed Dec 12 2012 Petr Šabata <contyk@redhat.com> - 3.7.0-1
- 3.7.0 bump

* Mon Nov 19 2012 Petr Šabata <contyk@redhat.com> - 3.6.0-3
- Include section 7 manpages (#876857)
- Fix ancient bogus dates in the changelog (correction based upon commits)
- Explicitly require some TeX fonts no longer present in the base distribution

* Thu Oct 04 2012 Petr Šabata <contyk@redhat.com> - 3.6.0-2
- List all interfaces by default

* Wed Oct 03 2012 Petr Šabata <contyk@redhat.com> - 3.6.0-1
- 3.6.0 bump

* Thu Aug 30 2012 Petr Šabata <contyk@redhat.com> - 3.5.1-2
- Remove the explicit iptables dependency (#852840)

* Tue Aug 14 2012 Petr Šabata <contyk@redhat.com> - 3.5.1-1
- 3.5.1 bugfix release bump
- Rename 'br' to 'bridge'

* Mon Aug 06 2012 Petr Šabata <contyk@redhat.com> - 3.5.0-2
- Install the new bridge utility

* Thu Aug 02 2012 Petr Šabata <contyk@redhat.com> - 3.5.0-1
- 3.5.0 bump
- Move to db5.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Petr Šabata <contyk@redhat.com> - 3.4.0-1
- 3.4.0 bump
- Drop the print route patch (included upstream)

* Mon Apr 30 2012 Petr Šabata <contyk@redhat.com> - 3.3.0-2
- Let's install rtmon too... (#814819)

* Thu Mar 22 2012 Petr Šabata <contyk@redhat.com> - 3.3.0-1
- 3.3.0 bump
- Update source URL

* Mon Feb 27 2012 Petr Šabata <contyk@redhat.com> - 3.2.0-3
- Address dangerous /tmp files security issue (CVE-2012-1088, #797881, #797878)

* Fri Jan 27 2012 Petr Šabata <contyk@redhat.com> - 3.2.0-2
- Simplify the spec a bit thanks to the UsrMove feature

* Fri Jan 06 2012 Petr Šabata <contyk@redhat.com> - 3.2.0-1
- 3.2.0 bump
- Removing a useless, now conflicting patch (initcwnd already decumented)

* Thu Nov 24 2011 Petr Šabata <contyk@redhat.com> - 3.1.0-1
- 3.1.0 bump
- Point URL and Source to the new location on kernel.org
- Remove now obsolete defattr
- Dropping various patches now included upstream
- Dropping iproute2-2.6.25-segfault.patch; I fail to understand the reason for
  this hack

* Tue Nov 15 2011 Petr Šabata <contyk@redhat.com> - 2.6.39-6
- ss -ul should display UDP CLOSED sockets (#691100)

* Thu Oct 06 2011 Petr Sabata <contyk@redhat.com> - 2.6.39-5
- Fix ss, lnstat and arpd usage and manpages

* Wed Sep 07 2011 Petr Sabata <contyk@redhat.com> - 2.6.39-4
- lnstat should dump (-d) to stdout instead of stderr (#736332)

* Tue Jul 26 2011 Petr Sabata <contyk@redhat.com> - 2.6.39-3
- Rebuild for xtables7

* Tue Jul 12 2011 Petr Sabata <contyk@redhat.com> - 2.6.39-2
- Rebuild for xtables6

* Thu Jun 30 2011 Petr Sabata <contyk@redhat.com> - 2.6.39-1
- 2.6.39 bump

* Wed Apr 27 2011 Petr Sabata <psabata@redhat.com> - 2.6.38.1-4
- Link [cr]tstat to lnstat

* Wed Apr 27 2011 Petr Sabata <psabata@redhat.com> - 2.6.38.1-3
- Install ctstat, rtstat and routef manpage symlinks
- Install m_xt & m_ipt tc modules
- Creating devel and virtual static subpackages with libnetlink

* Thu Apr 21 2011 Petr Sabata <psabata@redhat.com> - 2.6.38.1-2
- General cleanup
- Use global instead of define
- Buildroot removal
- Correcting URL and Source links
- Install genl, ifstat, routef, routel and rtpr (rhbz#697319)

* Fri Mar 18 2011 Petr Sabata <psabata@redhat.com> - 2.6.38.1-1
- 2.6.38.1 bump

* Wed Mar 16 2011 Petr Sabata <psabata@redhat.com> - 2.6.38-1
- 2.6.38 bump

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Petr Sabata <psabata@redhat.com> - 2.6.37-2
- man-pages.patch update, ip(8) TYPE whitespace

* Mon Jan 10 2011 Petr Sabata <psabata@redhat.com> - 2.6.37-1
- 2.6.37 upstream release
- ss(8) improvements patch removed (included upstream)

* Wed Dec 08 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-10
- fix a typo in ss(8) improvements patch, rhbz#661267

* Tue Nov 30 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-9
- ss(8) improvements patch by jpopelka; should be included in 2.6.36

* Tue Nov 09 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-8
- rhbz#641599, use the versioned path, man-pages.patch update, prep update

* Tue Oct 12 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-7
- Do not segfault if peer name is omitted when creating a peer veth link, rhbz#642322

* Mon Oct 11 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-6
- Man-pages update, rhbz#641599

* Wed Sep 29 2010 jkeating - 2.6.35-5
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-4
- Modified man-pages.patch to fix cbq manpage, rhbz#635877

* Tue Sep 21 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-3
- Don't print routes with negative metric fix, rhbz#628739

* Wed Aug 18 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-2
- 'ip route get' fix, iproute2-2.6.35-print-route.patch
- rhbz#622782

* Thu Aug 05 2010 Petr Sabata <psabata@redhat.com> - 2.6.35-1
- 2.6.35 version bump
- iproute2-tc-priority.patch removed (included in upstream now)

* Thu Jul 08 2010 Petr Sabata <psabata@redhat.com> - 2.6.34-5
- Licensing guidelines compliance fix

* Wed Jul 07 2010 Petr Sabata <psabata@redhat.com> - 2.6.34-4
- Requires: iptables >= 1.4.5, BuildRequires: iptables-devel >= 1.4.5

* Thu Jul 01 2010 Petr Sabata <psabata@redhat.com> - 2.6.34-3
- Build now runs ./configure to regenerate Makefile for ipt/xt detection

* Mon Jun 21 2010 Petr Sabata <psabata@redhat.com> - 2.6.34-2
- iproute-tc-priority.patch, rhbz#586112

* Mon Jun 21 2010 Petr Sabata <psabata@redhat.com> - 2.6.34-1
- 2.6.34 version bump

* Tue Apr 20 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.33-2
- 578729 6rd tunnel correctly 3979ef91de9ed17d21672aaaefd6c228485135a2
- change BR texlive to tex according to guidelines

* Thu Feb 25 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.33-1
- update

* Tue Jan 26 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.32-2
- add macvlan aka VESA support d63a9b2b1e4e3eab0d0577d0a0f412d50be1e0a7
- kernel headers 2.6.33 ab322673298bd0b8927cdd9d11f3d36af5941b93
  are needed for macvlan features and probably for other added later.
- fix number of release which contains 2.6.32 kernel headers and features
  but it was released as 2.6.31

* Mon Jan  4 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.31-1
- update to 2.6.31

* Fri Nov 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-5.1.20091106gita7a9ddbb
- 539232 patch cbq initscript

* Fri Nov 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-5.0.20091106gita7a9ddbb
- snapshot with kernel headers for 2.6.32

* Fri Oct  9 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-5.0.20091009gitdaf49fd6
- new official version isn't available but it's needed -> switch to git snapshots

* Thu Sep 24 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-5
- create missing man pages

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 23 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-3
- new iptables (xtables) bring problems to tc, when ipt is used. 
  rhbz#497344 still broken. tc_modules.patch brings correct paths to
  xtables, but that doesn't fix whole issue.
- 497355 ip should allow creation of an IPsec SA with 'proto any' 
  and specified sport and dport as selectors

* Tue Apr 14 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-2
- c3651bf4763d7247e3edd4e20526a85de459041b ip6tunnel: Fix no default 
 display of ip4ip6 tunnels
- e48f73d6a5e90d2f883e15ccedf4f53d26bb6e74 missing arpd directory

* Wed Mar 25 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.29-1
- update to 2.6.29
- remove DDR patch which became part of sourc
- add patch with correct headers 1957a322c9932e1a1d2ca1fd37ce4b335ceb7113

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.28-2
- 483484 install distribution files into /usr/share and also fixed
 install paths in spec
- add the latest change from git which add DRR support
 c86f34942a0ce9f8203c0c38f9fe9604f96be706

* Mon Jan 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.28-1
- previous two patches were included into 2.6.28 release.
- update

* Mon Jan 12 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.27-2
- 475130 - Negative preferred lifetimes of IPv6 prefixes/addresses
  displayed incorrectly
- 472878 - “ip maddr show” in IB interface causes a stack corruption
- both patches will be probably in iproute v2.6.28

* Thu Dec 4 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.27-1
- aead support was included into upstream version
- patch for moving libs is now deprecated
- update to 2.6.27

* Tue Aug 12 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.26-1
- update to 2.6.26
- clean patches

* Tue Jul 22 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-5
- fix iproute2-2.6.25-segfault.patch

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.6.25-4
- rebuild for new db4-4.7

* Thu Jul  3 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-3
- 449933 instead of failing strncpy use copying byte after byte

* Wed May 14 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-2
- allow replay setting, solve also 444724

* Mon Apr 21 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-1
- update
- remove patch for backward compatibility
- add patch for AEAD compatibility

* Thu Feb 21 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-4
- add creating ps file again. Fix was done in texlive

* Wed Feb  6 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-3
- rebuild without tetex files. It isn't working in rawhide yet. Added
  new source for ps files. 
- #431179 backward compatibility for previous iproute versions

* Mon Jan 21 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-2
- rebuild with fix tetex and linuxdoc-tools -> manual pdf
- clean unnecessary patches
- add into spec *.so objects, new BR linux-atm-libs-devel

* Wed Oct 31 2007 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-1
- new version from upstrem 2.3.23

* Tue Oct 23 2007 Marcela Maslanova <mmaslano@redhat.com> - 2.6.22-5
- move files from /usr/lib/tc to /usr/share/tc
- remove listing files twice

* Fri Aug 31 2007 Marcela Maslanova <mmaslano@redhat.com> - 2.6.22-3
- package review #225903

* Mon Aug 27 2007 Jeremy Katz <katzj@redhat.com> - 2.6.22-2
- rebuild for new db4

* Wed Jul 11 2007 Radek Vokál <rvokal@redhat.com> - 2.6.22-1
- upgrade to 2.6.22

* Mon Mar 19 2007 Radek Vokál <rvokal@redhat.com> - 2.6.20-2
- fix broken tc-pfifo man page (#232891)

* Thu Mar 15 2007 Radek Vokál <rvokal@redhat.com> - 2.6.20-1
- upgrade to 2.6.20

* Fri Dec 15 2006 Radek Vokál <rvokal@redhat.com> - 2.6.19-1
- upgrade to 2.6.19

* Mon Dec 11 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-5
- fix snapshot version

* Fri Dec  1 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-4
- spec file cleanup
- one more rebuilt against db4

* Thu Nov 16 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-3
- fix defective manpage for tc-pfifo (#215399)

* Mon Nov 13 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-2
- rebuilt against new db4

* Tue Oct  3 2006 Radek Vokal <rvokal@redhat.com> - 2.6.18-1
- upgrade to upstream 2.6.18
- initcwnd patch merged
- bug fix for xfrm monitor
- alignment fixes for cris
- documentation corrections
        
* Mon Oct  2 2006 Radek Vokal <rvokal@redhat.com> - 2.6.16-7
- fix ip.8 man page, add initcwnd option

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.6.16-6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Radek Vokal <rvokal@redhat.com> - 2.6.16-5
- fix crash when resolving ip address

* Mon Aug 21 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-4
- add LOWER_UP and DORMANT flags (#202199)
- use dist tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.6.16-3.1
- rebuild

* Mon Jun 26 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-3
- improve handling of initcwnd value (#179719)

* Sun May 28 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-2
- fix BuildRequires: flex (#193403)

* Sun Mar 26 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-1
- upgrade to 2.6.16-060323
- don't hardcode /usr/lib in tc (#186607)

* Wed Feb 22 2006 Radek Vokál <rvokal@redhat.com> - 2.6.15-2
- own /usr/lib/tc (#181953)
- obsoletes shapecfg (#182284)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.6.15-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.6.15-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 17 2006 Radek Vokal <rvokal@redhat.com> 2.6.15-1
- upgrade to 2.6.15-060110

* Mon Dec 12 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-11
- rebuilt

* Fri Dec 09 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-10
- remove backup of config files (#175302)

* Fri Nov 11 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-9
- use tc manpages and cbq.init from source tarball (#172851)

* Thu Nov 10 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-8
- new upstream source 

* Mon Oct 31 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-7
- add warning to ip tunnel add command (#128107)

* Fri Oct 07 2005 Bill Nottingham <notting@redhat.com> 2.6.14-6
- update from upstream (appears to fix #170111)

* Fri Oct 07 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-5
- update from upstream
- fixed host_len size for memcpy (#168903) <Matt_Domsch@dell.com>

* Fri Sep 23 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-4
- add RPM_OPT_FLAGS

* Mon Sep 19 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-3
- forget to apply the patch :( 

* Mon Sep 19 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-2
- make ip help work again (#168449)

* Wed Sep 14 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-1
- upgrade to ss050901 for 2.6.14 kernel headers

* Fri Aug 26 2005 Radek Vokal <rvokal@redhat.com> 2.6.13-3
- added /sbin/cbq script and sample configuration files (#166301)

* Fri Aug 19 2005 Radek Vokal <rvokal@redhat.com> 2.6.13-2
- upgrade to iproute2-050816

* Thu Aug 11 2005 Radek Vokal <rvokal@redhat.com> 2.6.13-1
- update to snapshot for 2.6.13+ kernel

* Tue May 24 2005 Radek Vokal <rvokal@redhat.com> 2.6.11-2
- removed useless initvar patch (#150798)
- new upstream source 

* Tue Mar 15 2005 Radek Vokal <rvokal@redhat.com> 2.6.11-1
- update to iproute-2.6.11

* Fri Mar 04 2005 Radek Vokal <rvokal@redhat.com> 2.6.10-2
- gcc4 rebuilt

* Wed Feb 16 2005 Radek Vokal <rvokal@redhat.com> 2.6.10-1
- update to iproute-2.6.10

* Thu Dec 23 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-6
- added arpd into sbin

* Mon Nov 29 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-5
- debug info removed from makefile and from spec (#140891)

* Tue Nov 16 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-4
- source file updated from snapshot version
- endian patch adding <endian.h> 

* Sat Sep 18 2004 Joshua Blanton <jblanton@cs.ohiou.edu> 2.6.9-3
- added installation of netem module for tc

* Mon Sep 06 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-2
- fixed possible buffer owerflow, path by Steve Grubb <linux_4ever@yahoo.com>

* Wed Sep 01 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-1
- updated to iproute-2.6.9, spec file change, patches cleared

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 26 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-16
- Took tons of manpages from debian, much more complete (#123952).

* Thu May 06 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-15
- rebuilt

* Thu May 06 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-13.2
- Built security errata version for FC1.

* Wed Apr 21 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-14
- Fixed -f option for ss (#118355).
- Small description fix (#110997).
- Added initialization of some vars (#74961). 
- Added patch to initialize "default" rule as well (#60693).

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Nov 05 2003 Phil Knirsch <pknirsch@redhat.com> 2.4.7-12
- Security errata for netlink (CAN-2003-0856).

* Thu Oct 23 2003 Phil Knirsch <pknirsch@redhat.com>
- Updated to latest version. Used by other distros, so seems stable. ;-)
- Quite a few patches needed updating in that turn.
- Added ss (#107363) and several other new nifty tools.

* Tue Jun 17 2003 Phil Knirsch <pknirsch@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 16 2003 Phil Knirsch <pknirsch@redhat.com> 2.4.7-7
- Added htb3-tc patch from http://luxik.cdi.cz/~devik/qos/htb/ (#75486).

* Fri Oct 11 2002 Bill Nottingham <notting@redhat.com> 2.4.7-6
- remove flags patch at author's request

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-4
- Don't forcibly strip binaries

* Mon May 27 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-3
- Fixed missing diffserv and atm support in config (#57278).
- Fixed inconsistent numeric base problem for command line (#65473).

* Tue May 14 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-2
- Added patch to fix crosscompiling by Adrian Linkins.

* Fri Mar 15 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-1
- Update to latest stable release 2.4.7-now-ss010824.
- Added simple man page for ip.

* Wed Aug  8 2001 Bill Nottingham <notting@redhat.com>
- allow setting of allmulti & promisc flags (#48669)

* Mon Jul 02 2001 Than Ngo <than@redhat.com>
- fix build problem in beehive if kernel-sources is not installed

* Fri May 25 2001 Helge Deller <hdeller@redhat.de>
- updated to iproute2-2.2.4-now-ss001007.tar.gz 
- bzip2 source tar file
- "License" replaces "Copyright"
- added "BuildPrereq: tetex-latex tetex-dvips psutils"
- rebuilt for 7.2

* Tue May  1 2001 Bill Nottingham <notting@redhat.com>
- use the system headers - the included ones are broken
- ETH_P_ECHO went away

* Sat Jan  6 2001 Jeff Johnson <jbj@redhat.com>
- test for specific KERNEL_INCLUDE directories.

* Thu Oct 12 2000 Than Ngo <than@redhat.com>
- rebuild for 7.1

* Thu Oct 12 2000 Than Ngo <than@redhat.com>
- add default configuration files for iproute (Bug #10549, #18887)

* Tue Jul 25 2000 Jakub Jelinek <jakub@redhat.com>
- fix include-glibc/ to cope with glibc 2.2 new resolver headers

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- rebuilt in the new build environment
- use RPM macros
- handle RPM_OPT_FLAGS

* Sat Jun 03 2000 Than Ngo <than@redhat.de>
- fix iproute to build with new glibc

* Fri May 26 2000 Ngo Than <than@redhat.de>
- update to 2.2.4-now-ss000305
- add configuration files

* Mon Sep 13 1999 Bill Nottingham <notting@redhat.com>
- strip binaries

* Mon Aug 16 1999 Cristian Gafton <gafton@redhat.com>
- first build
