---
layout: default
nav_exclude: true
parent: development
title: Apache Zeppelin Project Build
tags:
    - 2019
    - zeppelin
---

Zeppelin 소스 코드를 빌드해봐요. 오픈소스 수정은 선호하진 않지만, 
Frontend 화면 수정은 필요할 것 같아요.  
**Personalized** 기능이 필요한데 0.8.2 버전에서 
Bug [ZEPPELIN-3065](https://issues.apache.org/jira/browse/ZEPPELIN-3065) 가 있어요.

### Zeppelin Posts
1. [Zeppelin Install & QuickStart](/development/zeppelin-quickstart/)
1. [Zeppelin Usage](/development/zeppelin-usage/)
1. [Zeppelin interpreter](/development/zeppelin-interpreter/)
1. [Zeppelin on CDH](/development/zeppelin-on-cdh/)
1. [Zeppelin Project Build](/development/zeppelin-project-build/)
1. [Zeppelin Project Upgrade 0.8.2 ](/development/zeppelin-upgrade-0.8.2/)


### Versions
* Zeppelin 0.8.2
* Git Any
* Maven 3.1 or igher
* JDK 1.7
* Mac, IntelliJ

> 제환경은 OpenJDK 1.8 이예요. 빌드는 잘 되요.

[Build Zeppelin](http://zeppelin.apache.org/docs/0.8.2/setup/basics/how_to_build.html#build-requirements)
공식 문서 링크

### Project Build
#### Download source code
stable 버전으로 하시는게 정신건강에 좋아요.
```
git clone -b v0.8.2 https://github.com/apache/zeppelin.git zeppelin
```

#### Maven build
```bash
./dev/change_scala_version.sh 2.11
# build zeppelin with all interpreters and include latest version of Apache spark support for local mode.
mvn clean package -DskipTests -Pspark-2.0 -Phadoop-2.4 -Pr -Pscala-2.11
```
IntelliJ 에서는
View > Tool Window >  Maven > *Execute Maven Goal*

#### 문제해결
R 관련 오류가 발생하는데, R interpreter 를 빌드에서 제외하길 원하시면 `-Pr` 옵션을 제거하고 다시 빌드하면 성공해요.

