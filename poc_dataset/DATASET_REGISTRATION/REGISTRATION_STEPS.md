# Gaia Dataset 등록 — Helios UI 단계별 절차

[`README.md`](README.md)가 "**무엇을** 몇 개, 어떤 경로로 등록할지"를 정리한 계획이라면,
이 문서는 "**어떻게**(Helios UI에서 어떤 순서로 클릭하는지)"를 정리한 실행 절차입니다.

> **출처 표기 원칙**: 아래에서 `cohesity_gaia_poc_testcases.md` 원문을 그대로 인용한 부분과,
> Cohesity 제품의 일반적인 개념(정확한 메뉴명은 버전마다 다를 수 있음)을 설명한 부분을
> 구분해 표시했습니다. 후자는 실제 화면과 다르면 Cohesity SE/Support에 확인하세요
> (`cohesity_gaia_api_developer_guide_v1.2.md` 5.3절이 API Base URL에 대해 취하는 것과
> 같은 태도입니다 — 이 저장소는 특정 버전의 UI를 검증할 방법이 없습니다).

## 0. 전체 흐름

```
NAS/M365 소스를 Cohesity로 백업 (Protection Group)         ← 1절, Gaia 고유 기능 아님
        │
        ▼
Helios(Self-Managed) 로그인
        │
        ▼
Insights > Data Insights > Create Dataset                  ← 2절, TC-FUNC-01 원문
        │
        ├── Dataset 이름 입력
        ├── Object Type 선택 (NAS / M365 Mailbox / M365 OneDrive)
        ├── 백업된 소스 중 포함할 경로/계정 체크
        ├── Authorized Users 지정                          ← RBAC 테스트의 핵심
        └── Create 클릭
        │
        ▼
Index Status: Running → Succeeded 대기
```

(출처: `../../cohesity_gaia_poc_testcases.md` TC-FUNC-01 수행절차 — "Helios(Self-Managed) >
Insights > Data Insights > Create Dataset에서 데이터 소스 선택 → Authorized Users 지정 →
Create 클릭", `../../../gaia_eval/cohesity_gaia_api_developer_guide_v1.2.md` 3.2절 "데이터
소스 준비" 4단계와 동일한 흐름)

## 1. NAS 소스를 Cohesity에 등록/백업하기 (Dataset 생성 전 필수 선행 작업)

Gaia Dataset은 **이미 Cohesity로 백업된(보호된) 데이터**에서만 만들 수 있습니다
(TC-FUNC-01 사전조건: "보호(backup)된 데이터 소스 최소 1개 존재"). 이 백업 자체는 Gaia
기능이 아니라 Cohesity DataProtect의 표준 절차라, 이 저장소 문서들에는 상세 화면이
나오지 않습니다 — 아래는 일반적인 개념입니다:

1. Helios(Self-Managed) 로그인
2. **Protection > Sources**(또는 이와 동등한 메뉴)에서 NAS 소스(파일 서버/공유)를 새로
   등록 — 호스트/IP, 접근 자격증명 입력
3. 등록한 NAS 소스 아래에서 Dataset에 포함시킬 경로를 선택해 **Protection Group**(백업
   정책) 생성 (경로는 3절 표의 "포함 경로" 열 사용)
4. Protection Group 실행(Run) → 백업 스냅샷이 최소 1회 성공할 때까지 대기 — 성공해야
   Data Insights에 "보호된 데이터 소스"로 노출됩니다
5. M365 Mailbox/OneDrive(Dataset 3~4번)는 NAS가 아니라 M365 테넌트 연동이 필요합니다
   (별도 사전 작업, `README.md` 3~4번 항목 참고)

## 2. Gaia Dataset 생성 (10개 공통 절차)

TC-FUNC-01 수행절차 원문을 단계별로 풀면:

1. Helios(Self-Managed) > **Insights > Data Insights** 이동
2. **Create Dataset** 클릭
3. Dataset 이름 입력 — 3절 표의 "Dataset 이름"을 그대로 사용하세요 (나중에 TC 결과
   리포트·CSV에서 어떤 Dataset인지 바로 구분하기 위함)
4. **Object Type** 선택 — 대부분 NAS(1번 항목 참고), Mailbox/OneDrive Dataset(3~4번)만
   해당 M365 Object Type 선택
5. 1절에서 백업해 둔 소스 중 이 Dataset에 포함할 경로/계정을 체크
6. **Authorized Users** 필드에 3절 표의 사용자를 정확히 지정 — **여기서 잘못 지정하면
   TC-RBAC-04/05/06, TC-SEC-05가 전부 무의미해집니다** (Dataset A/B 격리가 테스트의
   전제조건이므로)
7. TC-DATA-02/03 대상 Dataset(Freshness)이면 이 화면에서 **Continuous Indexing** 옵션도
   함께 확인/적용 (4절 참고)
8. **Create** 클릭
9. Index Status가 `Running` → `Succeeded`로 바뀔 때까지 대기 (대용량 티어는 수 시간
   소요될 수 있음 — TC-PERF-03이 바로 이 소요 시간 자체를 측정하는 테스트입니다)

## 3. Dataset별 구체적 값

`README.md` 요약 표와 동일한 10개(+선택 1개)를 실제 입력값 기준으로 정리했습니다.

| # | Dataset 이름 | Object Type | 포함 경로 | Authorized Users | 비고 |
|---|---|---|---|---|---|
| 1 | `finance-core` | NAS | `finance_core_companies.txt`의 4개 경로 (`$GAIA_DATASET_DIR/003230_삼양식품` 등) | User A만 | 이후 `../TC-SEC/injection_docs/` 3개 문서 추가 인덱싱 (TC-SEC-03/04) |
| 2 | `hr-synthetic` | NAS | `../TC-RBAC/dataset_hr_synthetic/` | User C 등 (**User A 제외**) | User A 미지정이 TC-RBAC-05/06 차단 판정의 기준 |
| 3 | `mailbox-poc` | M365 Mailbox | 백업된 M365 테넌트 Mailbox 계정 | 임의 | TC-DATA-08: 파일/디렉터리 단위 include-exclude 미노출 확인 |
| 4 | `onedrive-poc` | M365 OneDrive | 백업된 M365 테넌트 OneDrive 계정 | 임의 | TC-DATA-08: 경로 단위 include-exclude 가능 여부 확인 |
| 5 | `perf-1gb` | NAS | `../PERF/tier_1gb_companies.txt`의 37개 경로 | 임의 | |
| 6 | `perf-10gb` | NAS | `../PERF/tier_10gb_companies.txt`의 130개 경로 | 임의 | |
| 7 | `perf-100gb` | NAS | `$GAIA_DATASET_DIR` 전체(275개사) | 임의 | TC-PERF-07 시점엔 Finance-Core와 **동시에** 등록되어 있어야 함 |
| 8 | `perf-200gb` | NAS(2개 소스) | `$GAIA_DATASET_DIR` 전체 + `$GAIA_WEB_DATASET_DIR` 전체 | 임의 | 7번 소스에 `$GAIA_WEB_DATASET_DIR` NAS 소스만 추가하면 됨(새로 안 만들어도 됨) |
| 9 | `corrupt-files` | NAS | `../TC-DATA-07_corrupt_files/` 5개 파일 | 임의 | Index Status가 의도적으로 Warning — 다른 Dataset과 분리 필수 |
| 10 | `freshness` | NAS | `../TC-DATA-03_05_freshness/` 3개 파일 | 임의 | 4절의 Continuous Indexing 활성화 먼저 필요 |
| 11(선택) | `format-fixture` | NAS | `../TC-DATA-01_format_coverage/content.*` 8개 파일 | 임의 | Finance-Core에 얹어도 무방 (`README.md` 참고) |

"임의"로 표시한 항목은 RBAC 격리 테스트 대상이 아니라 어떤 사용자를 지정해도 무방하다는
뜻입니다(단, 로그인 가능한 유효 사용자 1명은 지정해야 함).

## 4. Continuous Indexing 활성화 (Freshness Dataset 전용, TC-DATA-02)

1. Cohesity Support에 "Continuous Indexing 활성화" 요청 — Self-Managed는 **기본 비활성
   상태**입니다(`cohesity_gaia_poc_testcases.md` 상단 "사전 정정 및 확인 사항" 2번).
   TC-DATA-03도 이 활성화가 끝나야 진행 가능
2. 활성화 확인 후 `freshness` Dataset을 만들 때(2절 6번 단계) Continuous Indexing 옵션이
   화면에 노출되는지 확인하고 켬 — 이 노출 여부 확인 자체가 TC-DATA-02의 합격 기준
   ("활성화 여부가 Dataset 설정 화면에서 확인 가능")

## 5. Authorized User 변경 / AD 그룹 연동 (TC-RBAC-07/08)

- **TC-RBAC-07 (권한 제거)**: Data Insights에서 `finance-core` Dataset 선택 → 편집 →
  Authorized Users에서 User A 제거 → 저장. 이후 User A가 재로그인한 뒤 접근이 차단되는지,
  제거~차단까지 걸린 시간을 측정
- **TC-RBAC-08 (AD 그룹)**: SSO/AD 연동이 사전에 구성되어 있어야 합니다(사전조건). Authorized
  Users 필드에 개별 사용자 대신 AD 그룹을 지정하고, 그룹 소속/비소속 사용자로 각각
  접근을 시도해 상속이 정확한지 확인
