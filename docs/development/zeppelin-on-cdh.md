---
layout: default

parent: development
title: Apache Zeppelin on CDH, Yarn
tags: 
    - 2019
    - zeppelin
---
Apache Zeppelin 과 CDH 를 연동해요.   
Yarn 리소스 매니저 관리하에 Spark 어플리케이션을 실행시킬 수 있어요.

### Zeppelin Posts
1. [Zeppelin Install & QuickStart](/development/zeppelin-quickstart/)
1. [Zeppelin Usage](/development/zeppelin-usage/)
1. [Zeppelin interpreter](/development/zeppelin-interpreter/)
1. [Zeppelin on CDH](/development/zeppelin-on-cdh/)
1. [Zeppelin Project Build](/development/zeppelin-project-build/)
1. [Zeppelin Project Upgrade 0.8.2 ](/development/zeppelin-upgrade-0.8.2/)

### Version
* Zeppelin 0.8.2 
* Cloudera CDH 6.1.x

[Zeppelin Zeppelin on CDH](https://zeppelin.apache.org/docs/0.8.2/setup/deployment/cdh.html#5-run-zeppelin-with-spark-interpreter)
공식 문서를 참고해요.

#### 설정
`/conf/zeppelin-env.sh` 파일을 수정해요. 설치 환경에 따라서 경로는 다를 수 있어요.
```bash
export MASTER=yarn-client
export SPARK_HOME='/opt/cloudera/parcels/CDH/lib/spark`
export HADOOP_CONF_DIR='etc/hadoop/conf'
```
Cloudera Manager > Yarn > Application 목록에서 Zeppelin 이 실행중인걸 확인 할 수 있어요.

#### 확인코드
```scala
%spark
val df = spark.read.option("inferSchema", "true").csv("hdfs:///tmp/sample_07.csv")
df.show()
```
테스트 코드도 잘 작동해요.

#### 문제해결
* Permission Error 가 보인하면 HDFS 에 zeppelin 사용자 디렉토리 `/user/zeppelin` 를 만들어 주세요.

* Zeppelin 0.8.1 버전을 사용하신다면, 위의 확인 코드가 아래 이슈로 오류가 발생할 수 있어요.  
Issue [ZEPPELIN-3939](https://issues.apache.org/jira/browse/ZEPPELIN-3939)
0.8.2 버전에서 Fix([Github ZEPPELIN-3939](https://github.com/apache/zeppelin/pull/3290)) 되었네요.

