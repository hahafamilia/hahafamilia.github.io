---
layout: default
parent: development
title: "Hive Java UDF, 유니코드"
tags: 
    - 2019
    - hive-udf 
    - unicode
---

## 개요
[Cloudera Document 6.1 Hive UDF](https://www.cloudera.com/documentation/enterprise/6/6.1/topics/cm_mc_hive_udf.html)
문서를 참고하여 Cloudera CDH 플랫폼에서 HIVE UDF 를 작성하는 방법을 알아봅니다.  
또한 MySQL의 `Collate` 와 문자열 유니코드에 대해서도 간단히 알아보겠습니다. 

저의 이번 경우는 HIVE로 집계된 데이터를 SQOOP으로 export 시에 오류가 발생하였습니다.  
기존에 설계된 MySQL 디비의 테이블 칼럼 Collate 속성이 `utf8-general-ci` 로 설계되어 있어 Key 칼럼에 Accent 문자열을 포함하는 문자열 데이터 자정시에 상황에 따라 키중복이 발생했던 것이었습니다. 

칼럼의 Collate 속성이 `utf8-general-ci` 일경우 아래와 같은 경우 `ã` 문자열은 저장이 되겠지만 `a` 문자열 저장시 Key 중복 오류가 발생합니다. 
``` sql
insert into test(word) values ('ã');
insert into test(word) values ('a');
```
왜 그럴까요? Collate 는 문자열 정렬에 관련한 속성으로 값의 비교정책입니다. `utf-general-ci` 는 대소문자, 악센트 문자등을 같은 값으로 비교판단합니다. 
그렇기 때문에  `ã` 문자는 `a` 취급되고 키중복이 발생합니다.  

제 경우에 테이블의 변경할 수 없는 상황으로 HIVE 쿼리 수행시에 악센트 문자열을 제거 하는 작업을 수행했습니다. 

## UDF JAR 
Maven 에 HIVE dependency를 추가합니다. 
> 묶여진 Jar 파일은 모든 디펜던시를 포함하고 있어야 하는데요. Uber Jar 로의 빌드가 필요합니다. `maven-shade-plugin` 을 사용합니다.

```xml
<dependency>
    <groupid>org.apache.hive</groupid>
    <artifactId>hive-exec</artifactId>
    <version>2.1.1</version>
</dependency>
```

[NaverD2 한글인코딩](https://d2.naver.com/helloworld/76650) 에 잘 설명되어 있어 있어 많은 참고가 되었습니다. 
우선 악센트를 포함하는 문자열을 정준분해(NFD) 한후 정규식을 통해 캐릭터를 치환한후 다시 정준결합(NFC) 하는 HIVE UDF 함수를 작성합니다.
`각` 이라는 문자열을 정준분해 분해 할경우 `ㄱㅏㄱ` 이 됩니다.
```java
string = Normalizer.normalize(string, Normalizer.Form.NFD);
string = string.replaceAll("\\p{InCombiningDiacriticalMarks}+","");
string = Normalizer.normalize(string, Normalizer.Form.NFC);
```


```java
package bigdata.hive.udf;


import lombok.extern.slf4j.Slf4j;
import org.apache.hadoop.hive.ql.exec.Description;
import org.apache.hadoop.hive.ql.exec.UDFArgumentException;
import org.apache.hadoop.hive.ql.exec.UDFArgumentLengthException;
import org.apache.hadoop.hive.ql.metadata.HiveException;
import org.apache.hadoop.hive.ql.udf.generic.GenericUDF;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspector;
import org.apache.hadoop.hive.serde2.objectinspector.primitive.PrimitiveObjectInspectorFactory;
import org.apache.hadoop.hive.serde2.objectinspector.primitive.StringObjectInspector;

import java.text.Normalizer;

@Slf4j
@Description(
        name="str_normal",
        value="remove special character. ex) accent",
        extended="step1. Normalizer.Form.NFD" +
                "step2. replaceAll regular InCombiningDiacriticalMarks" +
                "step3. Normalizer.Form.NFC" )
public final class StringNormalize extends GenericUDF {

    StringObjectInspector stringOI;

    @Override
    public ObjectInspector initialize(ObjectInspector[] objectInspectors) throws UDFArgumentException {

        if (objectInspectors.length != 1) {
            throw new UDFArgumentLengthException("required string argument.");
        }

        ObjectInspector objectInspector = objectInspectors[0];

        if (false == objectInspector instanceof StringObjectInspector) {
            throw new UDFArgumentException(String.format( "argument must be a string. class=%s", objectInspector.getClass()));
        }

        this.stringOI = (StringObjectInspector) objectInspector;

        return PrimitiveObjectInspectorFactory.javaStringObjectInspector;

    }

    @Override
    public Object evaluate(DeferredObject[] deferredObjects) throws HiveException{

        DeferredObject deferredObject = deferredObjects[0];

        String string = this.stringOI.getPrimitiveJavaObject(deferredObject.get());

        if (string == null || string == "") {
            return string;
        }

        string = Normalizer.normalize(string, Normalizer.Form.NFD);
        string = string.replaceAll("\\p{InCombiningDiacriticalMarks}+","");
        string = Normalizer.normalize(string, Normalizer.Form.NFC);

        return string;

    }

    @Override
    public String getDisplayString(String[] strings) {
        return "String normalize. ";
    }
}
```

## Hive UDF 
Jar 파일을 HADOOP 파일시스템 `hdfs:///app/hive-udf/hive-udf.jar` 경로에 복사합니다. 
또한 HIVE SERVER2 를 서비스 하고 있는 호스트의 로컬 파일 시스템에도 `/usr/local/bigdata/hive-udf/hive-udf.jar` 저장합니다.
> 빌드된 jar 파일은 HADOOP과 HIVE SERVER2의 서버에 모두 등록되어이 있어야 합니다.

HIVE 서비스가 Jar 를 classpath 에 등록하기 위해서는 아래의 설정값을 변경해 주어야 합니다. 설정값을 변경 한후 HIVE 구성파일을 재배포 하고 서비스를 재시작 합니다.
> reloadable 속성을 정의 할경우 추후 Jar 파일이 변경될 경우 `reload;`  명령어를 사용할 수 있습니다.

Cloudera Manager > Hive > Configuration > Filter : Hive Serivce-Wide Advanced > 
Hive Service Advanced Configuration Snipped(Safety Valve) for hive-site.xml
Click(+)
```
Name : hive.reloadable.aux.jars.path
Value : /usr/local/bigdata/hive-udf
```


beeline 혹은 hue 의 HIVE Editor 에서 함수를 등록 합니다.
```sql
create function str_normal  as 'bigdata.hive.udf.StrignNormalize' using jar 'hdfs:///app/hive-udf/hive-udf.jar';
describe function extended str_normal;
show functions;
select str_normal('ã'));
--- result
a
```

### UDF 함수 업데이트
먼저 HIVE UDF 함수를 제거합니다.
``` sql 
drop function if exists str_normal; 
``` 
HADOOP 과 HIVESERVER2 의 Jar 파일을 업데이트 한 후 beeline 혹은 Hue 에서 `reload;` 명령어를 수행합니다.


> HUE Editor 에서 SQL을 작성하실 때 HIVESERVER2 의 호스트 서버에 Jar 파일을 등록하지 않고 진행 않아도 UDF 를 사용할 수 있습니다.
하지만 이럴경우 Oozie Workflow 를 실행하거나 Schedule 로 등록시 UDF 함수를 찾을 수 없다는 오류가 발생합니다.
