---
layout: default
nav_exclude: true
parent: development
title: Apache Zeppelin Upgrade from 0.8.1 to 0.8.2
tags: 
    - 2019
    - zeppelin
---

Apache Zeppelin 0.8.2 버전이 2019.11.29 일에 Release 되었어요.
0.8.1 버전에서 발견되었던 버그들도 수정이 되었으니 업그레이드를 진행 해보도록 할게요.

### Zeppelin Posts
1. [Zeppelin Install & QuickStart](/development/zeppelin-quickstart/)
1. [Zeppelin Usage](/development/zeppelin-usage/)
1. [Zeppelin interpreter](/development/zeppelin-interpreter/)
1. [Zeppelin on CDH](/development/zeppelin-on-cdh/)
1. [Zeppelin Project Build](/development/zeppelin-project-build/)
1. [Zeppelin Project Upgrade 0.8.2 ](/development/zeppelin-upgrade-0.8.2/)

[Apache Zeppelin 0.8.2 Upgrading](http://zeppelin.apache.org/docs/0.8.2/setup/operation/upgrading.html)
문서를 보니 0.8.x 버전에서의 업그레이드는 `conf` 와 `notebook` 디렉토리를 복사해주기만 하면 된다고 하니 손쉽게 진행 될 것으로 예상되요.

## 업그레이드
[Apache Zeppelin Download](http://zeppelin.apache.org/download.html)
다운로드 사이트에서 바이너리 파일을 다운로드 해서,
0.8.2 버전의 설치를 마치고 `conf` 와 `notebook` 디렉토리 옮겨준 후 서버를 구동하니 사이트가 정상적으로 열리네요.


### Interpreter
별도 추가한 interpreter 설정도 알아서 잡아주네요. 별도의 `repository` 설정을 했다라면 다운로드 하는데 시간이 조금 걸리긴해요.

`impala` 인터프리터가 사용하는 JDBC 라이브러리를 별도 디렉토리로 관리 해왔기에, 해당 디렉토리도 같이 복사해줬어요. 

### 그런데 문제가 있어요
모든 게 정상으로 보이는데 옮겨온 노트북들이 열리지 않네요. 
새로운 노트북을 생성해도 만들어지지 않구요. 
서버로그를 확인해도 특별한 오류가 보이지 않네요. 
그래서... 하나씩 하나씩 해봤어요.

원인은 `Helium` 플러그인!
Helium 차트를 사용했었는데, *conf/helium.json* 설정에 관련 정보가 있어요. 
이 설정 파일을 옮기게 되면 노트북이 작동을 안해요.

Helium 플러그인을 사용한 노트북이 많다면, 해결책을 찾아야 할텐데요.
그렇지 않다면 *helium.json* 파일은 옮기지 마시고, Zeppelin 서버를 실행해 보세요.
그리고 Helium 플러그인 기능을 다시 Enable 시키시면 되요.

