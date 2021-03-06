kafka-rpm
=========

A set of scripts to package kafka into an rpm.
Requires CentOS/RedHat 7.
Uses systemctl to register/manage service.
Configures Jolokia as Java Agent.

Setup
-----

    yum install make rpmdevtools

Product Documentation
---------------------

https://kafka.apache.org/documentation/
https://jolokia.org/documentation.html

Build
-----

Check https://archive.apache.org/dist/kafka/ for supported versions.

    git clone https://github.com/nicregez/kafka-rpm.git
    cd kafka-rpm
    export KAFKA_VERSION=2.2.0
    export SCALA_VERSION=2.12
    export BUILD_NUMBER=4
    make wget
    make jolokia
    make rpm

Resulting RPM will be avaliable at $(shell pwd)/RPMS/x86_64

Install
-------

If you want to install locally

    yum install -y RPMS/x86_64/kafka-${KAFKA_VERSION}-${BUILD_NUMBER}.x86_64.rpm

If you install from an RPM repository

    yum install -y kafka

Configure
---------

    vi /etc/kafka/server.properties

Operation
---------

    systemctl enable kafka
    systemctl start kafka

Default locations
-----------------

binaries

-   /opt/kafka/libs

configs

-   /etc/kafka/server.properties
-   /etc/kafka/log4j.properties
-   /etc/sysconfig/kafka

certificates and keystores (use symlinks)

-   /etc/pki/tls/private/kafka-server-keystore.jks
-   /etc/pki/tls/certs/kafka-server-truststore.jks
-   /etc/pki/tls/certs/kafka-client-truststore.jks

systemd

-   /usr/lib/systemd/system/kafka.service

data

-   /var/lib/kafka/data

logs

-   /var/log/kafka/log

tools

-   /opt/kafka/bin
-   /opt/kafka/config/tools-log4j.properties
