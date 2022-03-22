---
layout: default
nav_exclude: true
parent: development
title: Zabbix 모니터링 메모
tags: 
    - 2018
---

### Version
* zibbix 3.4
* Ubuntu 16.0
* Centos 6

#### Server Install
[Install Zabbix Server](https://tecadmin.net/install-zabbix-on-ubuntu/#)
EC2 설치시 Ubuntu로 설치 관련 글에 AGent, WEB 설정 등이 상세함.

```
sudo apt-get install libapach2-mod-php
/usr/share/zabbix/conf/zabbix.conf.php
```

> server port 10051

#### Agent Install
[Install Zabbix Agent](https://tecadmin.net/install-zabbix-agent-on-centos-rhel/)
```
rpm -Uvh http://repo.zabbix.com/zabbix/3.4/rhel/6/x86_64/zabbix-release-3.4-2.el6.noarch.rpm
rpm -Uvh http://repo.zabbix.com/zabbix/3.4/rhel/6/x86_64/zabbix-release-3.4-1.el6.noarch.rpm
yum install zabbix-agent
```

[Language](https://www.zabbix.org/wiki/How_to/install_locale)

[Add Agent to Server](https://tecadmin.net/add-host-zabbix-server-monitor/)

[Manual](http://manual.oplab.co.kr/doku.php/manual/config/items/itemtypes/snmp)

#### Tomcat jmx monitoring
```
wget http://apache.mirror.cdnetworks.com/tomcat/tomcat-8/v8.0.49/bin/extras/catalina-jmx-remote.jar
```

```
JAVA_OPTS="$JAVA_OPTS -Dcom.sun.management.jmxremote -Djava.rmi.server.hostname=HOST_SERVER_IP \
	-Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false"
JAVA_OPTIONS="$JAVA_OPTIONS -Dcom.sun.management.jmxremote"
JAVA_OPTIONS="$JAVA_OPTIONS -Dcom.sun.management.jmxremote.port=8420"
JAVA_OPTIONS="$JAVA_OPTIONS -Dcom.sun.management.jmxremote.ssl=false"
JAVA_OPTIONS="$JAVA_OPTIONS -Dcom.sun.management.jmxremote.authenticate=false"
```

#### Nginx monitoring
https://github.com/oscm/zabbix/tree/master/nginx

#### Zabbix Template
[oscm/zabbix](https://github.com/oscm/zabbix)
[share/zabbix](https://share.zabbix.com/operating-systems/linux/tcp-connection-status-template-for-zabbix-3-4)

