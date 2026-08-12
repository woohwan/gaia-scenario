"""
gaia_scenario 절대경로 설정.

이 저장소(gaia_scenario)는 cohesity-poc과 완전히 분리되어 존재합니다. 대용량
원본 데이터(gaia_dataset, gaia_web_dataset)만 복제하지 않고 절대경로로 직접
가리킵니다(각각 약 103GB/60GB라 저장소에 넣지 않음). 나머지 산출물(TC-RAG
golden set, TC-DATA-01 포맷별 QA 샘플 등)은 전부 poc_dataset/ 안에 이미
복사되어 있어 별도 경로 설정이 필요 없습니다.

원본 데이터 위치가 바뀌면(다른 머신으로 옮기는 경우 등) 아래 환경 변수로
오버라이드하면 됩니다.
"""
import os
from pathlib import Path

# DART 공시 문서 원본 (약 103GB)
GAIA_DATASET_DIR = Path(os.environ.get(
    "GAIA_DATASET_DIR",
    "/data/richard/data/gaia_dataset",
))

# 웹 수집 문서 원본 (약 60GB)
GAIA_WEB_DATASET_DIR = Path(os.environ.get(
    "GAIA_WEB_DATASET_DIR",
    "/data/richard/data/gaia_web_dataset",
))

# 이 저장소(gaia_scenario) 자신의 루트 — 어디로 옮겨져도 자동으로 맞춰짐
SCENARIO_ROOT = Path(__file__).parent
