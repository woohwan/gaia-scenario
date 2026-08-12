# PoC 데이터셋 — 시나리오 테스트 케이스 대응

이 저장소 루트의 `cohesity_gaia_poc_testcases.md`에 정의된 50개 테스트 케이스를
실행하는 데 필요한 데이터를 준비한 폴더입니다. **원본(`gaia_dataset/`,
`gaia_web_dataset/`)은 전혀 수정하지 않았고**, 필요한 만큼만 복사하거나 신규 합성했습니다.
신규 합성 데이터는 전부 완전 가상/합성이며 실존 인물·기업 정보가 아닙니다.

이 저장소는 cohesity-poc과 완전히 분리되어 있습니다. TC-RAG golden set, TC-DATA-01
포맷별 QA 샘플 등은 전부 poc_dataset/ 안에 복사되어 있고, 대용량 원본(gaia_dataset,
gaia_web_dataset)만 크기 때문에 절대경로로 직접 가리킵니다(아래 "절대경로 설정" 참고).

## 절대경로 설정 (`paths_config.py`)
대용량 원본(103GB/60GB)은 복제하지 않고 절대경로로 직접 가리킵니다. 기본값은
`paths_config.py`에 정의되어 있고, 환경 변수로 오버라이드할 수 있습니다 (다른 머신으로
옮긴 경우 등):

| 변수 | 기본값 |
|---|---|
| `GAIA_DATASET_DIR` | `/data/richard/data/gaia_dataset` |
| `GAIA_WEB_DATASET_DIR` | `/data/richard/data/gaia_web_dataset` |

## TC 코드 ↔ 폴더 매핑

| 대분류 | 관련 TC | 폴더 | 구성 방식 |
|---|---|---|---|
| FUNC | TC-FUNC-01~03 | `TC-FUNC/sample_dataset/` | gaia_dataset에서 003230_삼양식품(123MB, 233파일) 복사 (독립) |
| RAG | TC-RAG-01~07 | `TC-RAG/` | 기존 LLM 생성 QA 200개에서 재샘플링 + 무응답/모호질문 신규 작성해 복사 완료(독립). 실채점은 `$GAIA_DATASET_DIR` 필요 |
| DATA | TC-DATA-01 | `TC-DATA-01_format_coverage/` | 동일 내용 8포맷 신규 합성(독립) + 포맷별 QA 25개씩 샘플링해 복사 완료(독립) |
| DATA | TC-DATA-03/04/05 | `TC-DATA-03_05_freshness/` | 값 변경 전/후 문서, 삭제 테스트용 문서 신규 합성 (독립) |
| DATA | TC-DATA-06 | `PERF/volume_tiers.md` | `$GAIA_DATASET_DIR` 크기별 서브셋 (복사 없음, 경로만 참조) |
| DATA | TC-DATA-07 | `TC-DATA-07_corrupt_files/` | 정상/손상/암호화/빈/미지원 파일 신규 합성 (독립) |
| DATA | TC-DATA-02, TC-DATA-08 | — | 데이터 준비 불필요 (Cohesity Support 활성화 절차 / UI 확인 사항) |
| RBAC | TC-RBAC-01~08 | `TC-RBAC/` | Dataset A=Finance(`$GAIA_DATASET_DIR` 재사용) + Dataset B=HR(신규 합성, 독립) |
| SEC | TC-SEC-03/04/05 | `TC-SEC/injection_docs/` + `TC-RBAC/dataset_hr_synthetic/` | 인젝션 문구 삽입 문서 신규 합성 (독립) |
| SEC | TC-SEC-01, 02, 06 | — | 데이터 준비 불필요 (환경/설정 확인 사항) |
| PERF | TC-PERF-01~07 | `PERF/volume_tiers.md` | `$GAIA_DATASET_DIR` / `$GAIA_WEB_DATASET_DIR` 그대로 활용 |
| API | TC-API-01~07 | — | 위 Dataset이 인덱싱되어 있으면 데이터 준비 불필요 |

## 원칙
- 원본(`gaia_dataset/`, `gaia_web_dataset/`) 경로는 read-only로만 참조했고, 어떤
  파일도 수정·삭제하지 않았습니다.
- 큰 원본 데이터를 통째로 복제하지 않고, 케이스별로 필요한 최소량만 추출하거나
  (FUNC 1개사 123MB, TC-RAG golden set, TC-DATA-01 포맷별 QA 샘플) 아예 새로
  합성했습니다(RBAC용 HR 문서, SEC 인젝션 문서, DATA-01/07 fixture 등). 이렇게
  복사·샘플링된 산출물은 전부 poc_dataset/ 안에 있어 원본이 없어도 그대로 읽을 수
  있습니다.
- 대용량 성능 티어(TC-DATA-06, TC-PERF-03)와 골든셋 실채점 대상 문서만 복사 대신
  `paths_config.py`의 절대경로로 원본을 직접 가리키는 방식으로 처리했습니다
  (불필요한 디스크 사용 방지, 원본이 삭제/이동되지 않는 한 계속 유효 — 이동 시
  `GAIA_DATASET_DIR`/`GAIA_WEB_DATASET_DIR` 환경변수로 오버라이드).

## 알려진 한계 / 후속 결정 필요
- TC-RAG-07 네덜란드어 부분은 원본 데이터가 전혀 없어 이번 범위에서 제외했습니다
  (2026-08-11 확인). 필요 시 영어 문서를 LLM으로 번역해 별도 합성해야 합니다.
- TC-DATA-02(Continuous Indexing 활성화), TC-DATA-08(Mailbox/OneDrive 제약),
  TC-SEC-01/02/06, TC-PERF-02/04/05, TC-API-06 등은 데이터가 아니라 환경 설정/인프라
  확인이 핵심이라 이 폴더의 범위 밖입니다.
