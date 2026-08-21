# 3. 데이터/인덱싱 (TC-DATA-01~07)

파일 포맷, 인덱싱 갱신, 데이터 변경/삭제 반영, 대용량 처리 등 데이터 계층을
검증합니다. **TC-DATA-08(Include-Exclude 제약)은 이번 범위에서 제외**했습니다. 나머지
7개는 UI/인프라 기반이라 API 없이 수행 가능합니다.

---

## TC-DATA-01 — 지원 파일 포맷별 인덱싱/답변 정확도 `[P2]`

**목적**: 동일 내용을 여러 포맷으로 준비했을 때 포맷과 무관하게 동일 수준의 답변
품질이 나오는지 확인. 공식 지원 목록: .doc/.docx, .xls/.xlsx, .ppt/.pptx, .pdf/.odf,
.rtf/.txt, .html, .xml.

### 데이터 준비 (생성 방법 포함)
1. **동일 내용 fixture (엄격 비교용)** — 이 저장소의
   `poc_dataset/TC-DATA-01_format_coverage/` 폴더에 있는 `content.docx`, `content.xlsx`,
   `content.pptx`, `content.pdf`, `content.rtf`, `content.txt`, `content.html`,
   `content.xml` 8개 파일. 데이터 보존정책 안내 문서(표 3행 포함, [QA_format_fixture.md](QA_format_fixture.md)
   1부 4개 질문의 정답이 전부 담겨 있음)를 8개 포맷으로 완전히 동일한 내용으로 합성해 둔
   것입니다(이미 생성 완료, 업로드만 하면 됨).
2. **대규모 포맷별 커버리지 (참고용, 선택)** — [QA_format_fixture.md](QA_format_fixture.md)
   2부에 포맷 그룹당 25개씩 총 100개 질문-정답-근거파일이 정리되어 있습니다(원본은
   `poc_dataset/TC-DATA-01_format_coverage/qa_pairs_*.json`이며 이 문서에 전부 옮겨
   적어 두었으므로 json 파일을 직접 열 필요는 없습니다). 이 절차는 생략하고 1번 fixture
   만으로 진행해도 TC-DATA-01의 핵심 판정(포맷 간 답변 편차)은 충분합니다.
3. Dataset 등록: `content.*` 8개 파일을 NAS 소스로 백업 → `format-fixture` Dataset 생성
   (0.4 레지스트리 #5, 또는 `finance-core`에 얹어도 무방). 2번 대규모 커버리지 세트를
   함께 검증하려면 `perf-200gb`(0.4 레지스트리 #9, `$GAIA_WEB_DATASET_DIR` 전체 포함)
   Dataset을 사용합니다.

### 테스트 수행 절차 — 1) 엄격 비교
1. `format-fixture`(또는 `finance-core`) Dataset 선택.
2. [QA_format_fixture.md](QA_format_fixture.md) 1부의 4개 질문을 **8개 포맷 각각에
   대해** 순서대로 질의(동일 질문을 8번 반복 입력하며, 매번 답변이 어느 포맷 파일을
   근거로 했는지 Citation으로 확인).
3. 8개 포맷 모두 동일한 정답이 나오는지, Citation이 해당 포맷 파일을 정확히 가리키는지
   기록.

### 테스트 수행 절차 — 2) 대규모 포맷별 커버리지 (참고용)
1. `perf-200gb` Dataset 선택.
2. [QA_format_fixture.md](QA_format_fixture.md) 2부에서 포맷 그룹별로 5~10개씩 골라
   질문을 그대로 질의.
3. 문서에 적힌 정답과 Gaia 답변을 비교해 포맷별 정답률을 집계. 이 세트는 포맷 간
   내용이 서로 달라 절대 비교용이 아니라 "포맷 자체 파싱 실패 여부" 확인 용도입니다.

### 예상 결과 / 합격 기준
- 1)번: 8개 포맷 모두 동일 답변 (편차 0).
- 2)번: 포맷 간 정답률 편차 10%p 이내, 표/병합셀 등 특수 구조(xlsx) 별도 확인.

### 결과 기록
| 포맷 | Q1(90일) | Q2(30일/보안팀) | Q3(2026-08-01) | Q4(365일) | Citation 정확 |
|---|---|---|---|---|---|
| docx/xlsx/pptx/pdf/rtf/txt/html/xml | PASS/FAIL | | | | |

| 포맷 그룹 | 샘플 수 | 정답 수 | 정답률 |
|---|---|---|---|
| pdf / docx·doc / xlsx·xls·csv / ppt·pptx | | | |

---

## TC-DATA-02 — Continuous Indexing 활성화 확인 `[P1]`

**목적**: Continuous Indexing 옵션이 정상적으로 노출/적용되는지 확인. 이 TC는
데이터 준비가 필요 없고 환경 설정 확인이 핵심입니다.

> **어디서**: `freshness` Dataset을 만드는 Create Dataset 화면(아래 TC-DATA-03이 이 Dataset을
> 그대로 이어받아 사용).
> **어떻게**: Cohesity Support에 Continuous Indexing 활성화를 요청 → Dataset 생성 화면에서
> 옵션이 노출되는지 확인하고 켬. TC-DATA-03(Freshness 측정)의 필수 사전조건입니다.

### 사전조건
- Self-Managed 환경에서 Continuous Indexing은 **기본적으로 비활성화** 상태이며, 활성화
  하려면 Cohesity Support에 반드시 사전 문의해야 합니다.

### 테스트 수행 절차 ([00_COMMON_SETUP.md](00_COMMON_SETUP.md) 0.7절과 동일)
1. Cohesity Support에 "Continuous Indexing 활성화"를 요청하고 완료를 확인합니다.
2. `freshness` Dataset(TC-DATA-03/04/05용, 아래 참고)을 생성하는 화면에서 Continuous
   Indexing 옵션이 노출되는지 확인하고 켭니다.

### 예상 결과 / 합격 기준
- 옵션이 정상적으로 노출/적용되고 이후 스냅샷이 자동 반영됨.
- 활성화 여부가 Dataset 설정 화면에서 확인 가능.

### 결과 기록
| 항목 | 결과 |
|---|---|
| Support 활성화 요청 완료일 | |
| Dataset 화면에서 옵션 노출 여부 | PASS/FAIL |

---

## TC-DATA-03 — Continuous Indexing 데이터 최신성(Freshness) `[P1]`

**사전조건**: TC-DATA-02 완료(Continuous Indexing 활성).

> **어디서**: `freshness` Dataset (NAS, Continuous Indexing 활성 — [00_COMMON_SETUP.md](00_COMMON_SETUP.md)
> 0.4 레지스트리 #4). 소스 파일은 이 저장소의 `poc_dataset/TC-DATA-03_05_freshness/` 폴더.
> **어떻게**: 90일짜리 문서를 인덱싱 → 90일 답변 확인 → 소스 파일을 60일짜리로 교체·재백업
> → Last Indexed 갱신 대기 → 재질의해 60일로 바뀌는지, 걸린 시간(Data Freshness)이 얼마인지
> 측정. 아래 "데이터 준비"·"테스트 수행 절차"에 단계별로 상세 기술.

### 데이터 준비 (생성 방법 포함)
- 이 저장소의 `poc_dataset/TC-DATA-03_05_freshness/living_policy_v1_90days.docx` —
  "living source"로 쓰기 위해 신규 합성한 문서(원본 대용량 공시 데이터는 손대지 않음).
  본문에 "현재 스냅샷 보존 기간은 90일입니다"라는 내용이 명시되어 있습니다.
- Dataset: `freshness` (NAS, Continuous Indexing 활성 — 0.4 레지스트리 #4, 0.7절) —
  같은 폴더의 3개 파일 전체를 소스로 등록.

### 테스트 수행 절차
1. `living_policy_v1_90days.docx`를 보호 대상 NAS 소스에 올리고 백업 → `freshness`
   Dataset에 인덱싱.
2. "현재 스냅샷 보존 기간은?" 질의 → **90일** 확인, 질의 시각 기록.
3. 소스 위치의 파일을 `living_policy_v2_60days.docx`(이미 준비됨, 60일로 값 변경) 내용
   으로 교체(파일명 유지하거나, 실제 운영처럼 동일 파일명을 열어 90→60일로 직접 수정해도
   무방).
4. 신규 백업 스냅샷 생성 → Last Indexed 갱신 대기, 갱신 완료 시각 기록.
5. 동일 질문 재질의 → **60일**로 바뀌었는지 확인.
6. 백업 완료~답변 반영까지 걸린 시간(Data Freshness)을 계산.
7. 토픽/워드클라우드는 별도 7일 주기 갱신이므로 이번 측정 대상에서 제외하고 구분해
   기록.

### 예상 결과 / 합격 기준
- 변경된 값(60일)이 답변에 반영됨, 토픽 갱신 주기는 별도임을 확인.
- 백업 완료~답변 반영까지 소요 시간(Data Freshness) 측정 및 SLA 목표 대비 평가.

### 결과 기록
| 항목 | 값 |
|---|---|
| 백업 완료 시각 | |
| Last Indexed 갱신 시각 | |
| 재질의 결과(구값 90일 잔존 여부) | 없음/있음(FAIL) |
| Data Freshness (분) | |

---

## TC-DATA-04 — 원본 데이터 변경 반영 `[P2]`

**전제**: TC-DATA-03와 동일한 `living_policy_v1_90days.docx` → `v2_60days.docx` 교체
절차를 그대로 사용합니다(문서 값: 정책값 90일→60일). Continuous Indexing 없이도(일반
스케줄 백업+재인덱싱으로) 검증 가능하다는 점이 TC-DATA-03과의 차이입니다.

### 테스트 수행 절차
1. `living_policy_v1_90days.docx`가 인덱싱된 상태에서 "현재 스냅샷 보존 기간은?" 질의
   → 90일 확인.
2. 원본 문서 내용을 `living_policy_v2_60days.docx`로 교체.
3. (Continuous Indexing 미사용 시) Dataset을 수동 재인덱싱하거나 다음 정기 인덱싱
   주기를 대기.
4. 동일 질문 재질의 → 최신 값(60일)으로 답변하는지 확인.

### 예상 결과 / 합격 기준
- 이전 값이 아닌 최신 값으로 답변.
- 변경 후 재질의 시 구 값(90일)이 답변에 전혀 남아있지 않음.

### 결과 기록
| 항목 | 결과 |
|---|---|
| 변경 후 재질의 답변 | 60일/90일(FAIL)/기타 |
| 구 값 잔존 여부 | 없음/있음 |

---

## TC-DATA-05 — 원본 데이터 삭제 반영 `[P2]`

### 데이터 준비
- 이 저장소의 `poc_dataset/TC-DATA-03_05_freshness/deletion_candidate_falcon7.docx` —
  삭제 테스트 전용으로 신규 합성한 문서. 본문에 "임시 프로젝트 코드명은 Falcon-7입니다"
  내용 포함. `freshness` Dataset(0.4 레지스트리 #4)의 소스 경로에 이미 다른 2개 파일과
  함께 위치합니다.

### 테스트 수행 절차
1. `deletion_candidate_falcon7.docx`를 `freshness` Dataset 소스에 함께 업로드 후 인덱싱.
2. "임시 프로젝트 코드명은 무엇입니까?" 질의 → **Falcon-7** 확인.
3. 해당 파일을 소스에서 삭제 → 재인덱싱.
4. 동일 질문 재질의 → 더 이상 검색/답변에 노출되지 않는지 확인(무응답 또는 "정보
   없음" 처리가 정상).

### 예상 결과 / 합격 기준
- 삭제된 정보가 더 이상 검색/답변에 노출되지 않음.
- 삭제 후 재질의 시 해당 정보 미노출 100%.

### 결과 기록
| 항목 | 결과 |
|---|---|
| 삭제 전 질의 결과 | Falcon-7 확인/불가 |
| 삭제 후 재질의 결과 | 미노출(PASS)/노출(FAIL) |

---

## TC-DATA-06 — Dataset 규모별 성능/품질 비교 `[P2]`

### 데이터 준비 (복사 없이 원본 경로 직접 참조)

| 티어 | 구성 | 실측 크기 | 회사 수 | 회사 목록 |
|---|---|---|---|---|
| 1GB | `$GAIA_DATASET_DIR` 중 가장 작은 37개사 | 1.02GB | 37 | [00_COMMON_SETUP.md](00_COMMON_SETUP.md) 0.5절 "1GB 티어" |
| 10GB | `$GAIA_DATASET_DIR` 중 작은 130개사 | 10.00GB | 130 | [00_COMMON_SETUP.md](00_COMMON_SETUP.md) 0.5절 "10GB 티어" |
| 100GB | `$GAIA_DATASET_DIR` 전체 | 109.94GB | 275 | 전체(목록 불필요) |
| 200GB(근사) | `$GAIA_DATASET_DIR` 전체 + `$GAIA_WEB_DATASET_DIR` 전체 | ≈170GB | — | 전체(목록 불필요) |

1GB/10GB 티어의 회사 폴더명은 `$GAIA_DATASET_DIR/<회사명>/` 경로와 그대로 매칭됩니다
(0.5절 목록을 그대로 Protection Group의 "포함 경로" 목록으로 사용).

### 테스트 수행 절차
1. [00_COMMON_SETUP.md](00_COMMON_SETUP.md) 0.4 레지스트리 #6~9(`perf-1gb`, `perf-10gb`,
   `perf-100gb`, `perf-200gb`)를 0.2/0.3절 절차대로 순서대로 등록(동시에 4개를 유지할
   필요는 없음).
2. 각 Dataset의 Indexing 시작~완료(`Succeeded`) 소요 시간을 기록.
3. [QA_perf_common.md](QA_perf_common.md)의 50개 질문(4개 티어 모두에 근거 문서가
   포함되어 있음) 중 10~15개를 골라 각 규모의 Dataset에 동일하게 질의해 응답 지연
   (Latency)과 검색 품질(정답이 나오는지, 관련 문서가 Citation 상위에 나오는지)을 비교.

### 예상 결과 / 합격 기준
- Dataset이 커질수록 Indexing 시간 증가, 검색 품질은 일정 수준 이상 유지.
- 가장 큰 Dataset(100GB/200GB)에서도 관련 문서 검색 누락이 두드러지지 않음(정성 판단,
  목표치 참고용 "관련 문서 상위 노출 비율 0.7 이상").

### 결과 기록
| 티어 | Indexing 소요 시간 | 응답 지연(체감) | 검색 품질(정성) |
|---|---|---|---|
| 1GB / 10GB / 100GB / 200GB | | | |

---

## TC-DATA-07 — 손상/암호화/빈 파일 인덱싱 장애 처리 `[P2]`

### 데이터 준비 (이 저장소의 `poc_dataset/TC-DATA-07_corrupt_files/` 폴더, 전부 이미 생성됨)

| 파일 | 목적 | 비고 |
|---|---|---|
| `normal.pdf` | 정상 파일 대조군 | TC-DATA-01 fixture와 동일 내용 |
| `encrypted_password_poc-test-1234.pdf` | 암호화 PDF | 사용자 비밀번호: `poc-test-1234` |
| `corrupted.pdf` | 손상된 PDF | 정상 PDF를 1/3 지점에서 절단해 구조 파괴 |
| `empty_0byte.pdf` | 빈 파일 | 0바이트 |
| `unsupported_extension.xyz` | 미지원 확장자 | 공식 지원 목록에 없는 확장자 |

### 테스트 수행 절차
1. 위 5개 파일을 NAS 소스로 백업 → `corrupt-files` Dataset 생성(0.4 레지스트리 #3, 다른
   Dataset과 반드시 분리 — Index Status가 의도적으로 Warning이 되므로 정상 Dataset
   판정과 섞이지 않게 함).
2. Indexing 완료 후 Index Status와 실패 문서 목록/사유를 확인.
3. `normal.pdf` 내용에 대해 정상 질의([QA_small_fixtures.md](QA_small_fixtures.md)의
   `corrupt-files` 4개 질문 재사용)해 다른 파일 실패가 정상 파일 인덱싱/질의에 영향을
   주지 않는지 확인.

### 예상 결과 / 합격 기준
- `normal.pdf`만 정상 인덱싱되고 나머지 4개는 실패 처리.
- Index Status가 **Warning**으로 표시되고, 실패 문서 수(4개)와 사유가 UI에 명확히 노출.
- 정상 파일의 인덱싱·질의응답은 다른 파일 실패에 영향받지 않음.

### 결과 기록
| 파일 | 처리 결과 | 실패 사유(UI 표시) |
|---|---|---|
| normal.pdf | 성공/실패 | |
| encrypted_*.pdf | 성공/실패 | |
| corrupted.pdf | 성공/실패 | |
| empty_0byte.pdf | 성공/실패 | |
| unsupported_extension.xyz | 성공/실패 | |

| Index Status | 실패 문서 수(표시값) | normal.pdf 질의 정상 여부 |
|---|---|---|
| | | PASS/FAIL |
