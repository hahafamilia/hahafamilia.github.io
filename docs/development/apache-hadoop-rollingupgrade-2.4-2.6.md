---
layout: default
nav_exclude: true
parent: development
title: Apache Hadoop 롤링 업그레이드 2.4.1 to 2.6.0
tags: 
    - 2020
---

예전 하둡 플랫폼으로 10PB(2 peplica) 의 컨텐츠를 운영했던 경험이 있는데요. 
Apache Hadoop 1.x 버전에서 2.2 버전으로 서비스 중단 업그레이드, 2.2 버전에서 2.4 버전으로 2.6 버전으로 무중단 업그레이드를 진행했었습니다.
Apache Hadoop 2.4.1 버전에서 2.6.0 버전으로 Rolling Upgrade 진행했을때의 문서가 남아 있네요.
내용이 잘 정리되어 있진 않지만, 당시 작성내용을 우선 옮겨 두려고 합니다. 

* 네임노드 /data 디렉토리 백업
* 관리용 쉘 종료
```
/monitor/daemon_hdfs_status.sh		- 유지
/monitor/daemon_hdfs_balancer.sh	- 종료
/monitor/daemon_hdfs_namenode.sh	- 종료
```

* 2.6.0 설치(모든 노드에 설치하고, 환경설정을 이전버전과 동일하게 맞춥니다)
```
# 디렉토리 생성
mkdir pids logs temp
ln -s etc/hadoop/ conf
cp dfs.exclude fencing.sh topology.*  /home/hdfsnnuser/hadoop-2.6.0
cp core-site.xml hdfs-site.xml  /home/hdfsnnuser/hadoop-2.6.0/conf
```
* hadoop-env.sh( 네임노드와 데이터노드 다름)
```
#메모리 설정
export HADOOP_HEAPSIZE=61440
#로그디렉토리
export HADOOP_LOG_DIR=${HADOOP_PREFIX}/logs
#PID 디렉토리
export HADOOP_PID_DIR=${HADOOP_PREFIX}/pids

export HADOOP_COMMON_LIB_NATIVE_DIR=${HADOOP_PREFIX}/lib/native
export HADOOP_OPTS="$HADOOP_OPTS -Djava.library.path=$HADOOP_PREFIX/lib"
```

* log4j.properties
```
	log4j.logger.org.apache.hadoop.hdfs.nfs=INFO
	log4j.logger.org.apache.hadoop.oncrpc=INFO	
```
	
* `bin/hdfs dfsadmin -rollingUpgrade prepare`
* `bin/hdfs dfsadmin -rollingUpgrade query`, "Proceed with rolling upgrade:" 메시지 확인

* 관리자 웹
```
	Rolling upgrade started at 2015. 3. 17. 오후 7:12:25. 
	Rollback image has been created. Proceed to upgrade daemons.
```

* Standby Namenode 먼저 작업, shotdown 2.4.1

* Hadoop 링크 2.4.1 에서 2.6.0 버전 설치 경로로 변경

* 2.6 버전의 네임노드 업그레이드 시작, `bin/hdfs namenode -rollingUpgrade started > /dev/null &`
> 네임노드 Safemode off 확인

* HA 전환

* 나머지 Namenode 도 동일 작업 직행(Shutdown 2.4.1 > Start 2.6.0 > RollginUpgrade)

* Datanode 업그레이드(dfs.datanode.ipc.address), Namenode 에서 실행하는 명령어
```
bin/hdfs dfsadmin -shutdownDatanode myip.202:40020 upgrade
bin/hdfs dfsadmin -getDatanodeInfo myip.202:40020	
```
* 데이터노드가 Shutdown 되었음을 확인하고 Datanode 의 Hadoop 링크를 2.6.0 설치경로로 변경
* 하둡 2.6.0 Datanode 실행 
* 블럭맵 업데이트 확인, 로그내용 `Computing capacity for map BlockMap`

* 업그레이드 종료	
```
	bin/hdfs dfsadmin -rollingUpgrade finalize
```

[**Apache Hadoop Rolling Upgrade**]
(https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsRollingUpgrade.html)