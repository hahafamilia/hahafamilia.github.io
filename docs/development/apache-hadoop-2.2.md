---
layout: default
nav_exclude: true
parent: development
title: Apache Hadoop 2.2 운영
tags: 
    - 2014
---

과거 하둡 플랫폼 운영당시 메모 형식으로 작성하였던 문서들을 옮겨 놓았어요.
내용이 잘 정리되어 있진 않아도 
다시 읽어보니 하둡 1.X 버전으로 플랫폼 운영중에 하둡 2.X 버전으로 업그레이드 하면서 테스트했던 내용들을 메모 했었네요.
Federation, HA, fencing, Snapshot, Journalnode, Datanode 성능 등을 테스트 했었군요.


### Federation 에 Namenode 추가
namenode01-02 서버가 HA 구성되어 있고 Federation 구성되어있을경우 namenode03-04 를 추가합니다. 

1. namenode03, namenode04 에서 `core-site.xml hdfs-site.xml` namespace 관련 설정을 추가
1. namenode03 의 네임노드를 기존 cluster id 로 포맷, `bin/hdfs namenode -format -clusterId  [clusterID]`
1. namespace의 zookeeper 초기화, namenode03 의 zkfc 시작
```
$ bin/hdfs zkfc -formatZK	
$ sbin/hadoop-daemon.sh start zkfc
## 확인
$ zookeeper01:/[hadoop-home]/bin/zkCli.sh -server zookeeper01:2181
$ ls /hadoop-ha
```
1. namenode03 의 namenode 시작, `sbin/hadoop-daemon.sh start namenode`
1. namenode04 의 네임노드 초기화, `bin/hdfs namenode -bootstrapStandby`
```	
14/07/09 15:09:33 INFO namenode.TransferFsImage: Opening connection to http://namenode194:40070/imagetransfer?getimage=1&txid=16440263&storageInfo=-56:239138164:1404883838982:CID-clusterID
```
1. namenode04 의 namenode 시작, zkfc 시작
```
$ sbin/hadoop-daemon.sh start zkfc
$ sbin/hadoop-daemon.sh start namenode
```
1. datanode01 에서 namespace 관련 설정추가
1. namenode03 에서 datanode01 의 정보 업데이트 명령 수행
```
$ bin/hdfs dfsadmin -refreshNamenodes datanode01:50020
```
1. 모든 datanode 에서 작업 수행

### HA 기능 테스트

#### HdfsFilesystem 라이브러리에서 Configuration 값을 통해 HDFS 에 읽기/쓰기 요청을 보낼때 어떤일이 일어날까?
네임노드 접근시에 IPC 요청은 active/standby 2개의 서버로 요청되어 집니다. standby 로의 요청은 실패되어지고, 재시도 되지 않는다. 
```
2014-03-10 15:41:35,010 INFO org.apache.hadoop.ipc.Server: IPC Server handler 1 on 8020 , call org.apache.hadoop.hdfs.protocol.ClientProtocol.create from standby-nn.example.com:8928 Call#0 Retry#0: error: org.apache.hadoop.ipc.StandbyException: Operation category WRITE is not supported in state standby
```

#### 자동장애복구 - autofailover
1. nn1-active, nn2-standby 상태에서 nn1 을 리부팅
1. nn2 번은 nn1번의 장애를 인지하고 ssh 펜싱을 시도하지만 ssh 원격접속을 하지 못해 active 상태로의 전환 실패
1. nn1 번이 재부팅 완료되면, ssh 펜싱 성공하고 active 상태로 전환
1. nn1 번의 하둡 데몬은 모두다 종료된 상태로, 서비스노드의 파일 접근이 있을경우 nn2 의 로그에 nn1 번으로의 연결 시도 로그가 계속 보입니다.
1. nn1 이 재부팅 되는동안 서비스노드로부터의 액세스는 대기 상태로 빠집니다.
1. 다운타임이 짧을경우 하둡으로의 요청은 타임아웃되지 않고 nn2의 active 전환이 완료된후 하둡으로의 요청도 이어서 계속 되었다.
1. 타임아웃 되는데 소요된 시간( 약 2분 10초 ), 14/03/10 18:51:24 ~ 14/03/10 18:53:35

```
14/03/10 18:51:24 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
14/03/10 18:53:35 WARN retry.RetryInvocationHandler: Exception while invoking class org.apache.hadoop.hdfs.protocolPB.ClientNamenodeProtocolTranslatorPB.getFileInfo. Not retrying because failovers (15) exceeded maximum allowed (15)
```

#### 자동장애복구에서 fencing 
* fenching 로직을 통과하지 못할경우 standby 가 active로 올라오지 않습니다.
`hdfs haadmin -failover | transitionToActive ` 등의 명령어 들도 통하지 않는다.
* 이럴경우 `dfs.ha.automatic-failover.enabled (false)` 옵션을 끄고 
`bin/hdfs haadmin -ns mycluster -transitionToActive nn1` active 전환을 시도합니다.
* 쉘 팬싱을 적용할경우, 팬싱이 실패되면 반복적으로 재시도 된다.
* 팬싱이 실패되는 상황에서 액티브 노드가 정상화 되면, standby - standby  상태가 된다.
* 이럴경우 팬싱쉘에서 강제적으로 exit 0 으로 줄경우 standby 를 액티브로 전환이 가능하다.
* 2번 팬싱실패 재시도중 > 1번 정상화 네임노드실행 > standby - standby > 페일오버 명령어로 1번 정상화
* 1번 노드가 정상화 되면, 팬싱에 실패되더라도 2번 노드가 액티브로 올라옵니다.
* standby - standy 상황에서 상대편 노드로의 연결을 계속 실행하면서 실행도중 아래와 같은 에러발생 합니다. 2개의 노드가 모두 연결될때만 메타 파일에 액세스 할 수 있도록 설계 된 것으로 보입니다.

```text
WARN org.apache.hadoop.hdfs.server.namenode.ha.EditLogTailer: Unable to trigger a roll of the active NN 
```

### Snaphost 
* 스냅샷 생성은 빠릅니다. 아이 노드 조회 시간을 제외하고, 비용은 O (1) 
* 수정이 스냅샷을 기준으로 한 ​​경우 추가 메모리에만 사용됩니다. 메모리 사용량은 O (M) , M은 수정 된 파일 / 디렉토리의 수입니다.
* 데이타 노드에 블록은 복사되지 않습니다. 스냅샷 파일은 차단 목록과 파일 크기를 기록한다. 데이터 복사가 없습니다.
* 스냅샷에 악영향을 정기적으로 HDFS 작업에 영향을 미치지 않습니다. 
* 현재의 데이터에 직접 액세스 할 수 있도록 수정은 시간 역순으로 기록됩니다. 
* 스냅샷 데이터는 전류 데이터로부터 변형을 감산함으로써 계산된다.
* 디렉토리의 스냅샷 사용 허락, `bin/hdfs dfsadmin -allowSnapshot /`
* 디렉토리의 스냅샷 사용 차단, `bin/hdfs dfsadmin -disallowSnapshot /`
* 스냅샷 생성, `bin/hdfs dfs -createSnapshot / snap1`
* 스냅샷 삭제, `bin/hdfs dfs -deleteSnapshot /directory snap1`
* 스냅샷 허용된 디렉토리, `bin/hdfs lsSnapshottableDir`
* 스냅샷 간의 변화 추이, `bin/hdfs snapshotDiff /directory snap1 snap2`
* 스냅샷 위치, `bin/hdfs dfs -ls /.snapshot/snap1`	

#### Snapshot 테스트

1. t1.txt 파일생성 > snap1 생성
1. t1.txt 파일변경 > snap2 생성
1. t1.txt 파일변경 > snap3 생성

```
bin/hdfs fsck /tmp -files -blocks -locations
bin/hdfs fsck /tmp/.snapshot/snap1/t1.txt -files -blocks -locations
```
```
# file #1, version 1.0
BP-876852240-myip.108-1404457930723:blk_1073777524_36701 len=12 repl=2 [myip.118:40010, myip.114:40010]
BP-876852240-myip.108-1404457930723:blk_1073777524_36701 len=12 repl=2 [myip.118:40010, myip.114:40010]
# file #2, version 2.0
BP-876852240-myip.108-1404457930723:blk_1073777525_36702 len=12 repl=2 [myip.114:40010, myip.118:40010]
BP-876852240-myip.108-1404457930723:blk_1073777525_36702 len=12 repl=2 [myip.114:40010, myip.118:40010]
# file #3, version 3.0
BP-876852240-myip.108-1404457930723:blk_1073777526_36703 len=12 repl=2 [myip.118:40010, myip.115:40010]
BP-876852240-myip.108-1404457930723:blk_1073777526_36703 len=12 repl=2 [myip.118:40010, myip.115:40010]
```
```
# file #2 복원, version 2.0
BP-876852240-myip.108-1404457930723:blk_1073777527_36704 len=12 repl=2 [myip.114:40010, myip.117:40010]
```
```
# file #1 복원, version 1.0
BP-876852240-myip.108-1404457930723:blk_1073777528_36705 len=12 repl=2 [myip.116:40010, myip.118:40010]
```

### Datanode Xceiver 테스트
Datanode의 `dfs.datanode.max.xcievers` 는 동시 data connection 의 수입니다. 

#### 테스트 환경
* Datanode 1번 2번 에 각 xceiver 를 2개로 설정함.
* 클라이언트에서 요청 하는 블럭은 1번, 2번 DN이 모두 가지고 있음.
	
#### 테스트 결과
* 5개의 클라이언트 연결 시도시, 1번 노드에서 2개의 연결은 성공하고, 3개의 연결은 실패한다.
```
13/11/12 14:25:08 WARN hdfs.DFSClient: Failed to connect to /myip.13:40010, add to deadNodes and continuejava.io.EOFException
13/11/12 14:25:08 WARN hdfs.DFSClient: Failed to connect to /myip.13:40010, add to deadNodes and continuejava.io.EOFException
13/11/12 14:25:08 WARN hdfs.DFSClient: Failed to connect to /myip.13:40010, add to deadNodes and continuejava.io.EOFException
```

* 실패한 3개의 클라이언트는 2번 노드로 3개의 연결을 시도하고, 1개의 연결은 실패한다.
```
13/11/12 14:25:08 WARN hdfs.DFSClient: Failed to connect to /myip.11:40010, add to deadNodes and continuejava.io.EOFException
```
* 실패한 1개의 연결은 네임노드로 블럭에 대한 노드정보를 3초간격으로 3회 재요청하고, 실패로 빠진다.
```
13/11/12 14:25:08 INFO hdfs.DFSClient: Could not obtain block blk_-8368207181666867791_1294 from any node: java.io.IOException: No live nodes contain current block. Will get new block locations from namenode and retry...
13/11/12 14:25:11 WARN hdfs.DFSClient: Failed to connect to /myip.13:40010, add to deadNodes and continuejava.io.EOFException
13/11/12 14:25:11 WARN hdfs.DFSClient: Failed to connect to /myip.11:40010, add to deadNodes and continuejava.io.EOFException

13/11/12 14:25:11 INFO hdfs.DFSClient: Could not obtain block blk_-8368207181666867791_1294 from any node: java.io.IOException: No live nodes contain current block. Will get new block locations from namenode and retry...
13/11/12 14:25:14 WARN hdfs.DFSClient: Failed to connect to /myip.13:40010, add to deadNodes and continuejava.io.EOFException
13/11/12 14:25:14 WARN hdfs.DFSClient: Failed to connect to /myip.11:40010, add to deadNodes and continuejava.io.EOFException

13/11/12 14:25:14 INFO hdfs.DFSClient: Could not obtain block blk_-8368207181666867791_1294 from any node: java.io.IOException: No live nodes contain current block. Will get new block locations from namenode and retry...
13/11/12 14:25:17 WARN hdfs.DFSClient: Failed to connect to /myip.13:40010, add to deadNodes and continuejava.io.EOFException
13/11/12 14:25:17 WARN hdfs.DFSClient: Failed to connect to /myip.11:40010, add to deadNodes and continuejava.io.EOFException

13/11/12 14:25:17 WARN hdfs.DFSClient: DFS Read: java.io.IOException: Could not obtain block: blk_-8368207181666867791_1294 file=/hdfs/path/filename
    at org.apache.hadoop.hdfs.DFSClient$DFSInputStream.chooseDataNode(DFSClient.java:2426)
    at org.apache.hadoop.hdfs.DFSClient$DFSInputStream.blockSeekTo(DFSClient.java:2218)
    at org.apache.hadoop.hdfs.DFSClient$DFSInputStream.read(DFSClient.java:2381)
    at java.io.DataInputStream.read(DataInputStream.java:83)
    at tsetThread.run(testThread.java:39)
```

### JournalNode 서버 변경
Journalnode는 active 상태가 되는 네임노드에 epoch number 를 할당합니다.
epoch number 확인은 active 전환하고 
`path/current/last-promised-epoch, path/current/last-writer-epoch` 파일 내용을 학인할 수 있습니다.

#### 저널노드 서버 이동

1. 기존 저널 다운 
1. 새로운 저널노드 업 
1. 기존 저널의 저장 데이터 를 새로운 저널노드로 옮김
1. 새로운 저널 재시작
1. standby 네임노드 재시작
1. 새로운 저널노드 epoch number 업데이트


### 설정들
#### core-site.xml
* fs.trash.interval
* io.file.buffer.size

#### hdfs-site.xml
* dfs.namenode.handler.count
* dfs.datanode.handler.count
* dfs.datanode.max.transfer.threads
* dfs.datanode.socket.write.timeout
* dfs.socket.timeout
* dfs.datanode.du.reserved
* dfs.datanode.scan.preiod.hour