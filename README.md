# DB スぺ判定くん

## 使い方

1. `problems/<problem-id>/schema.sql` にスキーマを記述
2. `problems/<problem-id>/question.txt` に問題文を記述
3. `problems/<problem-id>/input.sql` に入力例を記述
4. `problems/<problem-id>/output.txt` に出力例を記述
5. `problems/<problem-id>/query-[ア|イ|ウ|エ].sql` にクエリを記述
6. Actions が走り、実行結果を `problems/<problem-id>/README.md` にてお知らせ

> [!WARNING]
> 5. の正解のクエリのみ通すよう、3. のテストケースを設定すること。
