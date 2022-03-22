---
layout: default
parent: development
title: Memcache 개념과 설치 / 운영
tags: 
    - 2013
---

### 아키텍처
![](images/development/2020-02-05-memcache-system.png)

#### 데이터 구조
* 캐시 항목을 찾기 위한 해쉬 테이블(burket list)
* 캐시 항목 제거(eviction) 순서를 결정하는 LRU(least recently used) list
* 키 (key), 데이터 (value), 플래그 및 포인터들을 담고 있는 캐시 데이터 구조
* 캐시 항목 데이터 메모리 관리자인 슬랩 할당자 (slab allocator)
* 캐시항목
    - 해쉬 테이블에서 bucket 당 single linked-list를 가르키는 포인터
    - LRU에서 double linked-list에 사용되는 포인터
    - 캐시 항목에 동시에 접근하는 스레드 수를 나타내는 reference counter
    - 캐시 항목 상태 플래그
    - 키 (key)
    - 값 길이 (바이트)
    - 값 (value)

#### 프로세스 흐름
![](images/development/2020-02-05-memcache-flow.png)

* NIC에 요청 packet이 도착하고 libevent에 의해 처리
* worker thread
    - 연결 및 데이터 패킷을 받기
    - 명령 및 데이터를 확인
* Hash 값은 키 데이터에서 생성
* 해쉬 테이블과 LRU 처리를 위해 global cache lock 획득 (Critical Section 시작)
    - 캐시 항목 메모리 할당
    - 캐시 항목 데이터 구조에 데이터를 저장 (플래그, 키, 값)
    - 해쉬 테이블에서 캐시 항목을 GET, STORE, DELETE하기 위해 해쉬 테이블을 탐색
    - 캐시 항목을 LRU 앞에 삽입 (GET, STORE) 또는 제거 (DELETE) 하면서 LRU 수정
    - 캐시 항목 플래그를 업데이트
* Global cache lock 해제 (Critical Section 끝)
* 응답 구성
* (GET만 해당) global cache lock 확인 (assert)
    - 캐시 항목 ref count를 1 감소
    - global cache lock 해제
* 요청한 클라이언트 (프론트엔드 웹 서버)로 응답 전송

#### 성능
* 성능 = 싱글코어 < 멀티코어 < 하이퍼스레딩
* Global cache lock은 스레드가 4개 이상일 경우 병목 현상이 발생하는 주요 원인
* Global cache lock은  워쿼 스레드 간의 lock 경합이 높을 수 있음
* Global cache lock의 성능 향상을 위한 1.6 버전 개발중

#### Consistent Hashing
Key의 Hash 값으로 Cache Server 에 데이터를 저장하는데, Cache Server 의 장애 발생시에
가장 가까운 Cache Server 로 할당되어 Hash 의 재조정 없이 서비스가 가능합니다.

* Consistent Hashing 알고리즘에서 한가지 유의 해야 할 점, TTL 이 적절히 설정되어야 합니다.

    1. A 서버 장애
    1. A 서버에서 담당하는 Hash 들은 B 서버에 저장
    1. A 서버 복구
    1. A 서버에서 담당하는 Hash 들은 다시 A 서버에 저장
    1. *B 서버에 저장되었던 Hash 들이 남아있음.*
    1. A 서버 다시 장애
    1. B 서버에 남아 있던 데이터로 서비스(Old Data 로 응답)

### memcached 설치
`yum -y install memcached`, 설치 안될경우 epel 리포지토리 등록

#### epel 리포지토리 등록
```
rpm -Uvh http://dl.fedoraproject.org/pub/epel/5/x86_64/epel-release-5-4.noarch.rpm    
yum repolist
yum -y install yum-priorities
```

#### 기타 라이브러리
```
yum -y install libevent libevent-devel 
yum -y install zlib zlib-devel 
yum -y install php-pecl-memcache
yum -y install libmemcached
```

#### 서비스 등록
```
chkconfig memcached on
chkconfig --list |grep memcached
```

#### apache, php, php-devel
`yum install httpd php php-devel`

#### PHP 모듈 확인
```
# "memcache" 라고 출력됨
php -m | grep memcache 
# /etc/php.d/memcache.ini 의 졍보가 출력됨.
php -i | grep memcache
# /usr/lib64/php/modules/memcache.so 라고 출력됨.
locate memcache.so		
```

#### memcached 환경설정
vi /etc/sysconfig/memcached	
```
PORT="11301"
USER="nobody"
```

#### 동시접속수
5 * apache maxclients, MAXCONN="1024"

#### capacity memory (MB)
CACHESIZE="2048"

#### 옵션 -t : work threads
OPTIONS=" -t 4 "

#### memcached-php 환경설정
* vi /etc/php.d/memcache.ini	
    - memcache.allow_failover : 0, 연결 에러가 발생할 경우 다른 서버로 연결할 것인지 여부
    - memcache.chunk_size : 32768(32KB), 데이터 전송 크기, 기본 8192(8KB), 보통 32768(32KB)
    - memcache.default_port : 11301
    - `php -i | grep memcache` 설정 확인

#### 데몬구동
```
/etc/init.d/memcached status
/etc/init.d/memcached start
/etc/init.d/memcached stop
/etc/init.d/memcached restart
```

### 운영 기타
#### memcached -h
```
-l <addr>     바인드할 주소
-p <num>      TCP 포트 번호 (기본값: 11211)
-U <num>      UDP 포트 번호 (기본값: 11211, 0 인경우 사용안함)
-s <file>     UNIX 소켓 경로 (네트워크 지원 안함)
-d            데몬으로 실행
-u <username> 전환할 사용자 이름(루트로 실행시)
-m <num>      최대 메모리(MB단위, 기본값: 64)
-M            데이터 저장시 메모리가 부족할 경우 오류를 반환(기본값은 오래된 데이터를 삭제)
-c <num>      최대 접속 개수 (기본값: 1024)
-P <file>     PID 파일 저장 위치. -d 옵션 사용시 사용
-f <factor>   증가 팩터값. (기본값: 1.25)
-n <bytes>    키+값+플래그를 저장할 최소 단위(기본값: 48)
-L            large memory pages 사용(가능한경우)
-t <num>      사용할 쓰레드 개수 (기본값: 4)
-v            로그 보임
-vv           자세한 로그 보임
-vvv          매우 자세한 로그 보임
```

* 프로토콜 : 바이너리/아스키, 부하가 많은상황에서 바이너리가 약간의 성능 우위
* 명령어 : stats settings 1 
* 기본 튜닝
    - TCP 스펙상 접속을 끊은 후 TIME_WAIT 대기 시간이 발생한다. 30~240초로 설정할 수 있는데, 대부분의 운영체제에서는 240초가 기본값이다.
    - memcached 를 실행한 서버에서 아래와 같이 30초로 세팅한다. 참고로 TCP표준은 최소 60초 이상을 권장한다.
    ```
    cat /proc/sys/net/ipv4/tcp_fin_timeout
    echo 30 > /proc/sys/net/ipv4/tcp_fin_timeout
    ```
* 포트변경시
```
cat /etc/sysconfig/memcached	
cat /etc/php.d/memcache.ini
php -i | grep memcache
```

### 참고자료
* 홈페이지 : http://memcached.org/
* 아키텍처 : http://helloworld.naver.com/helloworld/151047
* PHP API : http://www.php.net/manual/en/book.memcache.php
* PHP Sample : 
    - http://css.dzone.com/articles/how-use-memcache-php
    - http://pureform.wordpress.com/2008/05/21/using-memcache-with-mysql-and-php/
* 설치 & 기타
    - 윈디나라 : http://www.solanara.net/solanara/memcached
    - http://blog.pages.kr/366
    - MCB : http://www.interdb.jp/techinfo/mcb/index-e.html
* Mecache-Mysql
    - http://www.mysqlkorea.co.kr/gnuboard4/bbs/board.php?bo_table=develop_04&wr_id=1
    - http://downloads.mysql.com/docs/mysql-memcached-en.pdf
* 모니터링
    - http://blog.bbom.org/65
    - https://code.google.com/p/phpmemcacheadmin/
