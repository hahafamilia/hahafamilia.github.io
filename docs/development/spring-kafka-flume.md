---
layout: default
nav_exclude: true
parent: development
title: "AvroFlumeEvent, 이벤트 데이터의 발생 시각에 따른 데이터 수집"
tags: 
    - 2019
    - flume 
    - AvroFlumeEvent
---

다음과 같은 데이터 파이프 라인을 가정해 볼게요.

* 사용자의 Activity 이벤트가 발생
* API 서버를 통해 Kafka 에 Produce
* Flume 을 통해 Kafka 의 메시지를 HDFS 로 적재
* HDFS 에는 일자 별로 생성된 디렉토리에 저장

![kafka-flume-hdfs pipeline](/assets/images/2019/2019-08-12-18-40-40.png)

Flume 을 퉁한 데이터 수집시에 Hdfs Sink 는 `useLocalTimestamp` 설정은 제공 해요. 하지만 이 설정은 이벤트의 수집 시각을 기준으로 해요.

예제 그림에서 API 에서 시작된 데이터는 파이프라인을 거쳐 HDFS 에 도달하기까지 2초의 시간이 소요된다고 가정하면, 
2019-08-01 23:59:59 시각에 발생한 이벤트는 useLocalTimestamp 설정에 의해 2019-08-02 00:00:01 의 시각으로 2019-08-02 디렉토리에 적재됩니다.

데이터 수집 파이프라인에서 이벤트의 발생시각에 따른 수집이 필요한데요.
Flumg NG 라이브러리는 `AvroFlumeEvent` 클래스를 제공 해요.

**Kafka 에 저장하는 이벤트 메시지에 Flume Ng 의 헤더 데이터로 Timestamp 추가하고, 
Flume 에서 이 헤더의 Timestamp 값으로 데이터를 저장하면 되요. 
AvroFlumeEvent 는 Header 를 추가할 수 있게 해주는 클래스 라고 보시면 되요.**


```java
    public void send(String topic, ActivityEvent message) throws IOException {

        Optional<Long> optionalTs = Optional.ofNullable(message.getActivityTime());
        long ts = optionalTs.orElse(Instant.now().toEpochMilli());

        // Flume message header
        Map<CharSequence, CharSequence> headers = new HashMap<>();
        headers.put("timestamp", Long.toString(ts));

        // Avro message bytes
        byte[] bytes = ActivityEvent.serializeByte(message);

        // Attatch flume message header with avro message.
        bytes = packFlumeMessage(headers, bytes);

        // 카프카 레코드 작성
        ProducerRecord<Long, byte[]> record = new ProducerRecord<>(topic, ts, bytes);

        // 카프카 전송
        ListenableFuture<SendResult> future = kafkaTemplate.send(record);

        future.addCallback(new ListenableFutureCallback<SendResult>() {
            @Override
            public void onFailure(Throwable e) {
                log.warn("failed after send to kafka: exception={}, record={}", e.getMessage(), message, e);
            }

            @Override
            public void onSuccess(SendResult sendResult) {
                log.info("success after send to kafka: record={}", message);
            }
        });


    }

    /**
     * Kafka 전송 메시지에 Flume 의 헤더 값을 추가합니다.
     * eventTime 을 Flume 에 추가하기 위함입니다.
     * Flume 은 수집시간이 아닌 이벤트 발생시간 기준으로 파티션되어 저장합니다.
     * @param headers "timestamp" 밀리초, String
     * @param message
     * @return
     * @throws IOException
     */
    private byte[] packFlumeMessage(Map<CharSequence, CharSequence> headers, byte[] message) throws IOException {

        AvroFlumeEvent avroFlumeEvent = new AvroFlumeEvent(headers, ByteBuffer.wrap(message));
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        BinaryEncoder encoder = EncoderFactory.get().directBinaryEncoder(out, null);
        SpecificDatumWriter<AvroFlumeEvent> writer = new SpecificDatumWriter<>(AvroFlumeEvent.class);
        writer.write(avroFlumeEvent, encoder);
        encoder.flush();

        return out.toByteArray();
    }

```

보셔야 할 코드는 `send` 함수의 `packFlumeMessage` 함수 호출 부분 이예요.
Kafka 에 메시지를 byte 로 저장하고 `packFlumeMessage` 함수에서 Timestamp 헤더를 추가하고 있어요.

```java
// Attatch flume message header with avro message.
bytes = packFlumeMessage(headers, bytes);
```

전체 예제 소스는 [Github](https://github.com/hahafamilia/spring-kafka-flume#spring-kafka-flume) 를 통해서 보실 수 있어요. 
코드에는 Avro 데이터 처리는 Jackson 을 사용하고 있어요.
테스트는 EmbeddedKafka 테스트와 CloudKafka 테스트 가 있습니다. 

