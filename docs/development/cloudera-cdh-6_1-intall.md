---
layout: default
nav_exclude: true
parent: development
title: Cloudera CDH 6.1.1 설치하기
tags: 
    - 2019
    - cloudera-cdh6
    - installation
---


ASIS 플랫폼의 고도화 일환으로 빅데이터 플랫폼을 신규로 구축하게 되었어요.
구축과정의 일환인 Cloudera CDH 6.1.1 설치과정을 뒤늦게사나마 정리해볼게요.
설치를 진행하기 전에 플랫폼 아키텍처의 설계와 물리서버 사양의 선택, 랙 배치 등이 우선되었겠죠?
이것에 대해서는 또 정리하도록 할게요.

설치 과정은 크게 3단계로 진행되요.

1. 설치하기 전에 
1. Cloudera Manager 설치
1. CDH 구성요소 설치

Cloudera CDH 6.1 버전의 공식 문서를 참고해서 진행했어요. 

[Cloudera Enterprise 6.1 Document](https://docs.cloudera.com/documentation/enterprise/6/6.1.html)

[Cloudera Installation Guide](https://docs.cloudera.com/documentation/enterprise/6/6.1/topics/installation.html)

### 버전 
* CentOS 7.6.1810
* Java 1.8
* CDH 6.1.1 Express (free edition)

> 도메인은 example.com 으로 표기할게요. Repository 는 util01.example.com 호스트, 
Cloudera Manager 는 util02.example.com 호스트, Database 는 db01.example.com 에 설치했어요.

> 사용된 명령어들은 운영체제와 버전등의 상황에 따라 다를수 있으니 섹션에 맞는 작업을 진행하면 되요.

> Kerberos 인증, 이중화 관련 내용은 빠져 있어요.

## 설치하기 전에
Cloudera 가이드 문서 
[Before you Install](https://docs.cloudera.com/documentation/enterprise/6/6.1/topics/installation_reqts.html)
과정 이예요. 
이 과정에서는 설치패키지들의 관리와 운영체제 설정을 다루고 있어요.
Repository 구성을 제외하고 모든 물리 서버에 동일하게 구성해요.

### Configure Network Names
#### Set hostname, Edit /etc/sysconfig/network
```sh
sudo hostnamectl set-hostname util01.example.com
sudo echo 'HOSTNAME=util01.example.com' >> /etc/sysconfig/network
```

#### Edit /etc/hosts
```sh
192.168.100.101 util01.example.com util01
192.168.100.102 util02.example.com util02
192.168.100.103 master01.example.com master01
...
```
DNS 를 이용할경우 PTR(역방향조회) 설정이 되어 있어야 해요.

#### 확인해보기
```sh
uname -a
/sbin/ifconfig
host -v -t A $(hostname)
```

### Disabling the Firewall
방화벽을 사용할경우 포트사용목록에 나열된 모든 포트를 허용 해야해요.
```sh
sudo systemctl stop firewalld
sudo systemctl disable firewalld
```

> [CDH Components Ports](https://docs.cloudera.com/documentation/enterprise/latest/topics/cdh_ports.html)

> [Cloudera Manager Ports](https://docs.cloudera.com/documentation/enterprise/latest/topics/cm_ig_ports_cm.html)

### Setting SELinux mode
`getenforce` 명령어로 정책을 해서 `enforcing` 일경우 
*/etc/selinux/config* 편집하여 `SELINUX=enforcing` 항목을 
`SELINUX=permissive` 로 변경해요.

재부팅 하거나 `setenforce 0` 명령어로 즉시 반영해줘요.
SELinux는 설치가 종료된 후 정상화(`setenforce 1`) 해도되요.

### Enable an NTP Service
`yum install ntp` NTP를 설치하고, */etc/ntp.conf* 파일을 수정하여 NTP 서버를 추가합니다.
```
server 0.pool.ntp.org
server 1.pool.ntp.org
server 2.pool.ntp.org
```
`sudo systemctl start ntpd` 서비스를 시작하고, 
`sudo systemctl enable ntpd` 부팅시 실행되도록 서비스 활성화 해주세요.


### Install Python2.7 on Hue hosts
Hue 가 서비스되는 호스트에는 Python2.7 버전이 필요해요.

### nproc 구성
설치시 자동 구성되는데, 
*/etc/security/limits.conf* 값은 */etc/security/limits.d/* 값에 의해 무시될 수 있어요.
nproc 값은 65536, 262144 로 충분히 높게 설정하세요.

### 내부 Parcel Repository 구성
Cloudera Software Repository 를 사용할경우, 항상 최신버전을 설치하게되요. 
인터넷이 차단된 상황이거나 추후에 동일 버전으로 클러스터를 확장하기 위해서 
내부 Repository 를 구성해야해요.
Cloudera CDH 구성요소를 설치 할때 Parcel 파일을 사용하게 되요.

#### 다운로드 서버
`sudo yum install httpd` 웹서버를 설치하고, 
Apache HTTP Server 설정파일 */etc/httpd/conf/httpd.conf* 의 Listen 포트도 주정해주고, 
MIME 도 추가해주세요.
```
Listen 18090

<IfModule mime_module> 
    AddType application/x-gzip .gz .tgz .parcel
```

`sudo systemctl start httpd` Apache HTTP Server 시작

#### Parcel 다운로드
##### CDH6
```sh
sudo mkdir -p /var/www/html/cloudera-repos
sudo wget --recursive --no-parent --no-host-directories https://archive.cloudera.com/cdh6/6.1.1/parcels/ -P /var/www/html/cloudera-repos
sudo wget --recursive --no-parent --no-host-directories https://archive.cloudera.com/gplextras6/6.1.1/parcels/ -P /var/www/html/cloudera-repos
sudo chmod -R ugo+rX /var/www/html/cloudera-repos/cdh6
sudo chmod -R ugo+rX /var/www/html/cloudera-repos/gplextras6
```
##### Sqoop Connectors
```
sudo mkdir -p /var/www/html/cloudera-repos
sudo wget --recursive --no-parent --no-host-directories http://archive.cloudera.com/sqoop-connectors/parcels/latest/ -P /var/www/html/cloudera-repos
sudo chmod -R ugo+rX /var/www/html/cloudera-repos/sqoop-connectors
```

http://util01.example.com/cloudera-repos/ 저장소를 확인해보세요.


### 내부 Package Repository 구성
Cloudera Manager 는 Package 를 이용해서 설치해요. 그전에 Package Repository 를 구성해줘요.
#### Package 다운로드
```
sudo wget --recursive --no-parent --no-host-directories https://archive.cloudera.com/cm6/6.1.1/redhat7/ -P /var/www/html/cloudera-repos
sudo wget https://archive.cloudera.com/cm6/6.1.1/allkeys.asc -P /var/www/html/cloudera-repos/cm6/6.1.1/
sudo chmod -R ugo+rX /var/www/html/cloudera-repos/cm6
```
*/var/www/html/cloudera-repos/cm6/6.1.1/redhat7/yum/cloudera-manager.repo* 
파일의 `baseurl` 의 주소를 수정해 주세요.

## Cloudera Manager 설치
### Package Repository 등록
util01.example.com 호스트에 설치한 내부 Package Repository 를 등록해요.
```sh
sudo wget http://util01.example.com:18090/cloudera-repos/cm6/6.1.1/redhat7/yum/cloudera-manager.repo -P /etc/yum.repos.d/
sudo rpm --import http://util01.example.com/cloudera-repos/cm6/6.1.1/redhat7/yum/RPM-GPG-KEY-cloudera
```

### Install JDK
`sudo yum install oracle-j2sdk1.8` 설치경로는 /usr/java/<installed version> 입니다.

### Install Cloudera Manager 
```
sudo yum install cloudera-manager-daemons cloudera-manager-agent cloudera-manager-server
```

### Database 설치 및 구성
Database 는 Cloudera Manager, Oozie Server, Hive Metastore Server, Hue Server 에서 사용해요.

Database 는 클러스터 외부의 호스트에 설치해주세요.
MySQL, MariaDB, PostgreSQL, Oracle 를 지원해요.
설치하는 방법은 Cloudera 문서 
[Installing and Configuring Databases]
(https://docs.cloudera.com/documentation/enterprise/6/6.1/topics/cm_ig_installing_configuring_dbs.html#concept_r5p_brw_vcb
sudo yum install mariadb-server)
로 대체할게요.
Cloudera 문서에는 Database 의 권장설정을 제시하고 있어요. 
권장설정을 따라주세요.

```
sudo systemctl enable mysqld
sudo systemctl start mysqld
```
MySQL로 설치했어요. 서비스등록하고, 데이터베이스 시작해주세요.
`sudo /usr/bin/mysql_secure_installation` 보안설정도 진행해주세요.

#### Creating Databases for Cloudera Software
Cloudera 의 각 서비스들이 사용할 database 들을 생성해주고, 
사용자 권한 설정 작업을 해주어야해요.

Database 가 설치된 호스트 서버에서 `mysql -u root -p` MySQL에 root 로 접속해주세요.
```
CREATE DATABASE  <databaseName> DEFAULT CHARARCTER SET <characterSet> DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON <databaseName>.* TO  '<userName>'@'%' IDENTIFIED BY '<password>';
```
생성해야 하는 Database 는 아래와 같아요.

| Service           | Database      | UserName      |
| ---               | ---           | ---           |
| Cloudera Manager  | scm           | scm           |
| Activity Monitor  | amon          | amon          |
| Reports Manager   | rman          | rman          |
| Hue               | hue           | hue           |
| Hive Metastore    | metastore     | metastore     |
| Sentry Server     | sentry        | sentry        |
| Oozie             | oozie         | oozie         |

잘 만들어졌는지 확인도 해볼게요.
```
show databases;
show grants for '<userName>'@'%';
```

#### Installing JDBC Driver
Database 를 사용하는 서버들에는 JDBC Driver 가 설치되어 있어야 하는데요.
우선 Cloudera Manager 를 설치할 util02.example.com 호스트 서버에 설치 해주세요.
Cloudera 는 MySQL 같은 경우 5.1 버전의 JDBC Driver 를 추천하고 있네요.

```
wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.46.tar.gz
tar zxvf mysql-connector-java-5.1.46.tar.gz
sudo mkdir -p /usr/share/java/
cd mysql-connector-java-5.1.46
sudo cp mysql-connector-java-5.1.46-bin.jar /usr/share/java/mysql-connector-java.jar
```

### Set up the Cloudera Manager Database
Cloudera Manager, Database 가 동일한 호스트인지 서로 다른 호스트인지에 따라 방법이 다른데요. 
이 문서에서는 서로다른 서버에 설치하였어요.

##### Databse와 Cloudera Manager 를 하나의 Host에 설치한 경우
```
sudo /opt/cloudera/cm/schema/scm_prepare_database.sh <databaseName> <databaseUser>;
```
##### Database와 Cloudera Manager 가 서로 다른 Host인 경우
```
sudo /opt/cloudera/cm/schema/scm_prepare_database.sh mysql -h <dbDomain> --scm-host <cmDomain> <databaseName> <databaseUser>;
# 예를들면
sudo /opt/cloudera/cm/schema/scm_prepare_database.sh mysql -h db01.example.com --scm-host util02.example.com scm scm
```


## CDH 및 기타 소프트웨어 설치
Cloudera Manager 설치를 마쳤어요. 
이제 Cloudera Manager Server 를 실행하고, Admin Console 에 접속하면 CDH 설치가 시작되요.

`sudo systemctl start cloudera-scm-server` Cloudera Manager Server 를 시작해요.
http://util02.example.com:7180/ 주소를 통해 Cloudera Manager 관리 콘솔에 접속합니다. 
최초 로그인 정보는 `admin` 입니다.

> CDH 는 Package 와 Parcels 로 설치가능한데, Cloudera는 Parcels 설치를 권장하고 있어요. 
이유는 롤링 업그레이드 가능하기 때문이예요. 

> 이 문서에서는 TLS 설정을 하지않고 진행했어요.

### Parcel Repository 등록
* Cloudera Manager WebUI > Navigaton bar > Hosts > parcels > Configuration
* Cloudera Manager WebUI > Menu > Administration > Settings > Category > Parcels

위의 두 메뉴에서 원격 Repository URL 
*http://util01.example.com:18090/cloudera-repos/cdh6/6.1.1/parcels/*
을 등록 할 수 있어요.
    
### SSH 설정 
각 호스트에 SSH 접속하여 설치가 진행되는데, root 비밀번호를 이용하거나, 
공개키 설정이 되어 있어야 해요. 

### 설치 마법사
대부분 설치마법사가 이끈는 대로 따라가면 되고, 확인이 필요한 부분은 
Cloudera 문서 [Install CDH and Other Software]
(https://docs.cloudera.com/documentation/enterprise/6/6.1/topics/install_software_cm_wizard.html)
를 참고해 주세요.

#### Host Inspector 
CDH 설치를 완료하면, Host Inspector 를 수행하고 아래와 같은 경고가 보일 수 있어요.

* *Transparent Huge Page Compaction이 설정되었으며 심각한 성능 문제를 일으킬 수 있습니다.*
    * [Transparent Huge Page](https://allthatlinux.com/dokuwiki/doku.php?id=thp_transparent_huge_pages_%EA%B8%B0%EB%8A%A5%EA%B3%BC_%EC%84%A4%EC%A0%95_%EB%B0%A9%EB%B2%95)
    메모리를 많이 사용하는 플랫폼에서는 설정을 꺼주는게 좋아요. 

* *Starting with CDH 6, PostgreSQL-backed Hue requires the Psycopg2 ...*
    * Hue 서비스는 Python 2.7 을 필요로해요. 앞에서 이미 설정했어요.

### 클러스터 생성
Cloudera 문서 
[Recommended Role Distribution]
(https://docs.cloudera.com/documentation/enterprise/6/6.1/topics/cm_ig_host_allocations.html)
를 참고해서 Cluster 의 서비스 역할을 각 호스트에 어떻게 배치 할지에 대해 미리 계획을 세워두세요.

Cluster 를 생성하고, 사용자 지정 서비스를 선택하여, 
HDFS, Hive, Hue, Impala, Kafka, Oozie, Spark, YARN, ZooKeeper를 설치하면되요.
