# Lecture 01 Answers

## Exercises

- Model's answer to the course-specific question (the 3 homework levels; a summary is fine):
- What you noticed when comparing it with the correct meaning in the glossary:
- Token counts you displayed (input / output):

## Homework

- Level attempted: Implementation
- What you did:　会話履歴を保持するチャット機能の追加
- Results:達成
- Observations and questions:下記
## 実装課題：会話履歴を保持するチャット機能の追加

### 1. 実施したこと

`app/ask.py` に会話履歴を保持するチャット機能を追加した。元のコードは一度の質問に回答する仕組みだったが、変更後は過去の質問と回答を踏まえて会話を続けられるようにした。

### 2. 実装方法

Google Gen AI SDKの `client.chats.create(model=MODEL)` を使い、チャットセッションを作成した。セッションはループの前に一度だけ作成し、`while` ループ内で入力を受け取り、同じセッションの `send_message()` に質問を送るようにした。

また、`--chat` オプションを追加し、以下のコマンドで会話を開始できるようにした。

```bash
uv run python -m app.ask --chat
```

`exit` と入力すると終了する。従来の単発質問の機能も残した。

### 3. 動作確認と結果

次の順番で入力し、回答を確認した。

| 入力 | 回答の概要 |
|---|---|
| 私が今勉強しているのはPandasです。 | Pandasの概要や学習項目について回答した。 |
| 私が勉強しているものは何ですか？ | 「Pandas（パンダス）」と回答した。 |
| それでできることを初心者向けに3つ教えてください。 | Pandasの機能として、表形式でのデータ整理、条件に応じた抽出、計算・集計の3つを説明した。 |

2回目の質問には学習対象の名前を含めていないが、最初に伝えたPandasを正しく回答できた。また、3回目の「それ」という指示語もPandasとして解釈しており、過去の会話を踏まえた応答を確認できた。

### 4. 考察

会話履歴を保持することで、ユーザーが毎回前提を説明し直さなくても、続きの質問ができるようになった。

この機能はモデル自体を追加学習するものではなく、SDKが管理する過去のやり取りを次のリクエストに含めることで実現している。今回の実装では履歴をファイルに保存していないため、プログラムを終了して起動し直すと、会話履歴は引き継がれない。

今回確認したのは短い会話1例であり、長い会話や話題が切り替わる場合にも正しく文脈を参照できるかは未確認である。また、会話の文脈を保持できることと、回答内容が常に正確であることは別である。今後は、会話が長くなった場合の応答や、履歴の増加によるトークン数・応答時間への影響も確認したい。