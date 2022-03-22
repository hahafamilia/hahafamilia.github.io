---
layout: default
nav_exclude: true
parent: development
title: Kafka Manager 설치
tags: 
    - 2019
    - kafka
    - kafka-manager
    - installation
---

## KafkaManager 설치
[Kafka Manager](https://github.com/yahoo/kafka-manager) 를 설치해 볼게요.
Kafka Manager 는 Yahoo 의 오픈소스 인데, Kafka 서비스의 상태를 확인하거나, 
*Skew* 등이 발생했을때 *Reassign Partitoin* 등을 할 수 있는 기능을 제공해줘요.


https://hahafamilia.github.io/bigdata/kafka-broker-reinstall/
Github 에서 다운로드 한 후, Scala 빌드 빌드툴 `sbt` 로 빌드 해줘요.

```
tar -xvzf kafka-manager-1.3.3.22.tar.gz cd kafka-manager-1.3.3.22
PATH=/usr/java/jdk1.8.0_141-cloudera/bin:$PATH JAVA_HOME=/usr/java/jdk1.8.0_141-cloudera \
./sbt -java-home /usr/java/jdk1.8.0_141-cloudera clean dist
cp target/universal/kafka-manager-1.3.3.22.zip /usr/local
cd /usr/local
unzip kafka-manager-1.3.3.22.zip
```

*conf/application.conf* 설정파일에 Zookeeper 호스트 주소를 설정해 줘요.
```
kafka-manager.zkhosts="zook01.example.com:2181,zook02.example.com:2181,zook03.example.com:2181"
```

Kafka Manager 를 실행해요.

```
/usr/local/kafka-manager-1.3.3.22/bin/kafka-manager \
-java-home /usr/java/jdk-1.8.0_181-cloudera \
-Dconfig.file=/usr/local/kafka-manager-1.3.3.22/conf/application.conf -Dhttp.port=18090
```

Cloudera Manager 웹 콘솔 Kafka 서비스 구성 메뉴에서, 
Kafka JMX 의 바인딩 포트를 0.0.0.0 으로 변경 해줘요.
```
# Additional Broker Java Options(borker_java_opts)
-Dcom.sun.management.jmxremote.host=0.0.0.0 -Dcom.sun.management.jmxremote.local.only=true
```
> JMX Server 포트는 127.0.0.1 로 바인딩되어 공인IP 접속이 불가능 해요.
