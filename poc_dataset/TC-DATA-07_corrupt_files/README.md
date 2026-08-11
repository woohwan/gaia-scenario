# TC-DATA-07 — 손상/암호화/빈 파일 인덱싱 장애 처리

| 파일 | 목적 | 비고 |
|---|---|---|
| `normal.pdf` | 정상 파일 대조군 | TC-DATA-01 fixture와 동일 내용 |
| `encrypted_password_poc-test-1234.pdf` | 암호화 PDF | 사용자 비밀번호: `poc-test-1234` |
| `corrupted.pdf` | 손상된 PDF | 정상 PDF를 1/3 지점에서 절단, PDF 구조 깨짐 |
| `empty_0byte.pdf` | 빈 파일 | 0바이트 |
| `unsupported_extension.xyz` | 미지원 확장자 | 공식 지원 목록(.doc/.docx 등)에 없는 확장자 |

## 절차
이 5개 파일을 모두 포함한 Dataset을 생성하고 Indexing 결과를 확인합니다.

## 예상 결과 / 합격 기준
- `normal.pdf`만 정상 인덱싱되고 나머지 4개는 실패 처리
- Index Status가 **Warning**으로 표시되고, 실패 문서 수(4개)와 사유가 UI에 명확히 노출
- 정상 파일(`normal.pdf`)의 인덱싱·질의응답은 다른 파일 실패에 영향받지 않아야 함
