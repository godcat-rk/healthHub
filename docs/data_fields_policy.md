# データフィールド保存方針

## 概要
Oura APIから取得できるデータのうち、どのフィールドを保存するか、どのフィールドを除外するかの方針を記載。

## 基本方針
- **日次サマリーデータのみ保存**：時系列データは除外
- **集計値とスコアを優先**：分単位の詳細データは保存しない
- **contributors は JSON型で保存**：柔軟性を保つ

---

## 1. Daily Sleep（睡眠）

### 保存対象
- `id`, `day`, `timestamp`
- `score`: 睡眠スコア（0-100）
- `contributors`: 7つの貢献要素（JSON）
  - deep_sleep, efficiency, latency, rem_sleep, restfulness, timing, total_sleep

### 除外フィールド
なし（すべて保存）

---

## 2. Daily Activity（活動量）

### 保存対象
- `id`, `day`, `timestamp`
- `score`: 活動スコア（0-100）
- `steps`: 歩数
- `active_calories`, `total_calories`: カロリー
- `equivalent_walking_distance`: 相当歩行距離
- `high/medium/low/sedentary_time`: 活動レベル別時間
- `high/medium/low/sedentary_met_minutes`: MET分
- `contributors`: 6つの貢献要素（JSON）

### 除外フィールド（大容量のため）
- **`met.items`**: 2991個の数値配列（分単位のMET値）
  - → 日次集計値（average_met_minutes等）で十分
- **`class_5_min`**: 長い文字列（5分単位の活動分類）
  - → 詳細分析が必要なら将来的に別テーブル化を検討

**現時点の判断**: `class_5_min`は一旦保存するが、将来的にストレージを圧迫する場合は除外を検討

---

## 3. Daily Readiness（レディネス）

### 保存対象
- `id`, `day`, `timestamp`
- `score`: レディネススコア（0-100）
- `temperature_deviation`: 体温偏差
- `temperature_trend_deviation`: 体温トレンド偏差
- `contributors`: 9つの貢献要素（JSON）
  - activity_balance, body_temperature, hrv_balance, previous_day_activity, previous_night, recovery_index, resting_heart_rate, sleep_balance, sleep_regularity

### 除外フィールド
なし

---

## 4. Daily Stress（ストレス）

### 保存対象
- `id`, `day`, `timestamp`
- `stress_high`: 高ストレス時間（秒）
- `recovery_high`: 高回復時間（秒）
- `day_summary`: 日次要約（"normal", "stressful"等）

### 除外フィールド
なし

---

## 5. Daily Resilience（レジリエンス）

### 保存対象
- `id`, `day`, `timestamp`
- `level`: レジリエンスレベル（"solid", "strong"等）
- `contributors`: 3つの貢献要素（JSON）
  - sleep_recovery, daytime_recovery, stress

### 除外フィールド
なし

---

## データサイズ見積もり

| エンドポイント | 1日あたりのサイズ | 1年あたり（365日） |
|--------------|-----------------|------------------|
| daily_sleep | ~500 bytes | ~180 KB |
| daily_activity | ~2 KB (class_5_min含む) | ~730 KB |
| daily_readiness | ~600 bytes | ~220 KB |
| daily_stress | ~300 bytes | ~110 KB |
| daily_resilience | ~400 bytes | ~150 KB |
| **合計** | **~4 KB** | **~1.4 MB** |

`met.items`を除外することで、1日あたり約10KBのストレージを節約。

---

## 将来的な検討事項

1. **時系列データの保存**
   - 必要に応じて別テーブル（`activity_timeseries`等）を作成
   - 詳細分析が必要な場合のみ有効化

2. **contributorsの個別カラム化**
   - JSON型のままでパフォーマンス問題が出た場合
   - 特定のcontributorで頻繁にフィルタ/ソートする場合

3. **データ保持期間**
   - 3年以上経過したデータのアーカイブ化を検討
