.PHONY:	rpm clean

KAFKA_VERSION ?= 2.2.0
SCALA_VERSION ?= 2.12
VERSION = $(shell echo $(KAFKA_VERSION) | sed "s/-/_/")
BUILD_NUMBER ?= 1
TARBALL_NAME = kafka_$(SCALA_VERSION)-$(KAFKA_VERSION)
TARBALL = $(TARBALL_NAME).tgz
TARBALL_URL = https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/${TARBALL}
JOLOKIA = jolokia-jvm-1.6.2-agent.jar
JOLOKIA_URL = http://search.maven.org/remotecontent?filepath=org/jolokia/jolokia-jvm/1.6.2/${JOLOKIA}
TOPDIR = /tmp/kafka-rpm
PWD = $(shell pwd)

wget:
	@wget "${TARBALL_URL}" -O ${TARBALL}

jolokia:
	@wget "${JOLOKIA_URL}" -O ${JOLOKIA}

rpm:
	@rpmbuild -v -bb \
			--define "version $(VERSION)" \
			--define "kafka_version $(KAFKA_VERSION)" \
			--define "build_number $(BUILD_NUMBER)" \
			--define "tarball $(TARBALL)" \
			--define "tarball_name $(TARBALL_NAME)" \
			--define "_sourcedir $(PWD)" \
			--define "_rpmdir $(PWD)/RPMS" \
			--define "_topdir $(TOPDIR)" \
			kafka.spec

clean:
	@rm -rf $(TOPDIR) $(PWD)/RPMS
	@rm -f $(TARBALL)

$(TARBALL):
	@spectool \
			--define "version $(VERSION)" \
			--define "kafka_version $(KAFKA_VERSION)" \
			--define "tarball $(TARBALL)" \
			-g kafka.spec
