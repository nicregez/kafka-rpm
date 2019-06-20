%define __jar_repack 0
%define debug_package %{nil}
%define name kafka
%define _prefix /opt
%define _conf_dir %{_sysconfdir}/kafka
%define _log_dir %{_var}/log/kafka/log
%define _data_dir %{_var}/lib/kafka/data

Summary: Apache Kafka.
Name: kafka
Version: %{version}
Release: %{build_number}
License: Apache License, Version 2.0
Group: Applications
Source0: http://apache.mirrors.spacedump.net/kafka/%{kafka_version}/%{tarball}
Source1: kafka.service
Source2: server.properties
Source3: log4j.properties
Source4: kafka.sysconfig
URL: http://kafka.apache.org/
BuildRoot: %{_tmppath}/%{name}-%{kafka_version}-root
Prefix: %{_prefix}
Vendor: Apache Software Foundation
Packager: Nicolas Regez <nicolas.regez@swisscom.com>
Provides: kafka
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Apache Kafka.

%prep
%setup -n %{tarball_name}

%build
rm -f config/{connect-*.properties,consumer.properties,producer.properties}
rm -f config/{log4j.properties,server.properties,zookeeper.properties,trogdor.conf}
rm -f libs/{kafka_*-javadoc.jar,kafka_*-scaladoc.jar,kafka_*-sources.jar}

%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/kafka
mkdir -p $RPM_BUILD_ROOT%{_prefix}/kafka/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/kafka/config
mkdir -p $RPM_BUILD_ROOT%{_prefix}/kafka/libs
mkdir -p $RPM_BUILD_ROOT%{_log_dir}
mkdir -p $RPM_BUILD_ROOT%{_data_dir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}/kafka.service.d
mkdir -p $RPM_BUILD_ROOT%{_conf_dir}
install -p -D -m 755 bin/kafka-*.sh $RPM_BUILD_ROOT%{_prefix}/kafka/bin
install -p -D -m 644 config/tools-log4j.properties $RPM_BUILD_ROOT%{_prefix}/kafka/config
install -p -D -m 644 libs/*.jar $RPM_BUILD_ROOT%{_prefix}/kafka/libs
install -p -D -m 644 %{S:1} $RPM_BUILD_ROOT%{_unitdir}/
install -p -D -m 644 %{S:2} $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 644 %{S:3} $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 644 %{S:4} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/kafka

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/bin/getent group kafka >/dev/null || /usr/sbin/groupadd -r kafka
if ! /usr/bin/getent passwd kafka >/dev/null ; then
    /usr/sbin/useradd -r -g kafka -m -d %{_prefix}/kafka -s /bin/bash -c "Kafka" kafka
fi

%post
%systemd_post kafka.service

%preun
%systemd_preun kafka.service

%postun
%systemd_postun kafka.service

%files
%defattr(-,root,root)
%{_unitdir}/kafka.service
%attr(-,root,root) %{_prefix}/kafka
%config(noreplace) %{_conf_dir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/kafka
%attr(0755,kafka,kafka) %dir %{_log_dir}
%attr(0700,kafka,kafka) %dir %{_data_dir}

%doc NOTICE
%doc LICENSE
