# kd-test

## Introduction

1. Demo: https://kd-test-api.samhsieh.xyz


2. 此 Demo 部署在 AWS 中


## Install

### 需求
1. docker

### 步驟
1. 切換至專案並編輯 `.env` 檔案
```
$ cd kd-test
$ vi .env
```


2. 執行 `docker-compose`
```
$ docker-compose up
```

3. 就會看見伺服器成功啟動
http://127.0.0.1:40002
   

## Test

### Postman

1. 打開 postman 並導入 Project 中 `postman` 資料夾中的檔案


2. 切換右上角環境至 `Production`


3. 點選左側目錄，可以看到所有的 Demo API


4. Demo API 皆需要 Token 才可以呼叫，Token 產生方法：
   
   點選`取得 Token` API，按下發送，並複製 Response 中的 `token`。 
   打開右上角的環境，並點選 `Production`，並將其中 `Token` 欄位的 `CURRENT VALUE` 用剛剛的 `Token` 取代即可
   
   
5. 選擇要測試的按下發送即可看到結果

### Curl

取得 Token
```
$ curl --location --request POST 'https://kd-test-api.samhsieh.xyz/token-auth/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "test",
    "password": "12345678"
}'
```

Retrieve Pokemons filter by types
```
$ curl --location --request GET 'https://kd-test-api.samhsieh.xyz/pokemons/?type=Grass' \
   --header 'Authorization: Bearer {{token}}'
```

Retrieve a Pokemon by identifier
```
$ curl --location --request GET 'https://kd-test-api.samhsieh.xyz/pokemons/1' \
   --header 'Authorization: Bearer {{token}}'
```

Create a Pokemon
```
$ curl --location --request POST 'https://kd-test-api.samhsieh.xyz/pokemons/' \
   --header 'Authorization: Bearer {{token}}' \
   --header 'Content-Type: application/json' \
   --data-raw '{
       "number" : "0001",
       "name": "Bulbasaur",
       "types": ["Grass", "Poison"]
   }'
```

Update a Pokemon by identifier 
```
$ curl --location --request PUT 'https://kd-test-api.samhsieh.xyz/pokemons/1' \
   --header 'Authorization: Bearer {{token}}' \
   --header 'Content-Type: application/json' \
   --data-raw '{
       "number" : "0002",
       "name": "Ivysaur",
       "types": ["Grass", "Poison"]
   }'
```

Delete a Pokemon by identifier
```
$ curl --location --request DELETE 'https://kd-test-api.samhsieh.xyz/pokemons/1' \
   --header 'Authorization: Bearer {{token}}'
```

Add / Delete evolutions of Pokemon
```
$ curl --location --request PATCH 'https://kd-test-api.samhsieh.xyz/pokemons/1' \
   --header 'Authorization: Bearer {{token}}' \
   --header 'Content-Type: application/json' \
   --data-raw '{
       "parent_id": 2
   }'
```
