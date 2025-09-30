# healthHub バッチ設計

## 目標
- Oura Ring の睡眠・レディネス・アクティビティ日次サマリーを堅牢に取り込むバッチを構築する。
- 初期コストを抑えつつ、将来的なマルチユーザ拡張に対応できる道筋を確保する。
- 初期段階から観測性・設定管理・テスト体制を整えた構成とする。

## ロードマップ
1. **フェーズ0: 前提整備（1日）**
   - Oura Personal Access Token（PAT）を取得・共有してもらう。
   - Supabase 無料プランでプロジェクトを作成し、データベース（PostgreSQL）接続情報を確認。
   - Supabase Service Role Key／Anon Key を GitHub Secrets に登録。希望するスキーマ名（例: `healthhub`）を決める。
   - リポジトリで使用するブランチ戦略・開発フローを確認。

2. **フェーズ1: プロジェクト土台構築（2〜3日）**
   - Poetry で Python プロジェクトを初期化し、`src/healthhub_batch` 構造を用意。
   - `httpx`・`pydantic`・`sqlalchemy[asyncpg]` など主要依存を追加し、`pytest` と Lint 設定を整備。
   - `typer` ベースの CLI エントリーポイント雛形を作り、設定読み込み（`pydantic-settings`）の仕組みを実装。
   - Makefile／GitHub Actions（Lint + Test）をセットアップ。

3. **フェーズ2: 仮実装での API 呼び出し（2日）**
   - PAT を利用して `/daily_sleep` `/daily_activity` `/daily_stress` `/daily_resilience` を取得するスクリプトを実装。
   - レスポンスから代表的な数値（スコア、歩数、ストレス時間など）を抽出し、ログまたは簡易レポートとして出力。
   - リトライ・例外ハンドリングの初期実装を組み込み、エラー時の挙動を確認。

4. **フェーズ3: データ確認・要件精査（1〜2日）**
   - 取得した JSON のフィールド一覧とサンプル値を整理し、保存対象の指標を確定。
   - 保存期間や再取得ポリシー（再実行時の上書き・欠損リカバリ）を合意。
   - 必要に応じて追加エンドポイントやメタ情報の取得可否を検討。

5. **フェーズ4: 永続化設計（2〜3日）**
   - Supabase/PostgreSQL 向けにテーブルスキーマ案を設計（睡眠・活動・ストレス・レジリエンス・ユーティリティテーブル）。
   - `alembic` で初期マイグレーションを作成し、Supabase DB へ適用する CLI フローを整える。
   - `INSERT ... ON CONFLICT` による upsert 方針と制約定義（PK・ユニーク制約）を文書化。

6. **フェーズ5: バッチ本実装（4〜5日）**
   - CLI から日付範囲を受け取って API → 変換 → Supabase/PostgreSQL 永続化までを実行するパイプラインを構築。
   - cron 相当の GitHub Actions ワークフローを用意し、Secrets から PAT・DB 接続情報を取得。
   - INFO/ERROR ログと Slack 通知（Webhook）を組み込み、テストで動作確認。

7. **フェーズ6: テスト強化と運用準備（2日）**
   - ユニットテスト・統合テストを充実させ、VCR.py／`respx` で API モックを安定化。
   - 本番運用 Runbook（トークン更新手順、GitHub Actions 再実行手順、Supabase のバックアップ方法）を整備。
   - 将来の多ユーザ化やデータウェアハウス連携に向けた TODO リストを整理。

## 取得エンドポイントと保存指標

| エンドポイント | 取得目的 | 主キー | 保存する主要フィールド例 |
| ------------- | ---------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/v2/usercollection/daily_sleep` | 日次の睡眠スコアと要素別貢献度を集計する | `user_id` + `day` | `score`, `contributors.deep_sleep`, `contributors.rem_sleep`, `contributors.total_sleep`, `contributors.restfulness`, `contributors.efficiency`, `contributors.latency`, `contributors.timing`, `timestamp`, `id` |
| `/v2/usercollection/daily_activity` | 日次の活動量（歩数・カロリー・貢献度）を把握する | `user_id` + `day` | `score`, `steps`, `total_calories`, `active_calories`, `target_calories`, `equivalent_walking_distance`, `inactivity_alerts`, `non_wear_time`, `sedentary_time`, `resting_time`, `high_activity_time`, `medium_activity_time`, `low_activity_time`, `contributors.meet_daily_targets`, `contributors.stay_active`, `contributors.training_volume`, `contributors.training_frequency`, `contributors.move_every_hour`, `contributors.recovery_time`, `timestamp`, `id` |
| `/v2/usercollection/daily_stress` | 日次のストレス状況とリカバリ時間を追跡する | `user_id` + `day` | `day_summary`, `stress_high`, `stress_medium`, `stress_low`, `recovery_high`, `recovery_medium`, `recovery_low`, `timestamp`, `id` |
| `/v2/usercollection/daily_resilience` | 日次のレジリエンスレベルをモニタリングする | `user_id` + `day` | `level`, `contributors.sleep_recovery`, `contributors.daytime_recovery`, `contributors.stress`, `timestamp`, `id` |
| `/v2/usercollection/daily_readiness` | レディネススコアと体温変化を管理する | `user_id` + `day` | `score`, `temperature_deviation`, `temperature_trend_deviation`, `contributors.activity_balance`, `contributors.body_temperature`, `contributors.previous_day_activity`, `contributors.previous_night`, `contributors.recovery_index`, `contributors.resting_heart_rate`, `contributors.sleep_balance`, `contributors.hrv_balance`, `timestamp`, `id` |
| `/v2/usercollection/daily_spo2` | 夜間 SpO₂ と呼吸障害指数を確認する | `user_id` + `day` | `spo2_percentage.average`, `breathing_disturbance_index`, `timestamp`, `id` |
| `/v2/usercollection/sleep` | 睡眠セッション詳細（必要に応じて） | `user_id` + `id` | `total_sleep_duration`, `deep_sleep_duration`, `rem_sleep_duration`, `light_sleep_duration`, `awake_time`, `efficiency`, `average_hrv`, `lowest_heart_rate`, `bedtime_start`, `bedtime_end`, `sleep_phase_5_min`, `timestamp`, `day` |
| `/v2/usercollection/workout` | 運動セッション記録（オプション） | `user_id` + `id` | `activity`, `start_datetime`, `end_datetime`, `calories`, `distance`, `intensity`, `label`, `source`, `day` |
| `/v2/usercollection/session` | 瞑想などのセッション（オプション） | `user_id` + `id` | `type`, `start_datetime`, `end_datetime`, `mood`, `heart_rate`, `heart_rate_variability`, `motion_count`, `day` |
| `/v2/usercollection/heartrate` | 心拍時系列（必要時のみ） | `user_id` + `timestamp` | `bpm`, `source` |
| `/v2/usercollection/vO2_max` | VO₂ Max 長期指標 | `user_id` + `timestamp` | `vo2_max`, `day` |
| `/v2/usercollection/daily_cardiovascular_age` | 心血管年齢 | `user_id` + `day` | `vascular_age`, `timestamp`, `id` |
| `/v2/usercollection/sleep_time` | 推奨睡眠時間情報 | `user_id` + `day` | `status`, `optimal_bedtime`, `recommendation`, `timestamp`, `id` |
| `/v2/usercollection/tag` / `enhanced_tag` | ユーザタグ・拡張タグ | `user_id` + `id` | `day`, `timestamp`, `text`/`comment`, `tag_type_code`, `start_time`, `end_time` |
| `/v2/usercollection/rest_mode_period` | レストモード設定期間 | `user_id` + `id` | `start_day`, `start_time`, `end_day`, `end_time`, `episodes` |

## 技術スタック

### プログラミング言語とランタイム
- データ取得やスケジューリング支援のエコシステムが豊富な Python 3.11 LTS（Linux サーバ上）を採用。
- Poetry が管理する `venv` を用いて依存関係を固定し、再現性のあるビルドを確保する。

### コアライブラリ
- リトライミドルウェアを備えた非同期対応 HTTP クライアントとして `httpx` を利用。
- API レスポンスの厳格なスキーマ検証と型安全な変換に `pydantic` を使用。
- Supabase/PostgreSQL への接続に `sqlalchemy` + `asyncpg` を採用し、将来のスキーマ拡張にも柔軟に対応。
- テーブル定義の進化に合わせたスキーママイグレーションに `alembic` を使用。
- 構造化された JSON ログ出力のため、標準ログとの連携を前提に `structlog` を採用。

### 永続化レイヤ
- Supabase（無料プラン）のマネージド PostgreSQL を永続化先とし、コスト 0 円で運用を開始。
- スキーマ例: `healthhub.daily_sleep`, `healthhub.daily_activity`, `healthhub.daily_stress`, `healthhub.daily_resilience` など。全テーブルで `user_id` + 日付 or ドキュメント ID を主キーに設定。
- `INSERT ... ON CONFLICT` を利用して冪等アップサートを実装し、再実行時の重複や欠損を防止。
- Supabase の行レベルセキュリティ（RLS）は管理用途なので無効化またはバッチ専用ロールで管理。将来のユーザ向け API では RLS を活用できるよう余地を残す。

### 設定とシークレット管理
- 本番実行で必要な値: `OURA_PAT`, `SUPABASE_DB_URL`（`postgres://` 形式）, `SUPABASE_SERVICE_ROLE_KEY`（必要なら REST 呼び出し用）。
- Secrets は GitHub Actions Secrets に登録し、ローカル開発では `.env` に同じキー名でセット。
- `pydantic-settings` で必須の環境変数を検証し、欠落時は起動エラーとする。

### 観測性とアラート
- 各 API 呼び出し（エンドポイント、期間、リクエスト ID）を INFO ログに、失敗時はスタックトレース付きで ERROR ログに出力。
- ログは JSON 形式とし、GitHub Actions のログ／将来的なクラウドログ基盤への転送に備える。
- リトライ上限を超えた致命的失敗時は Slack Webhook（Secrets に URL を保存）で通知。
- Supabase 側のメトリクスはダッシュボードで確認し、必要に応じてクエリパフォーマンスを監視。

### テスト戦略
- 共通テストハーネスとして `pytest`、非同期コード向けに `pytest-asyncio` を使用。
- VCR.py または `respx` で Oura API レスポンスをモックし、安定したテストを実現。
- Supabase 用にはテスト用 PostgreSQL（Docker の `postgres:15-alpine` など）を立て、マイグレーションとアップサート処理の回帰テストを実行。

### パッケージングと CI/CD
- `src/healthhub_batch` 配下にインストール可能なパッケージとしてプロジェクト構成。
- Makefile で `make lint`・`make test`・`make run` などを定義し開発者体験を向上。
- GitHub Actions でプッシュ時にテストと Lint を実行。スケジュールトリガーのワークフローは別ファイル（例: `.github/workflows/daily-batch.yml`）に定義。

### バッチ運用フロー（GitHub Actions + Supabase）
1. `schedule` トリガー（例: 毎日 06:00 JST）でワークフローを起動。
2. `actions/checkout` → Poetry キャッシュ復元 → 依存をインストール。
3. Secrets から `OURA_PAT`, `SUPABASE_DB_URL`, `SUPABASE_SERVICE_ROLE_KEY` を取得し、環境変数にエクスポート。
4. Python CLI を `--start-date` `--end-date` 付きで実行し、Supabase の PostgreSQL に対して upsert。
5. 結果ログを標準出力で確認し、失敗時は Slack 通知。成功時は Supabase 上にデータが蓄積。
6. 必要に応じて Supabase の自動バックアップ（無料枠の 7 日分）を確認し、重要な節目ではダンプをローカルへ取得。

### 将来の検討事項
- マルチユーザ運用開始時に Supabase Auth と連携し、ユーザごとのトークン保管・アクセス制御を実現。
- ワークフロー負荷が増えた場合は Supabase Edge Functions や別クラウドのジョブサービス（Cloud Run Jobs など）への移行を検討。
- 下流レポーティングが成熟した段階で Supabase Data Studio や BigQuery/Snowflake への連携を評価。

## データベーススキーマ案（Supabase/PostgreSQL）

### 共通方針
- 全テーブルに `user_id`（UUID）、`created_at`（TIMESTAMPTZ、`now()` デフォルト）、`source_timestamp`（Oura 側タイムスタンプ）を持たせ、再取得時の upsert と監査を容易にする。
- 日次サマリー系は `day` を `date` 型とし、`PRIMARY KEY (user_id, day)` を設定。セッション系は `PRIMARY KEY (user_id, document_id)` とする。
- スコア類は 0–100 の整数なので `smallint`、時間（秒）・歩数などは `integer`、体温偏差やレジリエンス寄与のような小数は `numeric(5,2)` を基本とする。
- Supabase 管理者ロール（Service Role Key）でバッチを実行し、RLS は当面無効化。将来のアプリ連携で RLS を再検討する。

### テーブル定義

#### `healthhub.daily_sleep_summaries`
| カラム | 型 | NOT NULL | 備考 |
|-|-|-|-|
| user_id | uuid | ✔ | バッチ設定で管理するユーザ識別子 |
| day | date | ✔ | 日次サマリー日付（主キー） |
| score | smallint |  | 睡眠スコア（0-100） |
| contributors_deep_sleep | smallint |  | 深い睡眠の貢献度 |
| contributors_rem_sleep | smallint |  | REM 睡眠貢献度 |
| contributors_total_sleep | smallint |  | 総睡眠貢献度 |
| contributors_restfulness | smallint |  | 安らかさ |
| contributors_efficiency | smallint |  | 効率 |
| contributors_latency | smallint |  | 入眠時間 |
| contributors_timing | smallint |  | タイミング |
| source_timestamp | timestamptz |  | Oura 返却の timestamp |
| document_id | uuid | ✔ | Oura ドキュメント ID（ユニーク制約） |
| created_at | timestamptz | ✔ | `now()` デフォルト |

`PRIMARY KEY (user_id, day)`、`UNIQUE (user_id, document_id)`。

#### `healthhub.daily_activity_summaries`
| カラム | 型 | NOT NULL | 備考 |
|-|-|-|-|
| user_id | uuid | ✔ | |
| day | date | ✔ | |
| score | smallint |  | 活動スコア |
| steps | integer |  | 総歩数 |
| total_calories | integer |  | 総消費 kcal |
| active_calories | integer |  | 活動による消費 kcal |
| target_calories | integer |  | 目標 kcal |
| equivalent_walking_distance | integer |  | m 単位 |
| inactivity_alerts | smallint |  | 非活動アラート回数 |
| non_wear_time | integer |  | 非装着時間（秒） |
| resting_time | integer |  | 安静時間（秒） |
| sedentary_time | integer |  | 座位時間（秒） |
| low_activity_time | integer |  | 低強度活動時間（秒） |
| medium_activity_time | integer |  | 中強度活動時間（秒） |
| high_activity_time | integer |  | 高強度活動時間（秒） |
| contributors_meet_daily_targets | smallint |  | 目標達成度 |
| contributors_stay_active | smallint |  | こまめな活動 |
| contributors_training_volume | smallint |  | トレーニング量 |
| contributors_training_frequency | smallint |  | トレーニング頻度 |
| contributors_move_every_hour | smallint |  | 1時間ごとの起立 |
| contributors_recovery_time | smallint |  | 回復時間 |
| source_timestamp | timestamptz |  | |
| document_id | uuid | ✔ | |
| created_at | timestamptz | ✔ | `now()` |

`PRIMARY KEY (user_id, day)`、`UNIQUE (user_id, document_id)`。

#### `healthhub.daily_readiness_summaries`
| カラム | 型 | NOT NULL | 備考 |
|-|-|-|-|
| user_id | uuid | ✔ | |
| day | date | ✔ | |
| score | smallint |  | レディネススコア |
| temperature_deviation | numeric(5,2) |  | 体温偏差（℃） |
| temperature_trend_deviation | numeric(5,2) |  | 体温トレンド偏差（℃） |
| contributors_activity_balance | smallint |  | 活動バランス |
| contributors_body_temperature | smallint |  | 体温要素 |
| contributors_previous_day_activity | smallint |  | 前日の活動 |
| contributors_previous_night | smallint |  | 前夜の睡眠 |
| contributors_recovery_index | smallint |  | 回復指数 |
| contributors_resting_heart_rate | smallint |  | 安静時心拍 |
| contributors_sleep_balance | smallint |  | 睡眠バランス |
| contributors_hrv_balance | smallint |  | HRV バランス |
| source_timestamp | timestamptz |  | |
| document_id | uuid | ✔ | |
| created_at | timestamptz | ✔ | |

`PRIMARY KEY (user_id, day)`、`UNIQUE (user_id, document_id)`。

#### `healthhub.daily_stress_summaries`
| カラム | 型 | NOT NULL | 備考 |
|-|-|-|-|
| user_id | uuid | ✔ | |
| day | date | ✔ | |
| day_summary | text |  | `restored`/`normal`/`stressful` |
| stress_high | integer |  | 高ストレス時間（秒） |
| stress_medium | integer |  | 中ストレス時間（秒） |
| stress_low | integer |  | 低ストレス時間（秒） |
| recovery_high | integer |  | 高リカバリ時間（秒） |
| recovery_medium | integer |  | 中リカバリ時間（秒） |
| recovery_low | integer |  | 低リカバリ時間（秒） |
| source_timestamp | timestamptz |  | |
| document_id | uuid | ✔ | |
| created_at | timestamptz | ✔ | |

`PRIMARY KEY (user_id, day)`、`UNIQUE (user_id, document_id)`。

#### `healthhub.daily_resilience_summaries`
| カラム | 型 | NOT NULL | 備考 |
|-|-|-|-|
| user_id | uuid | ✔ | |
| day | date | ✔ | |
| level | text |  | `solid` などのステージ名称 |
| contributors_sleep_recovery | numeric(5,2) |  | 睡眠回復（0-100） |
| contributors_daytime_recovery | numeric(5,2) |  | 日中回復（0-100） |
| contributors_stress | numeric(5,2) |  | ストレス寄与（0-100） |
| source_timestamp | timestamptz |  | |
| document_id | uuid | ✔ | |
| created_at | timestamptz | ✔ | |

`PRIMARY KEY (user_id, day)`、`UNIQUE (user_id, document_id)`。

### 補助テーブル
- **`healthhub.job_runs`**: 実行日時、対象期間、処理件数、ステータス、エラー要約、GitHub Actions 実行 ID を保存し、再実行やトラブルシュートに使う。
- **`healthhub.users`**: バッチ対象ユーザのメタ情報（`user_id`, `oura_pat_alias`, `timezone`, `is_active`, `created_at`）。将来の多 PAT 対応に備える。

### マイグレーション・アップサート
- 初期は `alembic` で上記テーブルを作成するマイグレーションを用意し、CI/CD から Supabase DB に適用する。
- upsert の例:
  ```sql
  INSERT INTO healthhub.daily_sleep_summaries (...)
  VALUES (...)
  ON CONFLICT (user_id, day)
  DO UPDATE SET
    score = EXCLUDED.score,
    contributors_deep_sleep = EXCLUDED.contributors_deep_sleep,
    updated_at = now();
  ```
  `updated_at` カラムを追加する場合は `TIMESTAMPTZ DEFAULT now()` を設定し、`ON CONFLICT` で更新する。
- `source_timestamp` を確認し、API から新鮮なデータが届いた場合のみ上書きするロジックをアプリ側で実装することも検討。