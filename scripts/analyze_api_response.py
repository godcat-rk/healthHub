#!/usr/bin/env python3
"""Analyze Oura API response structure and create data models."""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

# プロジェクトルートをPATHに追加
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from healthhub_batch.config import Settings
from healthhub_batch.oura_client import OuraClient


async def analyze_responses() -> None:
    """Fetch and analyze API responses."""
    settings = Settings()

    # 直近3日分のデータを取得
    from datetime import date, timedelta
    end_date = date.today()
    start_date = end_date - timedelta(days=3)

    endpoints = [
        "daily_sleep",
        "daily_activity",
        "daily_stress",
        "daily_resilience",
        "daily_readiness",
    ]

    # 出力ディレクトリを作成
    output_dir = Path(__file__).parent.parent / "artifacts" / "api_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    analysis_results = {}

    async with OuraClient(settings.oura_pat) as client:
        for endpoint in endpoints:
            print(f"\n{'='*80}")
            print(f"Analyzing: {endpoint}")
            print('='*80)

            method = getattr(client, f"get_{endpoint}")
            response = await method(start_date.isoformat(), end_date.isoformat())

            data_list = response.get("data", [])

            if not data_list:
                print(f"[ERROR] No data returned for {endpoint}")
                continue

            print(f"[OK] Records found: {len(data_list)}")

            # 最初のレコードの構造を分析
            sample = data_list[0]

            # フィールド一覧とデータ型
            field_info = {}
            for key, value in sample.items():
                value_type = type(value).__name__
                sample_value = value
                field_info[key] = {
                    "type": value_type,
                    "sample": sample_value,
                }

            analysis_results[endpoint] = {
                "record_count": len(data_list),
                "sample_record": sample,
                "field_summary": field_info,
            }

            # エンドポイントごとにJSONファイルを保存
            output_file = output_dir / f"{endpoint}_analysis.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(analysis_results[endpoint], f, indent=2, ensure_ascii=False)

            print(f"[SAVED] File: {output_file}")

    # 全体サマリーも保存
    summary_file = output_dir / "summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(analysis_results, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*80}")
    print(f"[COMPLETE] Analysis finished!")
    print(f"[OUTPUT] Results saved to: {output_dir}")
    print('='*80)


if __name__ == "__main__":
    asyncio.run(analyze_responses())