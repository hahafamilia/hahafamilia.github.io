---
layout: default
parent: development
title: IntelliJ maven scala 프로젝트 설정
tags: 
    - 2019
    - intellij
    - maven
    - scala
    - spark-streaming
---

IntelliJ IDE 에서 spark streaming 개발을 위해 scala maven 프로젝트 생성 방법을 알아봐요.
scala 프로젝트는 sbt 를 기본으로 사용하지만, maven 에 익숙하여 maven 으로 프로젝트를 생성해요.
`scala-archetype-simple` 으로 프로젝트 생성이 가능한데, 제가 직접 구성하는게 좋아요.

### Version 
* Spark 2.4.0
* Scala 2.11
* Hadoop 2.7
* Java 8
* Window

### Spark, Hadoop 설치
[Spark Download](https://spark.apache.org/downloads.html) 에서 Spark 를 다운로드해요.
운영중인 클러스터의 스파크버전과 맞추어 2.4.0 버전의 Pre-built for Apache Hadoop2.7 을 다운로드 했어요.
다운로드한 파일을 압축해제 하고 `SPARK_HOME` 환경변수로 등록후 `PATH` 설정해요.

Window 에서 Hadoop 바이너리파일을 제공하는 [winutils](https://github.com/steveloughran/winutils)
라는 Git 프로젝트가 있어요. zip 으로 한후 압축풀고 Hadop2.7 디렉토리를 `HADOOP_HOME` 환경변수로 등록후 `PATH` 설정해요.

### IntelliJ 프로젝트 생성
1. `File > New > Project > Maven` 빈 프로젝트 생성

1. `/src/main/java, /src/test/java` 디렉토리 삭제
1. `/src/main/scala, /src/test/scala` 디렉토리 생성
1. scala 디렉토리 마우스 우클릭, `Mark Directory as > Sources Root(TestSources Root) `  
1. `File > New > .ignore file`, 
`Languages, frameworks > check scala`, `Global templates > check JetBrains, check Windows(macOS)
1. 프로젝트명 마우스 우클릭 `Add Framework Support...` scala SDK 지정
1. `pom.xml` 에 디펜던시를 추가해요. 구조화된 스트리밍을 프로그램을 개발할 예정이라 우선 아래의 디펜던시만 추가했어요.
```
org.scala-lang:scala-library
org.apache.spark:spark-core_2.11
org.apache.spark:spark-sql_2.11
```

### 확인
[Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
에 나와있는 테스트 코드작성하고, `nc -lk 9999` Netcat 띄우고, IntelliJ 에서 `Run SimpleApp` 실행시킨후, Netcat 에서 텍스트 입력해봐요.
```
import org.apache.spark.sql.SparkSession

object SimpleApp {
    def main(args: Array[String]) : Unit = {
        val spark = SparkSession.builder().appName("SimpleApp").master("local[*]").getOrCreate()
        val lines = spark.readStream.format("socket")
            .option("host", "loalhost").option("port", 9999).load()
        import spark.implicits._
        val words = lines.as[String].flatMap(_.split(" "))
        val wordCounts = words.groupBy("value").count()
        val query = wordCounts.writeStream.outputMode("complete").format("console").start()
        query.awaitTermination()
    }
}
```

