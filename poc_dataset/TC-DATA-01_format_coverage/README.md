# TC-DATA-01 — 지원 파일 포맷별 인덱싱/답변 정확도

## 1. 동일 내용 fixture (엄격 비교용)
이 폴더의 `content.*` 8개 파일은 **완전히 동일한 내용**(데이터 보존정책 안내, 표 3행 포함)을
아래 포맷으로 각각 준비한 것입니다. Dataset에 8개 파일을 모두 포함시키고, 동일 질문을
포맷별로 질의해 정답률/Citation을 비교합니다.

| 파일 | 포맷 |
|---|---|
| content.docx | Word |
| content.xlsx | Excel |
| content.pptx | PowerPoint |
| content.pdf | PDF |
| content.rtf | RTF |
| content.txt | 텍스트 |
| content.html | HTML |
| content.xml | XML |

### 검증용 질문 (합격기준: 8개 포맷 모두 동일 답변)
1. "현재 스냅샷 보존 기간은 며칠입니까?" → **90일**
2. "로그 보존 기간과 담당 부서는?" → **30일, 보안팀**
3. "이 정책의 개정일은 언제입니까?" → **2026-08-01**
4. "아카이브 보존 기간은?" → **365일**

## 2. 대규모 포맷별 커버리지 (참고용, 기존 산출물에서 샘플링)
collector/eval 파이프라인이 gaia_web_dataset 기반으로 생성해 둔 포맷 그룹별 QA
200개씩에서 포맷당 25개씩 샘플링해(고정 시드) 이 폴더에 복사했습니다. 원본 문서는
수정하지 않았고, `file_path` 필드는 **`$GAIA_WEB_DATASET_DIR`(기본값은
`../paths_config.py` 참고) 기준 상대경로**입니다 — 실제 파일을 열려면
`os.path.join(GAIA_WEB_DATASET_DIR, file_path)`처럼 결합해야 합니다(다른 머신으로
옮겨 `GAIA_WEB_DATASET_DIR`을 오버라이드해도 그대로 작동):

- `qa_pairs_pdf.json` (25개, PDF)
- `qa_pairs_docx_doc.json` (25개, docx/doc/odf/rtf)
- `qa_pairs_xlsx_xls_csv.json` (25개, xlsx/xls/csv)
- `qa_pairs_ppt_pptx.json` (25개, ppt/pptx)

이 세트는 포맷 간 내용이 서로 다르므로(정제 X, 정확도 절대비교용 아님) "포맷 자체의
파싱 실패 여부" 확인 용도로 쓰고, 엄격한 동일 내용 비교는 위 1번 fixture로 하는 것을
권장합니다.
