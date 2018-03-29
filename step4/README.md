
Local computer에서 SCORE 개발할 수 있는 환경 만들기
===================

## 1. 목적
 앞서서 github에 올라와 있는 SCORE를 받아와서 올려 보았습니다. 이번에는 실제 개발을 한다고 했을 때, 어떻게 개발할 수 있는 환경을 만드는 법을 이야기 하려고 합니다.


## 2. 프로젝트 구성
아래와 같이 프로젝트를 구성하겠습니다. 실제 사용된 파일은 이 폴더의 하위 폴더에 있습니다. 주목해야 하는 것은 ```score/develop```이라는 폴더가 생겼다는 것입니다. 이 폴더 아래에 앞서서 이용했던 ``` contract_score```의 코드를 있는 그대로 올려놓을 것 입니다. (실제 사용된 모든 파일은 현재 폴더아래 있습니다.)

```
├── README.md
├── conf
│   ├── channel_manage_data.json
│   ├── peer_conf.json
│   └── rs_conf.json
├── fluentd
│   └── etc
│       └── fluent.conf
├── score
│   └── develop
│       └── contract_score
├── launch_servers.sh
├── stop_servers.sh
└── delete.sh
```

이렇게 구성하고 loopchain에게 "score/deveop" 폴더 아래 있는 SCORE 프로젝트를 읽어오라고 할 것입니다.


## 3. 환경설정


### 1. RadioStation 설정 - [`channel_manage_data.json `](conf/channel_manage_data.json)
 ```score_package```의 값을 ```develop/contract_score```라고 줍니다. 이 뜻은 'score라는 폴더 아래에 develop/contract_score'라는 SCORE프로젝트를 가져오라는 뜻입니다.

 ```
 {
   "channel1":
     {
       "score_package": "develop/contract_score"
     }
 }
```


### 2. Peer 설정 - [`peer_conf.json `](conf/peer_conf.json)
 이제 각 peer에서 개발용으로 SCORE를 읽어오라고 설정해야 합니다. 아래 설정들의 의미는 다음과 같습니다.
  - LOOPCHAIN_DEFAULT_CHANNEL : Multichannel의 기능입니다. 각 RESTful request에는  ```channel_manage_data.json```에서 지정한 channel명이 붙어야 합니다. 그러나 이 옵션을 주면 여기서 지정한 채널로 reqeust가 들어간다는 의미입니다. 
  - ALLOW_LOAD_SCORE_IN_DEVELOP : 이 값을 'allow'라고 하면 local에서 읽어와서 SCORE를 실행한다는 의미입니다.
  - DEVELOP_SCORE_PACKAGE_ROOT : 앞서 지정한 ```score```폴더 아래 어디에서 개발중인 SCORE를 읽어올지 지정합니다. 현재 설정의 의미는 `score`아래 `develop`폴더 아래에서 읽어오라는 의미입니다.
  - DEFAULT_SCORE_PACKAGE : ```develop/contract_score```라고 줍니다. 이 뜻은 'score라는 폴더 아래에 develop/contract_score'라는 SCORE프로젝트를 가져오라는 뜻입니다.

```json
{
  "LOOPCHAIN_DEFAULT_CHANNEL" : "channel1",
  "ALLOW_LOAD_SCORE_IN_DEVELOP" : "allow",
  "DEVELOP_SCORE_PACKAGE_ROOT" : "develop",
  "DEFAULT_SCORE_PACKAGE" : "develop/contract_score"
}
```

### 3. 시작스크립트에서 Peer실행 추가설정 - `launch_servers.sh`
 기존에 있던 SSH key, SCORE저장소 도메인을 지웁니다. 현재 local computer에서 읽어서 처리할 것이기 때문입니다.

```bash
...

docker run -d --name peer0 \
  -v $(pwd)/conf:/conf \
  -v $(pwd)/storage0:/.storage \
  -v $(pwd)/score:/score \
  --link radio_station:radio_station \
  --log-driver fluentd --log-opt fluentd-address=localhost:24224 \
  -p 7100:7100 -p 9000:9000  \
  loopchain/looppeer:${TAG} \
  python3 peer.py -o /conf/peer_conf.json  -r radio_station:7102

...
```

### 4. 시작해보기

```bash
$ launch_servers.sh
```


## 4. 테스트

### 1. Peer 목록 조회

```bash
$ curl http://localhost:9002/api/v1/peer/list | python -m json.tool

//결과
{
    "data": {
        "connected_peer_count": 1,
        "connected_peer_list": [
            {
                "cert": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE+HQPBowjyJnyinsYjiztl5i6hQ1JiWdpRmyFR1T283M4liQia7weerQQ4Qw6jDVwd+RkwHeenvR0xxovUFCTQg==",
                "group_id": "c9850196-e559-11e7-bf35-0242ac110004",
                "order": 1,
                "peer_id": "c9850196-e559-11e7-bf35-0242ac110004",
                "peer_type": 1,
                "status": 1,
                "status_update_time": "2017-12-20 07:46:09.483471",
                "target": "172.17.0.4:7100"
            }
        ],
        "registered_peer_count": 1,
        "registered_peer_list": [
            {
                "cert": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE+HQPBowjyJnyinsYjiztl5i6hQ1JiWdpRmyFR1T283M4liQia7weerQQ4Qw6jDVwd+RkwHeenvR0xxovUFCTQg==",
                "group_id": "c9850196-e559-11e7-bf35-0242ac110004",
                "order": 1,
                "peer_id": "c9850196-e559-11e7-bf35-0242ac110004",
                "peer_type": 1,
                "status": 1,
                "status_update_time": "2017-12-20 07:46:09.483471",
                "target": "172.17.0.4:7100"
            }
        ]
    },
    "response_code": 0
}
```

### 2. Peer 상태 조회

```bash
$ curl http://localhost:9000/api/v1/status/peer | python -m json.tool

{
    "audience_count": "0",
    "block_height": 2,
    "consensus": "siever",
    "leader_complaint": 1,
    "made_block_count": 2,
    "peer_id": "c9850196-e559-11e7-bf35-0242ac110004",
    "peer_target": "172.17.0.4:7100",
    "peer_type": "1",
    "status": "Service is online: 1",
    "total_tx": 2
}
```

### 3. SCORE 버전 조회
 이 부분에서 보면 version이 하나만 나오는 것을 알 수 있습니다. 이것은 local 컴퓨터안에 있는 파일을 가지고 내부에서 git repository를 자체적으로 구성해서 올리기 때문입니다. 이것은 loopchain이 올라올 때, ```score/develop``폴더 아래 보면 ```deploy``` 란 폴더가 있는 것으로 확인 가능합니다.

```bash
$ curl http://localhost:9000/api/v1/status/score | python -m json.tool

{
    "all_version": [
        "b301ffd2e0cf8fe2541de975e8d3afd281a7170b"
    ],
    "id": "develop/contract_score",
    "status": 0,
    "version": "b301ffd2e0cf8fe2541de975e8d3afd281a7170b"
}
```



### 4. SCORE Transaction 생성

```bash
$ curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","method":"propose","params":{"proposer":"RealEstateAgent" , "counterparties": ["leaseholder","lessor"], "content": "A아파트 203동 803호를 보증금 1500 월세 70에 계약 2019년 8월 1일까지 임대함, 임대 취소시", "quorum": "3"}}'  http://localhost:9000/api/v1/transactions | python -m json.tool

// 결과
{
    "more_info": "",
    "response_code": "0",
    "tx_hash": "3fc5795f1ff0732533f01bb1612911036ab7c620446437e3f2818f9a662e9085"
}
```

### 5. SCORE Transaction 조회 - `/api/v1/transactions/result` 사용

```bash
$ curl http://localhost:9000/api/v1/transactions/result?hash=3fc5795f1ff0732533f01bb1612911036ab7c620446437e3f2818f9a662e9085 | python -m json.tool

// 결과
{
    "response": {
        "code": 0,
        "jsonrpc": "2.0"
    },
    "response_code": "0"
}
```

### 6. SCORE Transaction 실행 결과 조회 (Query)

``` bash
$ curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc": "2.0","channel":"channel1","method":"get_user_contracts","id":"test_query","params":{"user_id":"lessor"
}}' http://localhost:9000/api/v1/query | python -m json.tool

{
    "response_code": "0",
    "response": {
        "jsonrpc": "2.0",
        "code": 0,
        "response": {
            "user_contracts": [
                {
                    "proposer": "RealEstateAgent",
                    "counterparties": [
                        "leaseholder",
                        "lessor"
                    ],
                    "content": "A\uc544\ud30c\ud2b8 203\ub3d9 803\ud638\ub97c \ubcf4\uc99d\uae08 1500 \uc6d4\uc138 70\uc5d0 \uacc4\uc57d 2019\ub144 8\uc6d4 1\uc77c\uae4c\uc9c0 \uc784\ub300\ud568, \uc784\ub300 \ucde8\uc18c\
uc2dc ~~~ ",
                    "quorum": "3",
                    "approvers": [
                        "RealEstateAgent"
                    ],
                    "contract_id": 1
                }
            ]
        },
        "id": "test_query"
    }
}

```
