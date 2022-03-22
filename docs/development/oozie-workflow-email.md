---
layout: default
parent: development
title: "Oozie Workflow Email 알림 설정"
tags: 
    - 2019
    - oozie 
    - monitoring 
    - hue
---

Oozie 에서 Workflow 의 결과에 따른 Email 알림을 받는 방법에 대해서 알아볼게요. 

Workflow 를 1회성으로 실행시키는 경우와 Schedule 로 등록하여 주기적으로 실행하는 경우가 있을 수 있을텐데요.
1회성으로 Workflow 만 실행할때는 성공/실패에 대한 처리 결과를 받도록 하고, 
Schedule 로 등록하여 주기적으로 실행하는 경우에는 실패에 대한 알림 만을 받도록 합니다.

# Version
* Cloudera 6.1.1
* Oozie 5.0.0
* Hue 4.3.0

# Oozie SMTP 설정
`Cloudera Manager > Oozie > 구성` 탭 에서 mail 을 검색해서,
`oozie.email.smtp.host`, `oozie.email.from.address` 설정에 SMTP 의 도메인과 발신인 메일 주소를 설정해주세요.
Oozie, Hue 서비스의 재시작이 필요합니다.

> 아쉽게도 Oozie 5.0.0 버전에서는 SSL 설정을 할 수 없네요.
> [JIRA OOZIE-1393](https://issues.apache.org/jira/browse/OOZIE-1393) 를 확인해 보니 5.1.0 버전부터 Fixed 되었습니다.

# Workflow 처리 결과 알림
Oozie 서비스에 Mail 설정이 되어 있다면 Workflow 를 제출 할 때 처리 결과에 Email 받기 체크박스를 확인 할 수 있어요.
체크 해줌으로써 간단히 Mail 수신이 가능해요.

![](/assets/images/2019/2019-08-14-18-03-26.png)

# Workflow 실패시 알림

Hue Workflow Editor 에서 신규 Workflow 를 작성하는 레이아웃 이예요. 
종료 Action을 지정하는 Action에서(맨 마지막의 네모모양 레이어의 톱니바퀴 버튼) 실패에 대한 메일 알림 설정을 할 수 있습니다.

![](/assets/images/2019/2019-08-14-18-10-51.png)

수신 대상 Mail 주소를 `,` 구분자로 넣어주세요. 제목과 내용에 
[EL Function](https://oozie.apache.org/docs/5.0.0/WorkflowFunctionalSpec.html#a4.2_Expression_Language_Functions)
 을 사용할 수 있어요. 
`${wf:name()}` 는 Workflow 의 이름, `${wf:errofMessage(wf:lastErrorNode())}` 는 실패 액션의 오류 원인 이예요.

![](/assets/images/2019/2019-08-14-18-13-43.png)

## 특정 Action 의 결과 알림
만약 특정 Action 의 처리 결과에 대한 알림을 받고 싶을 경우, `Email` Action 을 사용 해야 해요.
Hue Workflow Editor 에서 선행 Action 의 수행후 `전환` 설정에서 `KO` 시에 `Kill` 이 아닌 Email Aciton 으로 전환 하게되면 Mail 을 수신할 수 있습니다. 


