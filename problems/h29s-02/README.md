# h29s-02

## schema

```sql
CREATE TABLE 勘定 (勘定科目 TEXT PRIMARY KEY, 期首残高 INT NOT NULL);

CREATE TABLE 会計取引 (取引番号 TEXT PRIMARY KEY, 取引日 DATE NOT NULL);

CREATE TABLE 移動 (
  勘定科目 TEXT REFERENCES 勘定 (勘定科目),
  取引番号 TEXT REFERENCES 会計取引 (取引番号),
  金額 INT NOT NULL,
  PRIMARY KEY (勘定科目, 取引番号)
);
```

## test-01

### data

```sql
INSERT INTO
    勘定 (勘定科目, 期首残高)
VALUES
    ('現金', 1000),
    ('備品', 200);

INSERT INTO
    会計取引 (取引番号, 取引日)
VALUES
    ('0001', '2017-04-01');

INSERT INTO
    移動 (勘定科目, 取引番号, 金額)
VALUES
    ('現金', '0001', -500),
    ('備品', '0001', 500);
```

### expected

```txt
500
```

### query-01

```sql
SELECT
    SUM(金額) AS 残高
FROM
    勘定,
    移動,
    会計取引
WHERE
    勘定.勘定科目 = 移動.勘定科目
    AND 会計取引.取引番号 = 移動.取引番号
    AND 勘定.勘定科目 = '現金'
    AND 取引日 <= '2017-04-30'
```

❌ WA: expected `500` but got `-500`

### query-02

```sql
SELECT
    期首残高 + SUM(金額) AS 残高
FROM
    勘定,
    移動,
    会計取引
WHERE
    勘定.勘定科目 = 移動.勘定科目
    AND 会計取引.取引番号 = 移動.取引番号
    AND 勘定.勘定科目 = '現金'
    AND 取引日 <= '2017-04-30'
GROUP BY
    勘定.勘定科目,
    期首残高
```

✅ AC

### query-03

```sql
SELECT
    残高
FROM
    勘定,
    移動,
    会計取引
WHERE
    勘定.勘定科目 = '現金'
    AND 取引日 <= '2017-04-30'
```

❌ RE: `column "残高" does not exist`

### query-04

```sql
SELECT
    残高
FROM
    勘定,
    移動,
    会計取引
WHERE
    勘定.勘定科目 = 移動.勘定科目
    AND 勘定.勘定科目 = '現金'
    AND 取引日 <= '2017-04-30'
```

❌ RE: `column "残高" does not exist`

