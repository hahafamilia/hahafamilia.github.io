---
layout: default
nav_exclude: true
parent: development
title: Apache Hadoop 2.4 운영
tags: 
    - 2014
---

과거 하둡 플랫폼 운영 당시 메모 형식으로 작성하였던 문서들을 옮겨 놓았어요.
당시 운영했던 플랫폼의 구성들과 운영을 위한 가이드 들을 작성했었네요.
Hadoop CLI Command 에 익숙하지 않은 운영/관리자를 위해 Shell 들도 개발해 놓았고, 
나중의 담당자를 위한 배려도 담겨있네요.

### Version
* Apache Hadoop 2.4.1

### Cluster 구성 
* Replication : 2
* Block size : 128M
* Public / Private Neetwork
* 클러스터 상태 확인
    - http://[namenode-ip]:40070/dfsclusterhealth.jsp
    - http://[namenode-ip]:40070/dfshealth.jsp

#### Nodes
* Namenode * 2Ea
* Journalnode * 3Ea
* ZKFC * 3Ea
* Datanode

#### Namenode
하둡 메타데이터 저장/관리 노드 , Namenode, DFSZKFailoverController 데몬 실행

* Namenode : 네임노드 데몬, 하둡 메타 관리
* DFSZKFailoverController : 주키퍼 클라이언트, 네임노드 헬스 체크, HA 컨트롤
* 관리/운영 배치(추가 개발)
    - /monitor/daemon_hdfs_status.sh
    - /monitor/daemon_hdfs_balancer.sh
    - /monitor/daemon_hdfs_namenode.sh
    - /monitor/daemon_hdfs_snapshot.sh
    - /monitor/daemon_meta_backup.sh
    - /monitor/daemon_del_meta.php
* 사용포트
    - 40000 : 네임노드 ipc 포트, 기본 주소 포트
    - 40070 : 네임노드 http 사용 포트

#### Journalnode
하둡 HA 구성을 위해 버전2 에서 등장한 노드로, 파일 추가/삭제 등으로 인한 메타 데이터 변경시 다수의 저널노드중 과반수 이상의 저널노드가 commit 되었을경우만 반영됨. 
active 노드만 쓰기 권한을 소유하고 standby 노드는 commit 된 로그를 주기적으로 동기화함. 

클러스터의 HA 구성에는 1개 이상의 홀수개 저널노드를 설치하여 안정성 확보 가능.
과반수 이하의 저널노드 장애는 서비스에 영향을 주진 않지만 과반수 이상의 장애는 서비스 장애로 이어짐으로 모니터링이 필요함.

* 실행 데몬명 : JournalNode
* 사용포트 : 8485

#### 주키퍼 노드
하둡 HA 구성을 위해 버전 2에서 등장한 노드로 네임노드의 DFSZKFailoverController 데몬은 주키퍼 노드와의 세션 유지를 통해 네임노드의 상태를 체크하여 네임노드의 active/standby 결정.

클러스터의 HA 구성에는 1개 이상의 홀수개 주키퍼노드를 설치하여 안정성 확보 가능.
주키퍼 노드의 장애는 서비스에 영향을 주진 않지만, 네임노드 장애가 동시에 발생하여 HA 전환이 필요할경우 standby-standby 상태에 빠질 수 있으니 모니터링이 필요함.

* 실행 데몬명 : QuorumPeerMain
* 사용포트 : 2181

#### 데이터 노드
* 데이터 저장 경로 : $HADOOP_HOME/conf/hdfs-site.xml 파일의 `dfs.data.dir`
* 실행 데몬명 : DataNode
* 사용포트
    - 40010 : 데이터노드 데이터 전송 포트
    - 40020 : 데이터노드 ipc 포트
    - 40075 : 데이터노드 http 포트

### 관리 / 운영
#### 데몬 시작/종료
* 주키퍼노드 
    - `zookeeper/bin/zkServer.sh [ start | stop ]`
* 주키퍼 노드를 제외한 노드
    - `hadoop/sbin/hadoop-daemon.sh [start | stop ] [ namenode | zkfc | journalnode | datanode ]`

#### 하둡 명령어
* `bin/hdfs` : 하둡 버전 1.x 의 “bin/hadoop” 명령어를 포함하는 명령어, 자세한 설명은 
[아파치 홈페이지](http://hadoop.apache.org/docs/stable/) 에서 확인 가능함. 

#### Namenode HA
* 하둡 HA는 버전 2 에서 추가된 기능으로 하둡 자체적으로 지원한다.
* namespace federation 으로 구성된 Cluster 개념 , namenode 는 HA 구성된 2개의 네임노드를 말한다.
* namespace, namenode 이름은 서버의 [하둡홈]/conf/hdfs-site.xml 에서 확인 가능하다.
* 현재 namenode의 상태 확인
    - [namenode]/hadoop/bin/hdfs haadmin –ns [namespace] –getServiceState [namenode]
    - ex) bin/hdfs haadmin -ns ns01 -getServiceState ns01nn1
* HA 전환
    - [namenode]/hadoop/bin/hdfs haadmin –ns [namespace] –failover [active nn] [standby nn]
    - ex) bin/hdfs haadmin –ns ns01 –failover ns01nn1 ns01nn2

#### 체크포인팅
체크포인팅 작업은 editslog 의 내용을 fsimage 로 머지 시키는 작업으로 하둡 버전 1 에서는 세컨더리 네임노드가 당당하였는데, 하둡 버전 2 에서는 세컨더리 네임노드는 사리지고 HA 구성된 standby 노드에서 역할을 수행함.

#### 밸런싱
* 데이터노드간 디스크 사용량 이 불균형 할 경우 노드간 블록을 이동시켜 균형화 하는 작업
* 밸런싱 수행중에 데이터노드의 시작/종료/추가/제거 가 발생할경우 밸런싱을 재시작 하여야 한다.
* threshold : 밸런싱 작업을 수행할 노드 선정 기준값
* threshold가 3일경우, 클러스터의 전체 용량 퍼센트 전후로 -3, +3 까지 밸런싱 작업을 수행
    - ex) 평균 사용량 85%, A 노드 사용량 83% : 밸런싱 미대상
    - ex) 평균 사용량 85%, A 노드 사용량 80% : 밸런싱 대상

#### 계획된 데이터 노드 제거
* conf/dfs.exclude 파일에 제거할 데이터노드의 address 추가
* `/manager/cmd_refreshNodes.sh` 실행
* 클러스터 정보 웹페이지(dfshealth.jsp) 혹은 하둡 리포트(/manager/cmd_report.sh) 에서 제거할 데이터노드의 상태가 `Decommissioning Nodes` 로 변경되었는지 확인
* 제거 대상이 된 데이터 노드의 블록들은 시간을 가지고 다른 노드로 이동되어진다. 
* 블록 이동이 완료되면 대상 노드는 DeadNode 로 상태가 변경된다. 
* conf/dfs.exclude 에서 대상 노드 address를 제거한다.

#### 네트워크 토폴로지
* 하둡으로 신규 파일이 업로드시에 1개의 리플리카는 자신의 데이터노드에 위치하고 그외의 리플리카는 자신 외의 노드에 위치시키는데 이러한 리플리카를 어디에 위치시킬 것인지에 대한 규칙.
* hadoop/topology.sh, hadoop/topology.data   data 파일에 토폴로지 규칙을 설정할 수 있다.
* 토폴로지로 한번 등록된 서버는 토폴로지 변경이 불가능하다.

#### 디스크 손상 
* 데이터노드가 사용하는 디스크 손상시 데몬은 다운된다. 이를 막기 위해 손상된 디스크를 몇 개까지 허용할 것인지에 대한 설정이 필요한다
* hdfs-site.xml 파일의 `dfs.datanode.failed.volumes.tolerated` 에 설정된 개수

#### 블록이름으로 파일 찾기
블록명으로 하둡의 파일을 찾을경우 최근 파일일 경우 네임노드 로그를 통해 찾을 수 있다.

* 네임노드는 파일 업로드 시에 파일에 블록을 할당하는 로그를 남긴다
    - ex) BLOCK* NameSystem.allocateBlock: /hdfs/path/filename. blk_-3299320753949086868_7367814
* 로그에서 블록명을 검색하면 하둡 파일 명을 찾을 수 있다.
* 최근에 업로드된 파일이 아닐 경우, 모든 메타 정보를 체크해야 한다. 이러한 작업은 수분의 시간이 소요되고, 시스템의 부하를 줄 수 있으므로 중복 혹은 반복 실행은 피해야 한다.
* 네임노드에서 /manager/cmd_fsck.sh  /hdfs/path –files –blocks > fsck-temp.log  를 수행하여 모든 파일의 블록 정보를 파일로 기록한다.

### 장애/복구 시나리오
#### 언더/커럽트/오버 블록 찾기
* 기본적인 손상/언더/오버 블록의 정보는 하둡 리포트를 통해 확인할 수 있다.
    - ex) 네임노드의 /manager/cmd_report.sh
* 모든 메타를 체크하여 손상/언더/오버 블록의 정보를 확인한다.
    - ex) /manager/cmd_fsck.sh / > fsck-tmp.log
* 언더/손상 블록의 정보가 보이며 결과의 맨 마지막에 클러스터 전체에 대한 요약 정보가 출력된다.

#### 커럽트 블록 찾기
* 커럽트 파일이 있을경우 `/manager/cmd_findCorrupt.sh` 쉘을 수행하면 커럽트 파일 목록을 찾을 수 있다. 이러한 작업은 수분의 시간이 소요되고, 시스템의 부하를 줄 수 있으므로 중복 혹은 반복 실행은 피해야 한다.

#### Namenode 디스크 손상
Namenode 디스크가 손상되었을때 HA 전환되어 서비스 장애가 발생하진 않습니다. 
디스크 손상이 해결되었을 경우 각각의 노드를 복구할 필요가 있습니다.

* Namenode 복구
    - `bin/hdfs namenode –bootstrapStandby` namenode disk로 fsimage 파일외의 파일들이 복사 된다.
* Journalnode 복구
    - 다른 저널노드의 /journal/data/path 디렉토를 복사해 온다.

* 휴지통/스냅샷 파일 복구
    - 삭제된 파일은 설정된 보관기간동안 휴지통에 보관되어지며, 휴지통의 파일은 복구가 가능합니다.
    - 휴지통의 경로는 /user/[하둡사용자]/.Trash
    - 휴지통에서도 삭제된 파일의 경우 스냅샷이 남아있을 경우 복구가 가능
    - 스냅샷의 경로는 /user/[스냅샷대상디렉토리]/.snapshot

### 관리자용 쉘 프로그램
Hadoop CLI Command 에 익숙하지 않은 운영/관리자를 위해 개발

* `/manager/cmd_fsck.sh` : 하둡내 파일/블록/노드 등의 정보 확인용 쉘, 관리자 실행권한.
대상 디렉토리가 많거나, 표시하는 정보가 자세할수록 시스템 부하 유발됨
    - ex) ./cmd_fsck.sh /hdfs/path/
    - ex) ./cmd_fsck.sh /hdfs/path/filename –files –blocks -locations
* `/manager/cmd_get.sh` : 하둡 파일 읽기
    - ex) ./cmd_get.sh /hdfs/path/filename /local/path/filename
* `/manager/cmd_ls.sh` : 하둡 파일 리스트( 리눅스 ls)
    - ex) ./cmd_ls /hdfs/path/filename
* `/manager/cmd_metasave.sh` : 리플리케이션 대기 파일/블록 정보를 파일로 저장
    - ex ) ./cmd_metasave.sh ms0306.log
* `/manager/cmd_refreshNodes.sh` : 계획된 데이터노드 삭제시 노드 정보 갱신
* `/manager/cmd_report.sh` : 하둡 현재 상태에 대한 관리자 리포트 출력, 루트 실행권한
* `/manager/cmd_safemode.sh` : 하둡 읽기전용 ON/OFF
    - ex) ./cmd_safemode.sh enter
    - ex) ./cmd_safemode.sh leave
* `/manager/cmd_setBalancerBandwidth.sh` : 밸런싱 작업중 사용할 대역폭, 바이트, 
설정된 바이트 * 10 만큼의 대역폭 사용
    - ex) ./cmd_setBalancerBandwidth.sh 52428800
* `/manager/cmd_startBalancer.sh` : 밸런싱 시작
* `/manager/cmd_stopBalancer.sh` : 밸런싱 중지
* `/monitor/daemon_del_meta.sh` : 24H 이전 백업메타파일 삭제
* `/monitor/daemon_meta_backup.sh` : 네임노드 메타데이터 압축/백업, 매 1시간
* `/monitor/daemon_hdfs_balancer.sh` : 주기적인 밸런싱 시작, 매 1시간
* `/monitor/daemon_hdfs_status.sh` : 하둡 정보 리포트, 매 15분
* `/monitor/daemon_hdfs_namenode.sh` : 하둡2 namenode 데몬 다운시 재시작
* `[datanode]/manager/start_khdfs.sh` [local ip] : 데이터노드 시작 
* `[datanode]/manager/stop_khdfs.sh` : 데이터노드 중지
* `[datanode]/manager/set_loglevel.sh` [local ip] : 데이터노드 로그레벨 WARN 설정

