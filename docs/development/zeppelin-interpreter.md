---
layout: default

parent: development
title: Apache Zeppelin Interpreter, Hive, Impala
tags: 
    - 2019
    - zeppelin
---

[Apache Zeppelin](https://zeppelin.apache.org/) 과 Cloudera CDH 의 Hive, Impala 를 연동하는 방법을 알아볼게요.

### Zeppelin Posts
1. [Zeppelin Install & QuickStart](/development/zeppelin-quickstart/)
1. [Zeppelin Usage](/development/zeppelin-usage/)
1. [Zeppelin interpreter](/development/zeppelin-interpreter/)
1. [Zeppelin on CDH](/development/zeppelin-on-cdh/)
1. [Zeppelin Project Build](/development/zeppelin-project-build/)
1. [Zeppelin Project Upgrade 0.8.2 ](/development/zeppelin-upgrade-0.8.2/)



### Environment
* Oracle JDK 1.8
* CentOS 7
* Zepplin 0.8.1
* Cloudera CDH 6.1.1
* Hive 2.1.1
* Impala 3.1.0
* Impala JDBC Driver 2.6.12

### Hive
[Zeppelin Hive Interpreter Document](https://zeppelin.apache.org/docs/0.8.0/interpreter/hive.html)
문서를 보면 Jdbc Interpreter 를 사용하라고 되어있네요. 
기본으로 PostgreSQL Connector 지원하고 그외는 Connector 는 추가를 해줘야 해요.

![Menu Interpreter](/assets/images/2019/2019-08-30-14-16-05.png)

#### Maven Repository
Zeppelin 콘솔에서 우측 상단의 메뉴에서 `interpreter` 메뉴를 클릭하여 Interpreter 설정 화면으로 이동해요. 
`Repository` 버튼을 클릭하면 등록되어져 있는 Repository 를 확인 할 수 있어요. 
그 옆으로 `+` 버튼 클릭해서 Cloudera Maven Repository 
`https://repository.cloudera.com/artifactory/cloudera-repos/` 를 추가 해주세요.

![Add Repository](/assets/images/2019/2019-08-30-14-46-45.png)

#### Hive Interpreter 추가
`Create` 버튼을 클릭하여 Interpreter 를 추가 해요. Interpreter Group 은 `jdbc` 로하고 아래의 Properties, Dependencies 값 조정해 주세요.

![Add Interpreter](/assets/images/2019/2019-08-30-14-49-53.png)

##### Properties
* default.driver : `org.apache.hive.jdbc.HiveDriver`
* default.url : `jdbc:hive2://<HiveServer2>:10000`

##### Dependencies artifact
* `org.apache.hive:hive-jdbc:2.1.1-cdh6.1.1`
* `org.apache.hadoop:hadoop-common:3.0.0-cdh6.1.1`

> [CDH 6.1.x Maven Artifacts](https://www.cloudera.com/documentation/enterprise/6/release-notes/topics/rg_cdh_61_maven_artifacts.html#concept_2gp_d8n_yk)

### Impala
Cloudera 는 Impala JDBC Connector 를 Maven 으로 제공하고 있지 않아요.
Zeppelin 설치 경로에 `external-lib/impala` 디렉토리를 생성하고 
[Impala JDBC Download](https://www.cloudera.com/downloads/connectors/impala/jdbc/2-6-12.html)
링크를 통해 다운로드 해주세요.

`Interpreter Name` 은 `impala` 로, `Interpreter Group` 은 `jdbc` 로 Interpreter 를 생성하고 Properties, Dependencies 값을 조정해 주세요.

##### Properties 
* default.driver : `com.cloudera.impala.jdbc41.Driver`
* default.url : `jdbc:impala://<ImpalaServer>:21050/scdh;AuthMech=0;`
> Properties `default.user` 에 기본값이 들어가 있네요. 저는 삭제 했어요.

##### Denpendies artifact
* `/opt/zeppelin/external-lib/impala/ImpalaJDBC41.jar` (Download 한 jar 파일의 경로)
> `AuthMech=0` 권한 설정을 하지 않았어요. Impala JDBC 권한 설정은 
[Impala JDBC Document](https://www.cloudera.com/documentation/other/connectors/impala-jdbc/latest.html)
문서를 참고해 주세요.

### Notebook
잘 연동 되었느지 확인해 볼게요. Note 를 생성하고 `Interpreter binding` 메뉴에서 `impala`, `hive` Interpreter 를 상단으로 올려주세요.

![Note Interpreter binding](/assets/images/2019/2019-08-30-15-28-22.png)

Hive 와 Impala 쿼리가 잘 동작하네요. 

![Note Paragraph](/assets/images/2019/2019-08-30-15-34-23.png)


### Spark
Zeppelin 은 Spark 가 임베디드 되어있는데, 버전 이 2.2.1 이네요.
새로운 버전의 Spark 를 설치하고 `/opt/zeppelin/conf/zeppelin-env/sh` 파일에서 `SPARK_HOME` 을 설정해 주시면 되요.
[Spark Interpreter Doc](https://zeppelin.apache.org/docs/0.8.2/interpreter/spark.html)
문서에 잘 설명되어 있어요.

```shell
export SPARK_HOME=<스파크설치경로>
```
