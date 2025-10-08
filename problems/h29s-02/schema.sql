CREATE TABLE 勘定 (勘定科目 TEXT PRIMARY KEY, 期首残高 INT NOT NULL);

CREATE TABLE 会計取引 (取引番号 TEXT PRIMARY KEY, 取引日 DATE NOT NULL);

CREATE TABLE 移動 (
  勘定科目 TEXT REFERENCES 勘定 (勘定科目),
  取引番号 TEXT REFERENCES 会計取引 (取引番号),
  金額 INT NOT NULL,
  PRIMARY KEY (勘定科目, 取引番号)
);
