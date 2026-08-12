# TC-PERF-03/04/06/07 — 규모별 데이터 볼륨 티어

원본은 수정하지 않고, Cohesity 소스/Dataset 등록 시 아래 절대경로만 지정해서 규모별
성능 테스트를 수행합니다. 별도 복사본을 만들지 않습니다(대용량이라 복사 자체가 비용이
큼 — 원본 경로를 그대로 protection job의 대상으로 사용).

경로는 `../paths_config.py`의 `GAIA_DATASET_DIR` / `GAIA_WEB_DATASET_DIR` 기준이며,
기본값은 아래와 같습니다(환경 변수 `GAIA_DATASET_DIR` / `GAIA_WEB_DATASET_DIR`로
오버라이드 가능 — 원본 데이터가 다른 위치로 이동한 경우 등):

- `GAIA_DATASET_DIR` 기본값: `/data/richard/data/gaia_dataset`
- `GAIA_WEB_DATASET_DIR` 기본값: `/data/richard/data/gaia_web_dataset`

| 티어 | 목표 | 실제 구성 | 실측 크기 | 회사 수 |
|---|---|---|---|---|
| 1GB | TC-PERF-03 소규모 기준선 | `$GAIA_DATASET_DIR` 중 가장 작은 회사 37개 (목록: `tier_1gb_companies.txt`) | 1.02GB | 37 |
| 10GB | TC-DATA-06 중간 규모 | `$GAIA_DATASET_DIR` 중 작은 회사 130개 (목록: `tier_10gb_companies.txt`) | 10.00GB | 130 |
| 100GB | TC-DATA-06 대규모 | `$GAIA_DATASET_DIR` 전체 (275개 회사) | 109.94GB | 275 |
| 200GB (근사) | TC-PERF-03 최대 규모 | `$GAIA_DATASET_DIR` 전체(109.94GB) + `$GAIA_WEB_DATASET_DIR`(60GB) | ≈170GB | - |

## 참고
- 200GB 정확히 채우려면 `$GAIA_WEB_DATASET_DIR` 만으로 부족(약 30GB 추가 필요). PoC
  목적상 170GB를 "최대 규모 근사치"로 사용하고, 정확히 200GB가 필요하면
  `$GAIA_WEB_DATASET_DIR`의 스킵/에러 없는 정상 문서 중 추가 회사 대신 web 카테고리를
  몇 개 더 포함하면 됩니다.
- `tier_1gb_companies.txt` / `tier_10gb_companies.txt`는 회사 폴더명 목록이며,
  `$GAIA_DATASET_DIR/<회사명>/` 경로와 그대로 매칭됩니다. 아래처럼 절대경로 리스트를
  즉시 만들 수 있습니다:
  ```bash
  GAIA_DATASET_DIR="${GAIA_DATASET_DIR:-/data/richard/data/gaia_dataset}"
  while read -r name; do echo "$GAIA_DATASET_DIR/$name"; done < tier_1gb_companies.txt
  ```
- TC-PERF-04(GPU/CPU/Memory 모니터링), TC-PERF-05(재시작 복구), TC-PERF-02(동시 사용자
  부하)는 데이터 자체보다 인프라/모니터링 설정이 핵심이라 이 문서의 범위 밖입니다.
