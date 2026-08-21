# 0. 공통 준비 사항 (환경 / Dataset 생성 절차 / Dataset 레지스트리)

`docs/` 아래 문서(00~06번 절차 문서 + `QA_*.md` 5개)만으로 테스트를 처음부터 끝까지
수행할 수 있도록, 반복적으로 쓰이는 환경 변수, NAS 백업 절차, Gaia Dataset 생성 공통
절차, 이 세트가 사용하는 전체 Dataset 목록과 계정을 이 문서 하나에 모았습니다. 01~06번
문서는 이 문서의 절차·표를 번호로만 인용하며, 그 외 이 저장소의 다른 위치(`poc_dataset/`의
각 README, 루트의 `cohesity_gaia_poc_testcases.md`/`EXECUTION_ORDER.md`/`migration.md` 등)는
열어볼 필요가 없습니다. 단, 합성 문서(docx/xlsx/pdf 등)처럼 실제로 업로드해야 하는
**데이터 파일 자체**는 이 저장소의 `poc_dataset/` 아래에 이미 만들어져 있으므로, 각 TC
절차에 그 파일 경로만 "업로드 대상"으로 직접 명시합니다(그 경로의 `.md` 설명 문서를 열어볼
필요는 없습니다).

## 0.1 환경 변수 / 원본 데이터 경로

| 변수 | 기본값 | 용도 |
|---|---|---|
| `GAIA_DATASET_DIR` | `/data/richard/data/gaia_dataset` | DART 공시 문서 원본(약 103GB, 275개사). TC-FUNC/RBAC/SEC/PERF-01/02와 TC-DATA-06의 100GB/200GB 티어가 이 경로를 그대로 참조합니다. |
| `GAIA_WEB_DATASET_DIR` | `/data/richard/data/gaia_web_dataset` | 웹 수집 문서 원본(약 60GB). TC-DATA-01의 대규모 포맷 커버리지 샘플과 TC-DATA-06의 200GB 티어가 참조합니다. |

다른 머신에서 실행할 경우 위 두 값을 동일 이름의 환경 변수로 오버라이드하면 됩니다(원본
데이터 위치만 바뀌었을 뿐 절차는 동일).

## 0.2 NAS 소스를 Cohesity에 등록/백업하기 (모든 Dataset 생성의 선행 작업)

Gaia Dataset은 **이미 Cohesity로 백업된(보호된) 데이터**에서만 만들 수 있습니다. 아래는
Dataset 생성 전 반드시 먼저 수행해야 하는 NAS 백업 절차입니다(Gaia 고유 기능이 아니라
Cohesity DataProtect의 표준 절차):

1. Helios(Self-Managed)에 로그인합니다.
2. **Protection > Sources**(또는 동등 메뉴)에서 대상 NAS 소스(파일 서버/공유)를 새로
   등록합니다 — 호스트/IP, 접근 자격증명을 입력합니다.
3. 등록한 NAS 소스 아래에서 이 문서 세트가 요구하는 경로(아래 0.4 표의 "포함 경로" 열)를
   선택해 **Protection Group**(백업 정책)을 생성합니다.
4. Protection Group을 실행(Run)하고, 백업 스냅샷이 최소 1회 성공할 때까지 대기합니다 —
   성공해야 Data Insights 화면에 "보호된 데이터 소스"로 노출됩니다.

## 0.3 Gaia Dataset 생성 공통 절차 (Helios UI)

아래 9단계는 이 문서 세트의 모든 Dataset 생성에 동일하게 적용됩니다. 각 TC 문서에서는
"0.3 공통 절차대로, 아래 표의 값을 입력해 생성" 식으로 이 절차를 그대로 재사용합니다.

1. Helios(Self-Managed) > **Insights > Data Insights**로 이동합니다.
2. **Create Dataset**을 클릭합니다.
3. Dataset 이름을 입력합니다(0.4 표의 "Dataset 이름" 열 값을 그대로 사용 — 이후 결과표에서
   어떤 Dataset인지 바로 구분하기 위함).
4. **Object Type**을 `NAS`로 선택합니다 — 이 문서 세트는 전부 NAS 소스만 사용합니다.
5. 0.2에서 백업해 둔 소스 중 이 Dataset에 포함할 경로를 체크합니다(0.4 표의 "포함 경로" 열).
6. **Authorized Users** 필드에 0.4 표의 "Authorized User" 열 값을 정확히 지정합니다 —
   여기서 잘못 지정하면 RBAC/SEC 격리 테스트가 전부 무의미해지므로 반드시 재확인합니다.
7. `freshness` Dataset(0.4의 #4)을 만드는 경우, 이 화면에서 **Continuous Indexing** 옵션도
   함께 확인하고 켭니다(0.7절을 먼저 완료해야 옵션이 노출됩니다).
8. **Create**를 클릭합니다.
9. Index Status가 `Running` → `Succeeded`로 바뀔 때까지 대기합니다(대용량 티어는 수 시간
   소요될 수 있음 — 이 소요 시간 자체를 측정하는 것이 TC-PERF-03입니다).

## 0.4 이 문서 세트에서 사용하는 Dataset 레지스트리

| # | Dataset 이름 | 포함 경로 | 크기(대략) | Authorized User | 사용 TC | QA 세트 |
|---|---|---|---|---|---|---|
| 1 | `finance-core` | `$GAIA_DATASET_DIR/003230_삼양식품/`, `$GAIA_DATASET_DIR/005380_현대자동차/`, `$GAIA_DATASET_DIR/005930_삼성전자/`, `$GAIA_DATASET_DIR/030610_교보증권/` (4개사) | 6.5GB | User A만 | FUNC-01,03~07 / RBAC 전체 / SEC-01,03,04,05 / PERF-01,02,05,07 | [QA_finance_core.md](QA_finance_core.md) (50개) |
| 2 | `hr-synthetic` | 이 저장소의 `poc_dataset/TC-RBAC/dataset_hr_synthetic/` 폴더 전체(`hr_evaluation_2026h1.docx`, `salary_bands_2026.xlsx` 2개 파일) | 수십 KB | User C만 (**User A 미지정**) | RBAC-06 / SEC-04,05 | [QA_hr_synthetic.md](QA_hr_synthetic.md) (25개, 원본 분량 한계) |
| 3 | `corrupt-files` | 이 저장소의 `poc_dataset/TC-DATA-07_corrupt_files/` 폴더 전체(5개 파일 — 내용은 03_DATA.md TC-DATA-07에 직접 명시) | <1MB | 임의(로그인 가능한 유효 사용자 1명) | DATA-07 | [QA_small_fixtures.md](QA_small_fixtures.md) (4개, 원본 분량 한계) |
| 4 | `freshness` | 이 저장소의 `poc_dataset/TC-DATA-03_05_freshness/` 폴더 전체(3개 파일 — 내용은 03_DATA.md TC-DATA-03/04/05에 직접 명시), **Continuous Indexing 활성 필요**(0.7절) | <1MB | 임의 | DATA-02,03,04,05 | [QA_small_fixtures.md](QA_small_fixtures.md) (4개, 원본 분량 한계) |
| 5 | `format-fixture` | 이 저장소의 `poc_dataset/TC-DATA-01_format_coverage/`의 `content.docx/.xlsx/.pptx/.pdf/.rtf/.txt/.html/.xml` 8개 파일(내용은 03_DATA.md TC-DATA-01에 직접 명시) | <1MB | 임의 | DATA-01 | [QA_format_fixture.md](QA_format_fixture.md) (4개 기본 + 선택 100개) |
| 6 | `perf-1gb` | `$GAIA_DATASET_DIR/<회사명>/` — 0.5절 "1GB 티어" 목록 37개사 | 1.02GB | 임의 | DATA-06 | [QA_perf_common.md](QA_perf_common.md) (50개, 6~9번 Dataset 공통) |
| 7 | `perf-10gb` | `$GAIA_DATASET_DIR/<회사명>/` — 0.5절 "10GB 티어" 목록 130개사 | 10.00GB | 임의 | DATA-06 | [QA_perf_common.md](QA_perf_common.md) (동일) |
| 8 | `perf-100gb` | `$GAIA_DATASET_DIR` 전체(275개사) | 109.94GB | 임의 | DATA-06 / PERF-03,07 | [QA_perf_common.md](QA_perf_common.md) (동일) |
| 9 | `perf-200gb` | `$GAIA_DATASET_DIR` 전체 + `$GAIA_WEB_DATASET_DIR` 전체(NAS 소스 2개를 하나의 Dataset에 포함) | ≈170GB | 임의 | DATA-06 / PERF-03,07 | [QA_perf_common.md](QA_perf_common.md) (동일) |

## 0.4-1 QA 세트 요약

Dataset마다 실제 질문-정답-근거를 담은 QA 문서를 준비했습니다(전부 `docs/` 안에 있으며,
finance-core/perf-common은 4개사/9개사의 실제 DART 공시 PDF 표지에서 직접 추출한 사실
기반, hr-synthetic/freshness/corrupt-files는 원본 합성 문서 분량이 작아 존재하는 사실만
정리했습니다).

| Dataset | QA 문서 | 개수 |
|---|---|---|
| `finance-core` | [QA_finance_core.md](QA_finance_core.md) | 50 |
| `perf-1gb`/`perf-10gb`/`perf-100gb`/`perf-200gb` (공통) | [QA_perf_common.md](QA_perf_common.md) | 50 |
| `hr-synthetic` | [QA_hr_synthetic.md](QA_hr_synthetic.md) | 25 |
| `freshness` + `corrupt-files` | [QA_small_fixtures.md](QA_small_fixtures.md) | 4 + 4 = 8 |
| `format-fixture` | [QA_format_fixture.md](QA_format_fixture.md) | 4 (+선택 100) |

"임의"로 표시한 항목은 RBAC 격리 테스트 대상이 아니므로 어떤 사용자를 지정해도 무방하다는
뜻입니다(단, 로그인 가능한 유효 사용자 1명은 반드시 지정).

`format-fixture`(#5)는 별도로 만들지 않고 `finance-core`(#1)에 8개 파일을 얹어도 무방합니다
(내용이 작고 "동일 질문 → 동일 답변" 비교만 하면 되므로 다른 Dataset과 섞여도 문제없음).
분리하는 이유는 순수하게 "포맷 자체만 다른, 완전히 통제된 비교군"을 유지하기 위함입니다.

`perf-100gb`~`perf-200gb`(#8~9)는 TC-PERF-07 시점에는 `finance-core`(#1)와 **동시에**
등록되어 있어야 합니다(대용량 Dataset이 인덱싱되는 동안 기존 Dataset에 질의하는 시나리오).
4개 Perf 티어(#6~9)를 항상 동시에 유지할 필요는 없고, 필요한 티어만 그때그때 등록해도
됩니다.

## 0.5 Perf 티어별 회사 목록

`perf-1gb`/`perf-10gb`에 포함할 회사 폴더명입니다. 각 이름은 `$GAIA_DATASET_DIR/<이름>/`
경로와 그대로 매칭됩니다(예: `348950_제이알글로벌리츠` → `$GAIA_DATASET_DIR/348950_제이알글로벌리츠/`).
아래 목록을 그대로 Protection Group의 "포함 경로" 목록으로 사용하면 됩니다. **일부 회사명에
공백이 포함되어 있으므로**(`007700_F&F 홀딩스`, `079160_CJ CGV`) 한 줄에 한 회사명만
배치했습니다 — 경로를 옮겨 적을 때 줄 단위로 그대로 복사하면 됩니다.

### 1GB 티어 (37개사, 실측 1.02GB)

```
348950_제이알글로벌리츠
363280_티와이홀딩스
088980_맥쿼리인프라
271980_제일약품
284740_쿠쿠홈시스
271940_일진하이솔루스
178920_PI첨단소재
005690_파미셀
241590_화승엔터프라이즈
033270_유나이티드
330590_롯데리츠
294870_IPARK현대산업개발
192080_더블유게임즈
013890_지누스
248070_솔루엠
003520_영진약품
001570_금양
006110_삼아알미늄
108320_LX세미콘
004490_세방전지
003850_보령
322000_HD현대에너지솔루션
006650_대한유화
298050_HS효성첨단소재
007700_F&F 홀딩스
006740_블루산업개발
214320_이노션
007570_일양약품
077970_STX엔진
032350_롯데관광개발
353200_대덕전자
003000_부광약품
005420_코스모화학
003620_KG모빌리티
011000_진원생명과학
336370_솔루스첨단소재
280360_롯데웰푸드
```

### 10GB 티어 (130개사, 실측 10.00GB)

1GB 티어 37개사를 포함해 아래 130개사 전체입니다.

```
348950_제이알글로벌리츠
363280_티와이홀딩스
088980_맥쿼리인프라
271980_제일약품
284740_쿠쿠홈시스
271940_일진하이솔루스
178920_PI첨단소재
005690_파미셀
241590_화승엔터프라이즈
033270_유나이티드
330590_롯데리츠
294870_IPARK현대산업개발
192080_더블유게임즈
013890_지누스
248070_솔루엠
003520_영진약품
001570_금양
006110_삼아알미늄
108320_LX세미콘
004490_세방전지
003850_보령
322000_HD현대에너지솔루션
006650_대한유화
298050_HS효성첨단소재
007700_F&F 홀딩스
006740_블루산업개발
214320_이노션
007570_일양약품
077970_STX엔진
032350_롯데관광개발
353200_대덕전자
003000_부광약품
005420_코스모화학
003620_KG모빌리티
011000_진원생명과학
336370_솔루스첨단소재
280360_롯데웰푸드
145720_덴티움
137310_에스디바이오센서
114090_GKL
009900_명신산업
279570_케이뱅크
001230_동국홀딩스
022100_포스코DX
057050_현대홈쇼핑
001680_대상
016380_KG스틸
003570_SNT다이내믹스
089590_제주항공
450080_에코프로머티
457190_이수스페셜티케미컬
007810_코리아써키트
020560_아시아나항공
181710_NHN
079160_CJ CGV
093370_후성
100090_SK오션플랜트
069260_티케이지휴켐스
210980_SK디앤디
000060_메리츠화재해상보험
475150_SK이터닉스
006120_SK디스커버리
031430_신세계인터내셔날
071970_HD현대마린엔진
003240_태광산업
017960_한국카본
004000_롯데정밀화학
009970_영원무역홀딩스
229640_LS에코에너지
003090_대웅
089860_롯데렌탈
019170_신풍제약
082740_한화엔진
001800_오리온홀딩스
462870_시프트업
097230_HJ중공업
014820_동원시스템즈
185750_종근당
489790_한화비전
073240_금호타이어
005850_에스엘
001430_세아베스틸지주
010780_아이에스동서
009240_한샘
005070_코스모신소재
031210_서울보증보험
192820_코스맥스
383220_F&F
103590_일진전기
361610_SK아이이테크놀로지
007340_DN오토모티브
007310_오뚜기
483650_달바글로벌
005250_녹십자홀딩스
439260_대한조선
302440_SK바이오사이언스
323410_카카오뱅크
282330_BGF리테일
336260_두산퓨얼셀
064400_LG씨엔에스
026960_동서
271560_오리온
042670_에이치디현대인프라코어
000670_영풍
005300_롯데칠성음료
052690_한전기술
042700_한미반도체
003230_삼양식품
001740_SK네트웍스
004370_농심
111770_영원무역
009420_한올바이오파마
326030_에스케이바이오팜
036570_NC
062040_산일전기
278470_에이피알
443060_HD현대마린솔루션
010620_에이치디현대미포
285130_SK케미칼
128940_한미약품
003410_쌍용씨앤이
161890_한국콜마
000500_가온전선
298040_효성중공업
307950_현대오토에버
377300_카카오페이
402340_SK스퀘어
006280_녹십자
020150_롯데에너지머티리얼즈
051600_한전KPS
```

## 0.6 테스트 계정

| 계정 | 역할/권한 | 접근 가능 Dataset |
|---|---|---|
| User A | 일반 사용자 | `finance-core`만 |
| User B | 일반 사용자 | 없음(어떤 Dataset의 Authorized User에도 미지정 — 차단 확인용) |
| User C | 일반 사용자 | `hr-synthetic`만 |
| Admin 계정 | Gaia Admin 역할('Manage Gaia' privilege 포함) | 전체 |
| Viewer 계정 | Gaia Viewer 역할만 | 대화(질의응답)만 가능, 생성/삭제/복구 불가 |
| Custom Role 계정 | Gaia Viewer + Operator 조합 Custom Role | 대화 + 복구(Recovery) 가능 |
| (선택) AD 그룹 소속/비소속 계정 각 1개 | SSO/AD 연동, AD 그룹 존재 필요 | TC-RBAC-08 전용 |

## 0.7 Continuous Indexing 활성화 (`freshness` Dataset 전용, TC-DATA-02)

1. Self-Managed 환경에서 Continuous Indexing은 **기본적으로 비활성화** 상태입니다. Cohesity
   Support에 "Continuous Indexing 활성화"를 요청하고, 완료될 때까지 대기합니다.
2. 활성화 확인 후, `freshness` Dataset을 생성하는 화면(0.3의 7단계)에서 Continuous
   Indexing 옵션이 노출되는지 확인하고 켭니다 — **이 노출 여부 확인 자체가 TC-DATA-02의
   합격 기준**입니다.

## 0.8 Authorized User 변경 / AD 그룹 연동 절차 (TC-RBAC-07/08에서 사용)

- **권한 제거(TC-RBAC-07)**: Data Insights에서 대상 Dataset(`finance-core`) 선택 → 편집 →
  Authorized Users에서 대상 사용자(User A) 제거 → 저장. 이후 해당 사용자가 재로그인한 뒤
  접근이 차단되는지, 제거~차단까지 걸린 시간을 측정합니다.
- **AD 그룹 지정(TC-RBAC-08)**: SSO/AD 연동이 사전에 구성되어 있어야 합니다. Authorized
  Users 필드에 개별 사용자 대신 AD 그룹을 지정하고, 그룹 소속/비소속 사용자로 각각 접근을
  시도해 상속이 정확한지 확인합니다.

## 0.9 범위 제외 안내

이 문서 세트는 NAS 외 다른 Object Type 소스가 필요한 테스트와 RAG 품질(RAGAS/골든셋
기반) 테스트를 전부 제외합니다(사용자 요청 및 API 미제공). 따라서 위 Dataset 레지스트리
(0.4)의 모든 Dataset은 Object Type이 `NAS`입니다. 제외 범위의 상세 사유는
[`README.md`](README.md)를 참고하세요(같은 `docs/` 폴더 내 문서입니다).
