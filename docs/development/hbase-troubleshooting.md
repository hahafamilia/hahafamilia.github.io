---
layout: default
nav_exclude: true
parent: development
title: 할아버지 클러스터의 엉망진창 HBase 문제해결
tags: 
    - 2020
    - hbase
    - cloudera-cdh4
    - troubleshooting
---

입사초기에 있었던 경험에 대해서 적어볼게요.
빅데이터 플랫폼 개발자 포지션으로 입사를 했어요. 
면접과정에서 플랫폼에 장애가 빈번하다. 직원들이 많이 빠져나갔다는 얘기는 들었어요.
전 과거 4년간 Apache Hadoop 1.x 버전에서 2.x 버전으로 업그레이드를 진행하면서 운영한 경험이 있어요.
당시 많은 문제들을 경험했고 Hell의 문앞에도 가 보았기 때문에... 다 해결해 주겠어! 라는 각오로 입사했어요. 
막상 입사해보니 그나마 있던 담당자 마저 퇴사... 뭔가 싸늘한 기운이 느껴집니다?
그래도 파이팅 해봅니다. 

클러스터는 Cloudera CDH 4, 2012년에 릴리즈 되었던 버전이예요. 7년간 한번도 업그레이드를 안할 수 있는건지..
HBase 를 사용하고 있는데, 아이고... Region Server 버전이 0.92 버전, 0.94 버전 서로 다릅니다?
Linux OS 는 Debian 그런데 지원이 종료된 버전이라서 더이상 신규 패키지 설치도 안된다고 하네요.
지난 얘기고 여기에라도 하소연하니 기분이 좀 좋아지는데요? 하하! 그럼 어떤 일이 있었는지 ?좀 풀어 볼게요.

### Version
* Cloudera CDH 4.0
* Hbase 0.92, 0.94
* Debian 6

### Hbase archive 파일
우선 급한불부터 꺼야겠어요. 클러스터의 용량이 비정상적으로 증가해요.
아무도 이유는 모르고, 실제 저장되는 데이터의 두배 분량 증가하고 있었어요.

Hdfs 의 디렉토리 사용량을 조사해보니 `/hbase/.archive` 디렉토리 사용량이 서비스에서 저장된 데이터 사용량만큼 차지하고 있어요.
원인을 알수 없어서 커뮤니티에 문의한 결과를 요약하자면

*0.92 버전에서는 `.archive` 를 생성하지 않아? `.archive` 디렉토리 삭제를 시도해 볼 수는 있겠지만 나도 장담은 못해!*  
[Cloudera Community Question](https://community.cloudera.com/t5/Support-Questions/I-want-to-reduce-disk-usage/m-p/80359#M54865)

짜잔~ 어떻해야하죠?

0.94버전의 Region Server가 범인일거예요. 0.94 버전의 Regison Server 제거하기 위해 디컨미션을 시도했지만, 실패!
신중하게 `.archive` 디렉토리 삭제를 시도했어요. 서비스 잠시 중지하고 디렉토리 옮긴후 서비스 정상유무 확인하고 삭제.
휴~ 다행히 성공이에요. 그런데 말입니다~ 또 생길거거든요. 

여기서 선택 필요해요. 이 문제를 해결하는데 시간을 쏟을 것인가? 신규 플랫폼 구축의 일정을 앞당길 것인가?
신규 플랫폼 구축의 일정을 앞당기는 것으로 선택했어요. 
물론 인수인계도 제대로 못받았고, Crontab 에 있는 수십개의 Shell/Python 배치들을 Workflow 로 포팅도 해야하고, 
프로듀서 API 서버도 개발해야되고, Spark Streaming 어플리케이션도 개발해야 하지만... 

### HBase Meta 장애
업수파악하면서 신규 플랫폼 아키텍처 구상에 한창 열을 올리는 중에 하루는 `.archive` 디렉토리 삭제하고 HBase 도 정상인데 RabbitMQ 소비되지 않는 메시지들이 증가하기 시작해요.
주변분들이 긴장하기 시작해요. 
*그때 그 장애야...  그래요? 원인이 뭐예요? 어떻게 해결했어요?
그런 모르는데! 결국 내부 인력으로 해결안되서 외부인역으로 해결했거든*

#### 현상
* Hbase Shell 에서 테이블들이 안보여요.
* HBase Web UI 에서 Tables > Catalog Table 에서 .META. 가 보이지 않아요.
* Region Servers 에서 각 Region Server 에서 numberOfOnlineRegions 값이 0으로 보여져요.
* Master 서버의 HDFS, HBASE 로그에 특이점은 발견되지 않았어요.
* Cloudera Manager 에서 보이는 서비스 상태는 모두 정상이예요.

#### 원인
커뮤니티를 보니 HBase Meta 장애가 자주 생기나 봅니다. 결국 정확한 원인을 밝히지는 못했어요. 
문제를 해결하고 나서 추측한 원인으로는
HDFS 파일시스템에 일시적인 부하, 혹은 실패가 있었어요. HBase 는 Meta 를 로드하는데 실패했겠죠.
서비스를 재시작하고 즉각적인 대응 조치가 들어가면서 클러스터는 더 바빠졌을거예요.
아마 시간을 두고 지켜보면서 관찰했더라면 클러스터가 장애를 극복했을 것 같아요.

#### 대응 
1. HBase 재시작하였지만 여전히 Meta 오류, RabbitMQ 컨슈머 어플리케이션 일시 중지.
1. 0.94 Region Server 강제 제거, HDFS 는 리플리케이션 복제에 들어가면서 클러스터는 더 바빠졌을거예요
1. HDFS 내의 Meta 저장 경로의 디렉토리를 삭제 `/hbase/-ROOT-, /base/.META.`
1. Hbase 시작
1. `sudo -u hbase hbase hbck -repair` 메타 복구 명령 시도
1. HBase Web UI 에서 Tables > Catalog Table 에서 .META. 가 보이기 시작해요.
1. 하지만 `numberOfOnlineRegions` 값은 여전히 0이고 데이터 쿼리는 안되요.
1. hbck 명령어의 추가 옵션 시도 `-fix, -fixMeta, -fixAssignments, -repairHoles, -repair`
1. 이 과정에서 보여지는 HBase 로그에는 region server not online 등의 로그가 보여요.
1. 대응을 계속 해나가는 과정에서 hbck 수행시 tableDescriptor 목록에 일부의 테이블들이 나열되는게 보여요.
1. 해당 테이블들을 쿼리 해보니 쿼리가 정상적이예요. 그래서 다른 테이블들을 repair 할 수 있는 방법을 계속 찾아봤어요
1. 여기까지 대응하면서 HBase 가 알고 있는 Table Region Server 들의 HDFS 내 경로가 블록조정과정으로 실제 경로와 다르기 때문이라는 걸 알게 되었어요.
1. 계속된 대응으로 hbck 에서 2천개 가량의 inconsistence(불일치) 값이 드디어 repair 되었어요.
1. RabbitMQ 컨슈머 어플리케이션 서비스 시작, Queue 가 소진되기 시작했어요.
1. 몇개의 inconsistence 가 repair 되지 않아 부가적인 문제가 발생해요.
1. HDFS 의 로그에서 해당 테이블의 Region Server 파일을 지속적으로 Open 시도하는 것을 확인했어요.
1. 그러다 보니 파일의 블록이 위치한 혹은 위치한 것으로 알고있는(실제로는 유실) Hbase Region Server (노드) 가 too many open files 오류로 다운되요.
1. HBase Web UI 에서 Table 목록의 상세 페이지를 확인하면 inconsistence Tavke Region Server 가 not deployed 로 표시되어 있고 Region Server 이름을 알 수 있어요
1. HDFS 내의 파일경로 /hbase/<tableName/<region> 디렉토리를 강제로 삭제했어요.
1. hbck 를 수행했고, inconstince 가 더이상 없는 것을 확인했어요. HDFS 에서도 더이상 Open 시도를 안해요.

### 지나고나서
문제를 경험하고 해결해 나가는 것도 소중한 경험이지만, 이런 문제는 안만나고 싶어요.
아! 신규 플랫폼은요~ Shell 배치들 포팅하면서 몇번 토하긴 했지만, 아주 잘 구측되었어요. 
아키텍쳐 구상하면서 계속적으로 Best Practice 찾고 벤치마킹 자료 검토할 때는 의논할 동료 없이 혼자 하는게 너무 힘들더라구요.



