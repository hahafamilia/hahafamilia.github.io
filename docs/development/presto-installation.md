---
layout: default
parent: development
title: Presto 설치, PrestoDB, PrestoSQL
tags: 
    - 2020
    - bigdata
    - presto
---



Cloudera CDH 위에서 Presto 엔진을 싱글 서버로 사용할 계획에 Presto 를 설치하려는데, 0.230 버전, 328 버전이 어떤걸 써야 할지 모르겠어요.
좀 더 알아보니 PrestoDB, PrestoSQL 두개로 나뉘는군요. 
[Presto, PrestoDB, PrestoSQL](https://blog.openbridge.com/what-is-facebook-presto-presto-database-or-prestodb-a-powerful-sql-query-engine-77d4c4a66d4)
의 차이를 설명한 문서예요. 요약하자면 PrestoDB를 사용하라는 겁니다. 
* Facebook에서 Presto 오픈소스 프로젝트를 공개했고 이것이 PrestoDB(https://prestodb.io/)
* Fracebook에서 3인의 개발자가 분사하여 만든 프로젝트가 PrestoSQL(https://prestosql.io/)

### Version
* PrestoDB 0.230
* CentOS
* Java8

### Presto 설치
[Download Link](https://repo1.maven.org/maven2/com/facebook/presto/presto-server/0.230/presto-server-0.230.tar.gz)
```
tar xvzf presto-server-0.230.tar.gz
cd presto-server-0.230
mkdir etc
cd etc
touch config.properties log.properties node.properties jvm.config
mkdir catalog
cd catalog
touch jmx.properties hive.properties
```

etc/config.properties
```
node-scheduler.include-coordinator=true
http-server.http.port=8080
query.max-memory=5GB
query.max-memory-per-node=1GB
query.max-total-memory-per-node=2GB
discovery-server.enabled=true
discovery.uri=http://domain:8080
```

etc/log.properties
```
com.facebook.presto=INFO
```

etc/node.properties
```
node.environment=production
node.id=presto01
node.data-dir=/var/presto/data
```

etc/jvm.config
```
-server
-Xmx16G
-XX:+UseG1GC
-XX:G1HeapRegionSize=32M
-XX:+UseGCOverheadLimit
-XX:+ExplicitGCInvokesConcurrent
-XX:+HeapDumpOnOutOfMemoryError
-XX:+ExitOnOutOfMemoryError
```

etc/catalog/jmx.properties
```
connector.name=jmx
```

etc/catalog/hive.properties
```
connector.name=hive-hadoop2
hive.metastore.uri=thrift://hiveserver2:9083
hive.config.resources=/etc/hadoop/conf/core-site.xml,/etc/hadoop/conf/hdfs-site.xml
```

run start
bin/launcher start
bin/launcher run
nohup ./launcher run &

log
/var/log 
launcher.log server.log http-request.log


### Presto CLI
[Download Presto CLI](https://repo1.maven.org/maven2/com/facebook/presto/presto-cli/0.230/presto-cli-0.230-executable.jar)

```
mv presto-cli-0.230-executable.jar presto
chmod +x
./presto --server localhost:8080 --catalog hive --schema default
presto> show tables from default;
```

### JDBC Driver
[Download JDBC Driver](https://repo1.maven.org/maven2/com/facebook/presto/presto-jdbc/0.230/presto-jdbc-0.230.jar)

JDBC URL
```
jdbc:presto://host:port
jdbc:presto://host:port/catalog
jdbc:presto://host:port/catalog/schema
```

### Multiple MySQL Conenctor

etc/catalog/db1.properties
```
connector.name=mysql
connection-url=jdbc:mysql://db1.example.com:3306
connection-user=username
connection-password=password
```

etc/catalog/db2.properties
```
connector.name=mysql
connection-url=jdbc:mysql://db2.example.com:3306
connection-user=username
connection-password=password
```

[catalog].[database].[table]

```
./presto --server localhost:8080 
presto> show schemas from db1;
presto> show schemas from db2;
```


[Cloudera Community Preso](https://www.linkedin.com/pulse/hello-presto-blog-1-thanks-facebook-neeraj-sabharwal)
[Presto Install](https://prestodb.io/docs/current/installation/deployment.html)
