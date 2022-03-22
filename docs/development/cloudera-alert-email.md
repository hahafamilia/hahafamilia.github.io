---
layout: default
parent: development
title: "Cloudera Manager 알람 설정, Gmail SMPT 서버 사용"
tags: 
    - 2019
    - cloudera-manager-alert
    - monitoring
---

Cloudera Manager 알림을 보내는 방법은 SMTP, SNMP, Custom Script 세가지를 제공하고 있어요. 
여기서 SNMP, Custom Script 는 Enterprise 버전에서만 지원해요.
별도의 SMTP 서버를 운영하고 있지 않다면 Gmail 을 이용할 수 있어요. 

## Cloudera Version 
Cloudera 6.1

### Gmail 설정
우선 Gmail 설정에서 IMAP 사용이 허용되어야 해요. 
그리고 `Google 계정 설정 > 보안 > 보안 수준이 낮은 앱의 액세스` 가 허용되어야 합니다. 

> 이 방법은 보안상 권장하지 않는 방법 이예요. 하지만 제가 근무하는 회사의 G Suite 에서는 액세스키에 의한 접근 기능이 제공되고 있지 안아서 이 방법을 사용하고 있어요.

# Cloudera Alert Publisher Mail 환경설정
[Email 구성 문서](https://www.cloudera.com/documentation/enterprise/6/6.1/topics/cm_ag_email.html#xd_583c10bfdbd326ba--6eed2fb8-14349d04bee--7d1d)
문서를 참조해서 간단하게 구성이 가능 합니다. 

Cloudera Manager Service > Configuration > Filter(Alert Pulisher & Main) 에서 설정이 가능해요. 아래의 항목들을 변경해요.

* 메일 서버 프로토콜 : smtps
* 메일 서버 호스트 이름 : smtp.gmail.com
* 메일 서버 사용자 이름 : 보내는 메일 주소 
* 메일 서버 암호 : 보내는 메일 주소의 로그인 비밀번호
* 보낸 사람 주소 : 
* 받는 사람 주소 : 

![Alert Pulisher Eaml Configuration](/assets/images/2019/2019-08-13-11-48-37.png?classes=shadow)

> Cloudera Manager 의 상단 메뉴의 `관리` 메뉴에서 `테스트 알림 전송` 기능을 제공하고 있어요. 

# Alert, Trigger 설정
어떤 알림을 받을 수 있을까요? Cloudera 의
[경고 관리 문서](https://www.cloudera.com/documentation/enterprise/6/6.1/topics/cm_ag_alerts.html)
를 보면 클러서터의 상태/로그/활동에 대한 경고들이 설정되어 있다고 합니다. 
`Cloudera Manager > 관리 > 알림` 메뉴에 알림 항목들이 설정되어 있어요.
`편집` 버튼을 통해 각 서비스의 `구성` 에서 설정을 변경 할 수 있습니다. 

## Trigger
원하는 조건에 해당하는 알림을 받고 싶으면 `Trigger` 를 구성할 수 있어요. 
트리거는 클러스터의 각 서비스의 관리 페이지에 트리거 생성 버튼을 통해서 만들수 있습니다. 


[트리거 문서](https://www.cloudera.com/documentation/enterprise/6/6.1/topics/cm_dg_triggers.html)
를 보면 Trigger 는 이름/표현/임계값/활성화여부 로 구성되요.
Trigger 표현은 아래처럼 조건과 액션으로 작성합니다.
```
IF (CONDITIONS) DO HEALTH_ACTION
```
```
IF ((SELECT fd_open WHERE roleType=DataNode AND last(fd_open) > 500) OR (SELECT fd_open WHERE roleType=NameNode AND last(fd_open) > 500)) DO health:bad
```
