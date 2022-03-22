---
layout: default
nav_exclude: true
parent: development
title: Apache Zeppelin 설치, QuickStart
tags: 
  - 2019
  - zeppelin
---

[Apache Zeppelin](https://zeppelin.apache.org/) 은 노트북 방식의 시각화 툴이예요. 
다양한 시각화 툴이 존재하지만 '가장 좋은 것'이 아니라 '나에게 맞는 것' 을 선택했어요.
제가 Zeppelin을 선택한 이유는 아래와 같아요.

1. 설치와 사용법이 쉬워야 한다.
1. 요구사항을 유연하게 처리 할 수 있어야 한다.
1. BI 웹 어드민을 개발 하지 않아도 되도록 정적 HTML 을 제공해야 한다. 

### Zeppelin Posts
1. [Zeppelin Install & QuickStart](/development/zeppelin-quickstart/)
1. [Zeppelin Usage](/development/zeppelin-usage/)
1. [Zeppelin interpreter](/development/zeppelin-interpreter/)
1. [Zeppelin on CDH](/development/zeppelin-on-cdh/)
1. [Zeppelin Project Build](/development/zeppelin-project-build/)
1. [Zeppelin Project Upgrade 0.8.2 ](/development/zeppelin-upgrade-0.8.2/)

## Environment
* Oracle JDK 1.8
* CentOS 7
* Zepplin 0.8.1

## Zeppelin
와우! Zeppelin~ 아파치 오픈 소스 프로젝트에 채택된 국내 프로젝트네요. 
공식 문서를 보고 [Quick Start](http://zeppelin.apache.org/docs/0.8.0/quickstart/install.html) 부터 진행 해볼게요.

## Install
Oracle JDK 1.7 를 필요로 하네요. 그리고 `JAVA_HOME` 이 필요하다고 하네요.
제가 사용중인 클러스터는 Cloudera CDH 6.1.x 으로 Oracle JDK 1.8 라이센스를 보유하고 있어서, 
JDK 1.8 환경에서 설치 진행해요.
> Oracle JDK 1.8 이 상용화 되어서 사용하지 못하는게 아닐까요? 
오픈소스에서 사용시 무료 라이센스 주면 안되나... Oracle...

> `JAVA_HOME` 설정은 `readlink -f $(which java)` 의 경로를 `/etc/profile` 파일에 `export` 명령문으로 저장해주시면 되요.
> `source /etc/profile` 해주셔야 현재의 터미널에 반영됩니다. 

두 가지 버전의 [Download](http://zeppelin.apache.org/download.html)
를 제공하고 있네요. 
all interpreter 버전으로 다운로드 진행 했어요. 제 설치 경로는 `/opt` 이예요.

```shell
# 사용자 추가
useradd -s /sbin/nologin zeppelin

# 설치 디렉토리
cd /opt
tar -xvf zeppelin-0.8.1-bin-all.tgz

# 권한, 링크
chown -R zeppelin:zeppelin zeppelin-0.8.1-bin-all
ln -s zeppelin-0.8.1-bin-all zeppelin
chown -h zeppelin:zeppelin zeppelin
```

Zeppelin 설치하였으니 `/opt/zeppelin/bin/zeppelin-daemon.sh start` 시작 명령어로 실행시시켜 볼게요. 
`http://localhost:8080` 접속하시면 시작화면을 보실 수 있어요. Stop 시켜주시고, 서비스 등록을 할게요.

### Service 등록
`/usr/lib/systemd/system/zeppelin.service` 파일을 생성해 주시고, 아래의 내용을 작성해 주세요.

```shell
# CentOS 7
[Unit]
Description=Zeppelin Service
After=syslog.target network.target

[Service]
Type=forking
User=zeppelin
Group=zeppelin
Restart=always
Environment="JAVA_HOME=<java home path>"
WorkingDirectory=/opt/zeppelin
ExecStart=/opt/zeppelin/bin/zeppelin-daemon.sh start
ExecStop=/opt/zeppelin/bin/zeppelin-daemon.sh stop
ExecReload=/opt/zeppelin/bin/zeppelin-daemon.sh reload

[Install]
WantedBy=multi-user.target
```

`zeppelin.service` 파일을 작성했으면, `systemctl daemon-reload` 명령어로 반영시켜준후, 서비스 `enable` 시켜 주세요.

```shell
systemctl enable zeppelin
systemctl start zeppelin
```

### Account
Zeppelin 에 접속해 보면 `anonymous` 익명 사용자로 접속 되는데요. 익명 사용자 접근을 제한하고 계정을 생성해 볼게요.

#### Disable Anonymous Access
``` shell
cd /opt/zeppelin
cp conf/zeppelin-site.xml.template conf/zeppelin-site.xml
vi zeppelin-site.xml
```

```xml
<property>
  <name>zeppelin.anonymous.allowed</name>
  <value>false</value>
</property>

<property>
  <name>zeppelin.notebook.public</name>
  <value>false</value>
</property>

<property>
  <name>zeppelin.notebook.default.owner.username</name>
  <value>admin</value>
</property>
```

#### Enable Shiro Authentication
``` shell
cd /opt/zeppelin
cp conf/shiro.ini.template conf/shiro.ini
vi shiro.ini
```

```xml
[users]
admin = password1234, admin
user1 = password1234, role1, role2
# user2 = password3, role3
# user3 = password4, role2
```

## Explore UI
[Explore UI](https://zeppelin.apache.org/docs/0.8.1/quickstart/explore_ui.html)
섹션에는 Layout, Menu, Notebook, Paragraph 에 관한 UI 사용법이 있네요.

## Tutorial
[Tutorial](http://zeppelin.apache.org/docs/0.8.1/quickstart/tutorial.html)
에서는 LocalFile 을 사용하는 예제와 Twitter Stream 데이터를 사용하는 예제가 있어요. 

샘플데이터 [bank.zip](http://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip)
을 다운로드해서 간단히 따라해 볼 수 있어요. 
> Zeppelin 에서 Spark Interpreter 가 기본 값이어서 샘플 코드에 Interperter 지정을 안해주고 있어요. 만약 예제가 동작하지 않는다면 `RDD` 생성 코드에 `%spark` Interpreter 를 지정해 주세요.

## 마치며
다음 포스트에 계속해서 Usage 문서에 대해서 알아 볼게요. 

[여기](https://www.vultr.com/docs/how-to-install-apache-zeppelin-on-centos-7#Prerequisites)
에 Zeppelin 설치에 관해서 잘 정리되어져 있네요.
