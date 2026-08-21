# QA — 소규모 픽스처 데이터셋 (freshness / corrupt-files)

`freshness`(0.4 레지스트리 #4)와 `corrupt-files`(0.4 레지스트리 #3)는 원래 목적 자체가
"1~2개 사실만 담은 최소 문서로 인덱싱/최신성/장애 처리를 확인"하는 것이라, 문서에 실제로
있는 사실이 각각 4개뿐입니다(합계 8개). 요청하신 50개에는 크게 못 미치지만, 존재하지 않는
사실을 지어내지 않기 위해 있는 만큼만 정리했습니다(사용자 확인 완료 사항). `format-fixture`
(TC-DATA-01)는 이미 자체 QA가 있어 이 문서에서 다루지 않습니다.

## `freshness` — 4개 (03_DATA.md TC-DATA-03/04/05에서 이미 사용 중인 것과 동일)

**1. (교체 전, `living_policy_v1_90days.docx`) 현재 스냅샷 보존 기간은 며칠입니까?**
- 정답: 90일
- 근거: `living_policy_v1_90days.docx` 본문 — "현재 스냅샷 보존 기간은 90일입니다"

**2. (교체 후, `living_policy_v2_60days.docx`) 현재 스냅샷 보존 기간은 며칠입니까?**
- 정답: 60일 (2026-08-15부로 90일에서 60일로 변경)
- 근거: `living_policy_v2_60days.docx` 본문 — "현재 스냅샷 보존 기간은 60일입니다.
  (2026-08-15부로 90일에서 60일로 변경)"

**3. (`deletion_candidate_falcon7.docx`) 임시 프로젝트 코드명은 무엇입니까?**
- 정답: Falcon-7
- 근거: `deletion_candidate_falcon7.docx` 본문 — "임시 프로젝트 코드명은 Falcon-7 입니다"

**4. (`deletion_candidate_falcon7.docx`) 프로젝트 예산은 얼마입니까?**
- 정답: 4억 2천만원
- 근거: `deletion_candidate_falcon7.docx` 본문 — "프로젝트 예산은 4억 2천만원입니다"

## `corrupt-files` — 4개 (정상 파일 `normal.pdf` 기준, TC-DATA-01 fixture와 동일 내용)

`normal.pdf` 외 나머지 4개 파일(암호화/손상/빈 파일/미지원 확장자)은 정상적으로 인덱싱되지
않도록 의도된 파일이라 추출 가능한 내용이 없습니다. `normal.pdf`는 `TC-DATA-01_format_coverage/content.pdf`와 동일 내용이므로 아래 4개 질문은 03_DATA.md TC-DATA-01의 4개 질문과 같습니다.

**1. 현재 스냅샷 보존 기간은 며칠입니까?**
- 정답: 90일
- 근거: `normal.pdf` 본문 표

**2. 로그 보존 기간과 담당 부서는?**
- 정답: 30일, 보안팀
- 근거: `normal.pdf` 본문 표

**3. 이 정책의 개정일은 언제입니까?**
- 정답: 2026-08-01
- 근거: `normal.pdf` 본문 상단

**4. 아카이브 보존 기간은?**
- 정답: 365일
- 근거: `normal.pdf` 본문 표
