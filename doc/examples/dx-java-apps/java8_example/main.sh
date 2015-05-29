#!/bin/bash
set -ex

export CLASSPATH=${DX_FS_ROOT}/:$CLASSPATH

# Make java 8 the default JRE
sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java 2000

# Add the following line if you need a javac as well
#
# sudo update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/java-8-openjdk-amd64/bin/javac 2000

# You can examine the output to verify that Java 8 is installed and working
java -version

java DXHelloWorld
