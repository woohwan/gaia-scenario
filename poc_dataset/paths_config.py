"""
gaia_scenario 절대경로 설정.

이 저장소(gaia_scenario)는 cohesity-poc 밖에 독립적으로 존재할 수 있습니다
(gaia_eval과 동일한 패턴). 대용량 원본 데이터는 옮기지 않고, cohesity-poc의
원본 경로를 절대경로로 직접 가리킵니다. cohesity-poc를 다른 위치로 옮기거나
원본 데이터 경로가 바뀌면 아래 환경 변수로 오버라이드하면 됩니다.
"""
import os
from pathlib import Path

# DART 공시 문서 원본 (cohesity-poc/gaia_dataset, 약 110GB)
GAIA_DATASET_DIR = Path(os.environ.get(
    "GAIA_DATASET_DIR",
    "/data/richard/cohesity-poc/gaia_dataset",
))

# 웹 수집 문서 원본 (cohesity-poc/gaia_web_dataset, 약 60GB)
GAIA_WEB_DATASET_DIR = Path(os.environ.get(
    "GAIA_WEB_DATASET_DIR",
    "/data/richard/cohesity-poc/gaia_web_dataset",
))

# collector/eval 파이프라인이 이미 생성해 둔 포맷별 QA 산출물 (TC-DATA-01 참고용)
COLLECTOR_EVAL_OUTPUT_DIR = Path(os.environ.get(
    "COLLECTOR_EVAL_OUTPUT_DIR",
    "/data/richard/cohesity-poc/collector/eval/output",
))

# gaia_ragas 파이프라인의 DART 기반 QA 산출물 (TC-RAG 골든셋의 출처)
GAIA_RAGAS_EVAL_DIR = Path(os.environ.get(
    "GAIA_RAGAS_EVAL_DIR",
    "/data/richard/cohesity-poc/gaia_ragas/eval",
))

# 이 저장소(gaia_scenario) 자신의 루트 — 어디로 옮겨져도 자동으로 맞춰짐
SCENARIO_ROOT = Path(__file__).parent
