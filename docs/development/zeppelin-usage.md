---
layout: default

parent: development
title: Apache Zeppelin Usage
tags: 
    - 2019
    - zeppelin
---

[Apache Zeppelin](https://zeppelin.apache.org/) 은 노트북 방식의 시각화 툴이예요. 

### Zeppelin Posts
1. [Zeppelin Install & QuickStart](/development/zeppelin-quickstart/)
1. [Zeppelin Usage](/development/zeppelin-usage/)
1. [Zeppelin interpreter](/development/zeppelin-interpreter/)
1. [Zeppelin on CDH](/development/zeppelin-on-cdh/)
1. [Zeppelin Project Build](/development/zeppelin-project-build/)
1. [Zeppelin Project Upgrade 0.8.2 ](/development/zeppelin-upgrade-0.8.2/)


## Environment
* Oracle JDK 1.8
* CentOS 7
* Zepplin 0.8.1

## Dynamic Form
Zeppelin 에서는 Dynamic Form 을 제공하고 있어서 Form 을 통해 입력받은 값으로 조건을 주는 형태로 사용 가능해요.
Dynamic Form 은 Paragraph scope 와 Note scope 에서 사용 문법의 차이가 있고, 또한 Programmatically 하게 추가하실 수 있어요.
예제에서는 text, select, checkbox 를 소개하고 있네요.

### Paragraph scope
#### Text input form

`${formName=defaultValue}` 의 형태예요.
```
%md Hello ${name}
%md Hello ${name=Michelle}
```

#### Select form

`${formName=defaultVallue,option1(displayName)|option2(displayName)|...}` 의 형태예요
```
%md This is ${day=mon,mon|tue|wed|thu|fri|sat|sun}
%md This is ${day=mon,1(mon)|2(tue)|3(wed)|4(thu)|5(fri)|6(sat)|7(sun)}
```

#### Checkbox form

`{checkbox(delimiter):formName=defaultValue1|defaultValue2...,option1|option2...}` 의 형태에요.
구분자 `delemiter` 의 기본값은 `,` 이고, 지정 할 수 있어요.
```
%md select ${checkbox:fields=name|age,name|age|salary|gender} from employees
# name, age
%md select ${checkbox( and ):fruit=apple|banana,apple|orange|banana} from employees
# name and age
```

### Note scope
Paragraph 에서와 사용법은 동일하고 `$$` 로 시작해요.

### Paragraph scope, Programmatically 
#### Text input form
`z.textbox(String formName, String defaultValue)` 의 형태예요. `textbox` 대신에 `input` 을 사용 할 수 있어요.
```
%spark
println("Hello", + z.textbox("name", "Michelle"))
println("Hello", + z.input("name"))
```

#### Select form
`z.select(String formName, Seq((String option, String displayName), ...))`  형태예요.
```java
%spark
println("Hello "+z.select("day", Seq(("1","mon"),
                                    ("2","tue"),
                                    ("3","wed"),
                                    ("4","thurs"),
                                    ("5","fri"),
                                    ("6","sat"),
                                    ("7","sun"))))
```

#### Checkbox form
`z.checkbox(String formName, Seq((String option, String displayName), ...)).mkString(String delimiter)`  형태예요.
```java
%spark
val options = Seq(("apple","Apple"), ("banana","Banana"), ("orange","Orange"))
println("Hello "+z.checkbox("fruit", options).mkString(" and "))
```

### Note scope, Programmatically 
Note scope 에서는 `noteTextbox`, `noteSelect`, `noteCheckbox` 로 사용해요.

## Display System
Zeppelin 은 Display System 이 있는데, 
Text Display System 을 기본 값으로 HTML, Table, Network, Angular Display System 을 통해서 결과를 출력할 수 있어요.
`%displaySystemName` 의 형태로 Display System 을 명시 하여 사용해요.

### Text
```shell
# 기본값으로 Text Display System 을 사용
%sh echo "Hello Zeppelin"
# Text Display System 명시
%sh echo "%text Hello Zeppelin"
```
### HTML
```shell
%sh echo "%html <h3>Hello Zeppelin</h3>"
```
#### Methematical expressions
[MathJax](https://www.mathjax.org/)

### Table
`\t` 으로 칼럼을 구분하고, `\n` 으로 행을 구분해줘요.
```shell
%sh echo -e "%table name\tsize\nsun\t100\nmoon\t10" 
```

Table 의 내용이 `%html` 일 경우 HTML Display System 을 사용해요.

```shell
%sh echo -e "%table name\tsize
%html <img src='http://...sun.png'/>sun\t100
%html <img src='http://...moon.png'/> moon\t10" 
```

### Network
`%network` Display System 은 Graph 로 처리되요. 
> [Graph](https://ko.wikipedia.org/wiki/%EA%B7%B8%EB%9E%98%ED%94%84) 는 연관된 객체들의 집합, Vertex, Edge 를 가집니다. 

```java
%spark
print(s"""
%network {
    "nodes": [{"id": 1, "label": "User", "data": {"fullName":"Andrea Santurbano"}},{"id": 2, "label": "User", "data": {"fullName":"Lee Moon Soo"}},{"id": 3, "label": "Project", "data": {"name":"Zeppelin"}}],
    "edges": [{"source": 2, "target": 1, "id" : 1, "label": "HELPS"},{"source": 2, "target": 3, "id" : 2, "label": "CREATE"},{"source": 1, "target": 3, "id" : 3, "label": "CONTRIBUTE_TO", "data": {"oldPR": "https://github.com/apache/zeppelin/pull/1582"}}],
    "labels": {"User": "#8BC34A", "Project": "#3071A9"},
    "directed": true,
    "types": ["HELPS", "CREATE", "CONTRIBUTE_TO"]
}
""")
```

### Angular 
Zeppelin 과 [AngularJS](https://angularjs.org/) 사이의 게이트웨이를 제공해요. Backend / Frontend API 제공합니다. 

## 마치며
[Zepplin 대시보드 만들기](https://www.youtube.com/watch?v=VKMB8nFhjug)
라는 유튜브 동영상 이예요. Zeppelin 프로젝트 참여자이신 것 같네요.
