---
layout: default
nav_exclude: true
parent: development
title: Cloudera CDH Configuration
tags:
    - 2020
    - cloudera-cdh6
    - configuration
    - troubleshooting
---
Bigdata 플랫폼으로 Cloudera CDH 6.1.x 를 운영중 트러블슈팅과 설정에 대해 이야기 해볼게요.

### Version
* Cloudera CDH 6.1
* Oracl Java 1.8

## YARN
### Turning YARN
YARN 의 리소스 관련 설정의 기본 값 
[Default Memory Setting](https://docs.cloudera.com/documentation/enterprise/6/6.3/topics/cm_mc_yarn_service.html#id_qv5_4ts_3q)

YARN 리소스 튜닝 방법
[Turning YARN](https://docs.cloudera.com/documentation/enterprise/6/6.3/topics/cdh_ig_yarn_tuning.html)

노드의 전체 가용 리소스에서 서비스 데몬들의 리소스 사용량을 제하고
리소스를 할당 해요.
튜닝 문서와는 다르게 Cloudera Manager 에서 각 호스트들의 리소스 사용량은 상이해요.
튜닝 문서와 *Cloudera Manager > Host > Worker > Resource*  리소스 사용량을 참고하여
Yarn 에 할당할 CPU, Memory 를 결정한 후, 아래의 프로퍼티에 값을 설정해요.
Impala, Kudu, Hbase 를 사용중이면 추가적인 메모리 할당이 필요해요.
```
yarn.nodemanager.resource.cpu-vcores
yarn.nodemanager.resource.memory-mb

yarn.scheduler.minimum-allocation-vcores
yarn.scheduler.maximum-allocation-vcores
yarn.scheduler.increment-allocation-vcores

yarn.scheduler.minimum-allocation-mb | 1G
yarn.scheduler.maximum-allocation-mb | 101G
yarn.scheduler.increment-allocation-mb | 512M
```

## Hive
### HA
공식 문서 [Configuration HiveServer2 HA](https://docs.cloudera.com/documentation/enterprise/6/6.1/topics/admin_ha_hiveserver2.html)

#### 절차
1. HAProxy 설정
1. HiveServer2 인스턴스를 추가
1. Locate the HiveServer 2 Load Balancer property
1. Set hostname:port
1. Restart Hive

#### Check 
* Hive on Spark
* Oozie job
* Hue Hive / Impala query
* scdh api, Impala JDBC
* Zeppelin Hive JDBC

> Oozie job 들은 Hive LB 주소로 변경되어야 하며 스케쥴은 재제출되어야 해요.  
> Impala, Oozie Server 는 HiveServer2 설정은 없지만, Restart 필요할 수 있어요.

### Hive Metastore Server HA
Metastore HA 는 Load balance 기능은 없고 
장애시 failover 를 진행 하도록 구성 할 수 있어요.

## Impala
### timezone
bigint 시간 값을 `from_unixtime()` 함수를 통해 문자열로 변환하여 사용할 경우, 
Hive 같은 경우 현지 timezone 이 적용되는데, Impala 같은 경우 UTC 기준 변환되요.

Impala 구성 *Impala Daemon 명령줄 인수 고급 구성* 메뉴에 아래와 같이 설정하여 
현지 timezone 을 따르게 할 수 있어요.
```
--use_local_tz_for_unix_timestamp_conversions=true 
--convert_legacy_hive_parquet_utc_timestamps=true
```

### Impala 쿼리 Oozie Workflow 등록
Bash 쉘을 통해 `impala-shell` CLI 를 사용해서 Shell 을 실행하거나 
Impala 쿼리를 Oozie Workflow 를 등록하여 배치를 작성할 수 있는데요.
`PYTHON_EGG_CACHE` 오류가 발생 할 수 있어요. Shell 상단에 캐시 경로를 지정해 주면 되요.
```bash
export PYTHON_EGG_CACHE=/tmp/.python-eggs
```

## Oozie
### Schedule Timezone
Oozie Server 에 Workflow 를 예약등록 할때 사용되어지는 Timezone 을 변경해야해요.
Oozie 구성 *oozie-site.xml에 대한 Oozie Server 고급 구성* 에 값을 추가하여 설정해요.
```
oozie.processing.timezone
GMT+0900
```

### Capture output 오류
Workflow 실패의 원인 중에 `capture output` 을 사용할 경우, 
output 사이즈가 기본설정값(2048) 을 초과하여 오류가 발생 할 수 있어요.
Oozie 구성 *action-conf/default.xml 에 대한 Oozie Server 고급 구성* 에 
값을 추가하여 사이즈 설정 할 수 있어요.
```
oozie.action.max.output.data
10240
```

## Hue
### Timezone
Hue UI의 Timezone 설정은 *time_zone* 에 값을 `Asis/Seoul` 변경해요.

## Kafka
### Kafka Manager Jmx
[Kafka Manager](https://github.com/yahoo/kafka-manager)
는 Kafka 클러스터를 모니터링 할 수 있는 좋은 도구 인데요. 
Kafka Jmx 서버에 접속하여 매트릭스를 수집해요. 
그런데, Kafka 는 JMX 서버를 127.0.0.1 로 바인딩하기 때문에, 공인/사설 IP 간의 접속이 불가능해요.
Kafka 구성 *Additional Broker Java Optoins* 설정에서 Jmx 포트를 0.0.0.0 으로 바인딩 해주세요.
```
-Dcom.sun.management.jmxremote.host=0.0.0.0 -Dcom.sun.management.jmxremote.local.only=true
```

### Kafka Broker
역시나 공인/사설 환경에서 producer API 서버에서 Kafka Broker 에 접속하기 위해서는 
Kafka Broker 서버를 0.0.0.0 으로 바인딩 해야 해요.
Kafka 구성 *kafka.properties에 대한 Kafka Broker 고급 구성* 설정에서 
각 Borker 마다 아래와 같이 설정해주세요.
```
#listeners=PLAINTEXT://0.0.0.0:9092
#advertised.listeners=PLAINTEXT://[공인IP]:9092
```