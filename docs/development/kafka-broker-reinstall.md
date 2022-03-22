---
layout: default
parent: development
title: "Kafka Broker 디스크 증설, RAID구성, OS 재설치"
tags: 
    - 2019
    - kafka
---

## Kafka Broker 재설치
Kafka Broker 서버의 디스크 용량을 증설하는 작업을 진행 하게 되었습니다. 
RAID 10으로 디스크 구성을 변경하다보니 불가피하게 OS를 재설치 합니다. 
Kafka는 Broker 서버의 장애 상황에서도 서비스를 유지 할 수 있도록 설계되어 있어요.
Broker 서버를 1대씩 순차적으로 RAID 구성 및 OS 재설치 진행후에 Partition을 Reassign 할 계획입니다.


### Environment
* CentOS 7.6
* Cloudera CDH 6.1.1
* Cloudera Manager
* Kafka 2.0.0-cdh6.1.1
* Kafka Manager
* Kafka Broker 3대
* Replication fector 3

### HowTo
Cloudera Manager 에서 작업대상 Broker 서버를 서비스에서 제거해요. 
Cloudera Manager의 Host 메뉴에서 해당 서버를 제거하여 CDH 플랫폼에서 호스트를 완전 제거 해요.
RAID 를 구성하고 OS를 재설치 진행해요.
Cloudera Manager 에서 호스트를 클러스터에 추가하고, Kafka 서비스에서 역할을 할당 해요.

<img src="/assets/images/2019/2019-06-25-12-06-26.png" width="30%">
여기까지 진행하고 Broker를 투입하게 되면 Cloudera Manager 에서 나머지 2대의 Broker 서버에 경고가(Lagging Replicas Test) 표시 되요. 
Kafka 는 Broker가 재투입 되더라도 Partition을 자동으로 재조정 하지 않기 때문이예요.


Kafka Manager 의 Topic 리스트에는 Under Replication 으로 표시되네요.

![Under Replication](/assets/images/2019/2019-06-25-12-07-45.png)

파티션을 재조정 하려면 각 Broker에 위치할 파티션들과 Replication 들을 Json 형식으로 일일이 작성해 Kafka Tool 명령어를 사용해야 해요.
이 작업은 매우 번거로울 수 있어요. 다행이 Kafka Manager 가 손쉽게 작업 할 수 있게 도와 주네요.

Kafka Manager 의 Topic 리스트에 작업할 Topic 의 상세 정보에 보면 Operation 들이 보입니다. 
Generate Partition Assignments 작업을 수행합니다. 위에서 말한 Json 파일을 만들어 준다고 보시면 되요.
이후 Reassign Partitions 작업을 수행합니다. Broker 서버로 파티션들을 옮기는 작업이예요. 용량에 따라 수분, 수십분이 소요 됩니다. 

아래는 2번째 Topic의 Reassign Partition 작업을 진행하고 6번째 Topic에서 Reassign Partition 작업을 진행 중입니다. 
진행 중인 Topic에 대해 하일라이트 표시를 해주고 있네요.
Reassign Partition 작업이 완료된 Topic는 Broker 가 3으로 표기되고, Under Replication 은 0으로 표기 되고 있습니다. 

그런데 Borker Leader Skew 가 발생 했네요. Skew는 사전적 의미로 왜곡된 이란 뜻이고, 파티션의 ISR Leader 선출에 문제가 있음을 말해요.

![Reassign Partitio](/assets/images/2019/2019-06-25-12-10-45.png)

모든 Topic에 대해 Reassign Partition 작업이 완료 되면 투입된 Broker 디렉토리에 파티션이 할당되었을 거예요.
Kafka Data 디렉토리에서 `du -hs` 명령어로 데이터 들이 잘 복제 되었음을 확인 할 수 있어요.

이제 Leader Skew를 해결 합니다. 
파티션은 각 Broker로 분배 되어 투입된 Broker에 할당되었지만 투입된 Broker는 아직 파티션의 Leader 역할을 가지고 있지 않기 때문에 Skew가 발생해요.
Kafka Manager 에서 Preferred Replica Election 작업을 수행 합니다. 


