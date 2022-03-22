---
layout: default
parent: development
title: Apache Pig Latin 
tags: 
    - 2019
    - bigdata
    - apache-pig
---

[Apache Pig](http://pig.apache.org/)
Yahoo 에서 공개한 걸로 알고 있어요. 
최근 버전은 `Hive on Spark` 처럼 `Pig on Spark` 으로 사용하는군요.
새로운 Flow 코드 작성시 잘 사용하진 않지만, 
SQL 사용시 함수와 프로시져를 만들어야 하는 경우가 있는데, 그런 경우 Pig 를 사용하고 있어요.
ASIS Flow 에서 사용되어지고 있는 코드 들이 있어서 간단히 문법에 대해 정리 해봐요.

### Pig Latin Basic
연산자 및 명령어들은 대소문자를 구분하지만, 별칭 및 함수 이름은 대소문자를 구분해요.

#### Data types
int, long, float, double, chararray, Bytearray, Boolean, Datetime, Biginteger, Bigdecimal, 
Tuple, Bag(collection of tuples), Map

#### Operator
피그에는 몇몇 종류의 operator 있는데, SQL 과 느낌이 비슷해요. 

* 로드/저장: LOAD, STORE
* 필터: FILTER, DISTINCT, FOREACH GENERATE, STREAM
* 그룹/조인 : JOIN, COGROUP, GROUP, CROSS
* 정렬 : ORDER, LIMIT
* 결합/분할 : UNION, SPLIT
* Diagnostic : DUMP, DESCRIBE, EXPLAIN, ILLUSTRATE

#### 주석
```
/* multi line
comments */
```
`-- single line comments`

#### Shell 안에서의 사용
```
#!/usr/bin/env bash


cat << PIGEND > ./pigscript.pig
    set [environment]
    register [library]
    pig codes
    ...
    {$today}
PIGEND

pig ./pigscript.pig
```

### 로드/저장
#### LOAD
`Relation_name = LOAD 'Input file path' USING function as schema;`
```
student = LOAD 'hdfs://localhost:9000/pig_data/student_data.txt' 
    USING PigStorage(',')
    as ( id:int, firstname:chararray, lastname:chararray, phone:chararray, 
    city:chararray );
```

#### STORE
`STORE Relation_name INTO 'directory path' [using function];`
```
STORE student INTO 'hdfs://localhost:9000/pig_Output/' USING PigStorage (',');
```

### Diagnostic
* `Dump Relation_name;` 결과를 화면에 출력
* `Describe Relation_name;` 스키마 출력
* `explain Relation_name;` 논리적, 물리적, MR plan 출력
* `illustrate Relation_name;` statement 를 단계적으로 실행

### 그룹/조인
#### GROUP
`Group_data = GROUP Relation_name BY age;`
```
group_data = GROUP student_details by age;
group_multiple = GROUP student_details by (age, city);
group_all = GROUP student_details All;
```
#### COGROUP
두개 이상의 relation 을 그룹핑 해요.
```
cogroup_data = COGROUP student_details by age, employee_details by age;
```
```
(23,{(6,Archana,Mishra,23,9848022335,Chennai),(5,Trupthi,Mohanthy,23,9848022336 ,Bhuwaneshwar)}, 
   {(5,David,23,Bhuwaneshwar),(3,Maya,23,Tokyo),(2,BOB,23,Kolkata)}) 
```
#### SELF JOIN
`Relation3_name = JOIN Relation1_name BY key, Relation2_name BY key;` 
`Relation1_name`, `Relation2_name` 가 동일한 데이터소스를 `LOAD` 해서 `JOIN` 해요.

```
customers3 = JOIN customers1 BY id, customers2 BY id;
```
#### INNER JOIN
`result = JOIN relation1 BY columnname, relation2 BY columnname;`
#### LEFT OUTER JOIN
`Relation3_name = JOIN Relation1_name BY id LEFT OUTER, Relation2_name BY customer_id;`
#### RIGHT OUTER JOIN
`outer_right = JOIN customers BY id RIGHT, orders BY customer_id;`
#### FULL OUTER JOIN
`outer_full = JOIN customers BY id FULL OUTER, orders BY customer_id;`
#### 다중키 JOIN
` Relation3_name = JOIN Relation2_name BY (key1, key2), Relation3_name BY (key1, key2);`
#### CROSS
`cross_data = CROSS customers, orders;`

### 결합/분할
#### UNION
`Relation_name3 = UNION Relation_name1, Relation_name2;`
```
student = UNION student1, student2;
```
#### SPLIT
`SPLIT Relation1_name INTO Relation2_name IF (condition1), Relation2_name (condition2);`
```
SPLIT student_details into student_details1 if age<23, student_details2 if (22<age and age>25);
```

### 필터
#### FILTER
`Relation2_name = FILTER Relation1_name BY (condition);`
```
filter_data = FILTER student_details BY city == 'Chennai';
```
#### DISTINCT
`Relation_name2 = DISTINCT Relatin_name1;`
```
distinct_data = DISTINCT student_details;
```
#### FOREACH
`Relation_name2 = FOREACH Relatin_name1 GENERATE (required data);`
```
foreach_data = FOREACH student_details GENERATE id,age,city;
```

### 정렬
#### ORDER BY
`Relation_name2 = ORDER Relatin_name1 BY (ASC|DESC);`
```
order_by_data = ORDER student_details BY age DESC;
```
#### LIMIT
`Result = LIMIT Relation_name required number of tuples;`
```
limit_data = LIMIT student_details 4; 
```

### 내장함수
Eval, Load/Store, String, Datetime, Math 등의 내장 함수는 
[링크](https://www.tutorialspoint.com/apache_pig/apache_pig_eval_functions.htm)로 대체 할게요.

