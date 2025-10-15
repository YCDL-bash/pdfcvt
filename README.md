# PDF to Markdown & Text Converter (Final v2)

PDF를 **마크다운(.md)**과 **순수 텍스트(.txt)** 두 가지 형식으로 동시에 변환하는 Python 프로그램입니다.

## 🎯 왜 두 가지 형식?

### 📝 Markdown (.md)
- 표 구조 유지
- 제목 계층 구조 표시
- 마크다운 뷰어에서 보기 좋음
- 문서 구조 파악에 유리

### 📄 Plain Text (.txt)
- **순수 텍스트만 추출**
- **AI 분석에 더 적합** ⭐
- 마크다운 서식으로 인한 혼란 없음
- 표는 탭으로 구분된 간단한 형식
- 내용에만 집중한 분석 가능

## 📦 출력 예시

### 한 번의 변환으로 두 파일 생성

```
C:\dev\python\pdfcvt\output\
└── document\
    ├── document.md      # 마크다운 버전
    └── document.txt     # 텍스트 버전
```

## 📋 파일 형식 비교

### Markdown (.md) 예시
```markdown
---
title: 운전 매뉴얼
author: Unknown
pages: 200
---

## Page 1

### 운전 절차

| 항목 | 값 |
| --- | --- |
| 온도 | 98℃ |
| 압력 | 2.5bar |

*[2 image(s) on this page]*
```

### Plain Text (.txt) 예시
```
============================================================
Title: 운전 매뉴얼
Author: Unknown
Pages: 200
============================================================

[Page 1]

운전 절차

[TABLE]
항목	값
온도	98℃
압력	2.5bar

[2 image(s) on this page]
```

## 🚀 사용 방법

### 기본 사용 (배치 변환)

```bash
# source 폴더의 모든 PDF를 변환
python pdf_to_md.py
```

**결과:**
```
🔄 Batch conversion mode (default paths)

📁 Source: C:\dev\python\pdfcvt\source
📁 Output: C:\dev\python\pdfcvt\output
📄 Found 2 PDF file(s)

============================================================
[1/2] Converting: manual.pdf
============================================================
📄 Processing 150 pages...
   Processed 1/150 pages...
   Processed 10/150 pages...
   ...
✅ Success!
   📝 Markdown: C:\dev\python\pdfcvt\output\manual\manual.md
   📄 Text: C:\dev\python\pdfcvt\output\manual\manual.txt
   📊 Tables: 28, Images: 45

============================================================
📊 Conversion Summary
============================================================
✅ Successful: 2
❌ Failed: 0
📊 Total tables: 45
🖼️  Total images detected: 78

All converted files are in: C:\dev\python\pdfcvt\output
Each PDF produced 2 files: .md (markdown) and .txt (plain text)
```

### 단일 PDF 변환

```bash
python pdf_to_md.py document.pdf
```

### 커스텀 출력 경로

```bash
python pdf_to_md.py document.pdf C:\custom\output
```

## 💡 언제 어떤 파일을 사용할까?

### `.md` 파일 사용 시기
- ✅ 문서 구조를 시각적으로 확인할 때
- ✅ 표를 제대로 된 형식으로 볼 때
- ✅ GitHub, Notion 등에 업로드할 때
- ✅ 마크다운 에디터에서 작업할 때

### `.txt` 파일 사용 시기  
- ⭐ **AI에게 분석을 요청할 때** (추천!)
- ⭐ **순수 텍스트 내용만 필요할 때**
- ✅ 검색이나 텍스트 마이닝할 때
- ✅ 다른 도구로 후처리할 때
- ✅ 파일 크기를 줄이고 싶을 때

## 🤖 AI 분석 활용 예시

### 시나리오 1: Claude/ChatGPT에게 문서 요약 요청

```
사용자: "이 운전 매뉴얼을 요약해줘"

[manual.txt 파일 첨부] ← .md보다 .txt 추천!

AI: 표 구조 때문에 혼란 없이 순수 내용만 분석
```

### 시나리오 2: 키워드 검색

```python
# .txt 파일이 더 깔끔한 검색 결과 제공
with open('manual.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    if '압력' in content:
        print("압력 관련 내용 발견!")
```

### 시나리오 3: 대량 문서 분석

```python
# 여러 txt 파일을 합쳐서 한 번에 분석
all_text = ""
for txt_file in glob.glob("output/*/*.txt"):
    with open(txt_file, 'r', encoding='utf-8') as f:
        all_text += f.read() + "\n\n"

# AI에게 전체 내용 분석 요청
```

## 📊 두 형식의 차이점

| 특징 | Markdown (.md) | Plain Text (.txt) |
|------|----------------|-------------------|
| 파일 크기 | 약간 더 큼 | 작음 |
| 가독성 | 구조화됨 | 단순함 |
| AI 분석 | 좋음 | **매우 좋음** ⭐ |
| 표 형식 | 마크다운 테이블 | 탭으로 구분 |
| 메타데이터 | YAML 형식 | 텍스트 헤더 |
| 이미지 표시 | `*[N image(s)]*` | `[N image(s)]` |

## 🎨 실제 변환 결과 비교

### 원본 PDF의 표

```
┌─────────┬────────┐
│  항목   │   값   │
├─────────┼────────┤
│  온도   │  98℃  │
│  압력   │ 2.5bar │
└─────────┴────────┘
```

### Markdown 변환 결과

```markdown
| 항목 | 값 |
| --- | --- |
| 온도 | 98℃ |
| 압력 | 2.5bar |
```

### Text 변환 결과

```
[TABLE]
항목	값
온도	98℃
압력	2.5bar
```

## 🛠️ 설치 및 설정

### 1. 폴더 구조

```
C:\dev\python\pdfcvt\
├── pdf_to_md.py
├── requirements.txt
├── source\          # PDF를 여기에 넣으세요
└── output\          # 결과가 여기에 저장됩니다
    └── document\
        ├── document.md
        └── document.txt
```

### 2. 설치

```bash
cd C:\dev\python\pdfcvt
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 사용

```bash
# PDF 파일을 source 폴더에 넣기
# 그냥 실행!
python pdf_to_md.py
```

## 📝 배치 파일로 더 쉽게

`convert.bat` 파일 생성:

```batch
@echo off
echo ========================================
echo PDF to Markdown and Text Converter
echo ========================================
echo.

cd C:\dev\python\pdfcvt
call venv\Scripts\activate
python pdf_to_md.py

echo.
echo ========================================
echo 변환 완료!
echo output 폴더에서 .md와 .txt 파일을 확인하세요.
echo ========================================
pause
```

더블클릭으로 실행! 🖱️

## 💡 활용 팁

### 팁 1: AI 분석 시 TXT 사용

```
❌ 비추천: manual.md 파일을 AI에게 업로드
   → 마크다운 문법 때문에 약간의 노이즈 발생

✅ 추천: manual.txt 파일을 AI에게 업로드
   → 순수 텍스트만 있어서 분석이 더 정확
```

### 팁 2: 목적에 따라 선택

```
문서 리뷰/편집 → .md 파일 사용
AI 분석/요약 → .txt 파일 사용
아카이빙 → 둘 다 보관
```

### 팁 3: 대량 처리

```bash
# source 폴더에 100개 PDF 넣기
# 한 번 실행으로 200개 파일 생성 (각각 .md와 .txt)
python pdf_to_md.py
```

## 🔍 차이점 예시

### 복잡한 표가 있는 경우

**Markdown (.md):**
```markdown
| 운전 절차 구분 | 운전 패턴 설명 | 운전 유형 구분 | 비고 |
| --- | --- | --- | --- |
| 축열 | 온도조절밸브를 통해 축열 온도 98℃ 조절 | 수동 |  |
```
→ 표 구조가 명확하지만, AI가 파싱할 때 약간 복잡할 수 있음

**Plain Text (.txt):**
```
[TABLE]
운전 절차 구분	운전 패턴 설명	운전 유형 구분	비고
축열	온도조절밸브를 통해 축열 온도 98℃ 조절	수동	
```
→ 탭으로 구분되어 있어서 AI가 더 쉽게 이해

## ⚙️ 기술 상세

### Text 변환 특징

1. **메타데이터**: YAML 대신 간단한 텍스트 헤더
2. **제목**: 마크다운 `###` 대신 빈 줄로 강조
3. **표**: 마크다운 테이블 대신 탭으로 구분
4. **이미지**: `*[N image(s)]*` 대신 `[N image(s)]`
5. **구분선**: `---` 대신 `-` 60개

### 처리 흐름

```
PDF 입력
    ↓
텍스트 추출
    ↓
    ├→ Markdown 형식 변환 → .md 저장
    └→ Plain Text 형식 변환 → .txt 저장
```

## 🎯 실전 사용 예시

### 사례 1: 기술 문서 분석

```bash
# 1. 기술 문서 PDF 변환
python pdf_to_md.py technical_manual.pdf

# 2. AI에게 질문
"technical_manual.txt를 보고 주요 위험 요소를 알려줘"
```

### 사례 2: 계약서 검토

```bash
# 1. 계약서 변환
python pdf_to_md.py contract.pdf

# 2-1. .md로 구조 확인
# 2-2. .txt를 AI에게: "이 계약서에서 불리한 조항을 찾아줘"
```

### 사례 3: 학술 논문

```bash
# 1. 논문 PDF 배치 변환
python pdf_to_md.py

# 2. .txt 파일들을 AI에게: "이 논문들의 공통 주제는?"
```

## 📚 FAQ

**Q: .md와 .txt 중 어느 것을 사용해야 하나요?**
A: AI 분석용이면 `.txt`, 사람이 읽을 거면 `.md`

**Q: 둘 다 저장되나요?**
A: 네! 한 번 실행으로 두 파일 모두 생성됩니다.

**Q: .txt 파일이 더 작나요?**
A: 네, 마크다운 문법이 없어서 약 10-20% 작습니다.

**Q: 표 정보가 손실되나요?**
A: 아니요, 탭으로 구분되어 모든 정보가 유지됩니다.

**Q: 기존 코드와 호환되나요?**
A: 네, 이전 버전과 동일하게 사용 가능합니다.

## 🔄 이전 버전과의 차이

### v2 (현재)
- ✅ `.md`와 `.txt` 동시 생성
- ✅ AI 분석에 최적화
- ✅ 두 가지 형식 제공

### v1 (이전)
- `.md`만 생성
- 한 가지 형식만 제공

## 🎉 시작하기

```bash
# 1. 폴더 이동
cd C:\dev\python\pdfcvt

# 2. 가상환경 활성화
venv\Scripts\activate

# 3. PDF를 source 폴더에 넣기

# 4. 변환!
python pdf_to_md.py

# 5. output 폴더 확인
# 각 PDF마다 .md와 .txt 두 파일이 생성됩니다!
```

**이제 상황에 맞게 `.md` 또는 `.txt`를 선택해서 사용하세요!** 🚀

---

**추천**: AI 분석용으로는 항상 `.txt` 파일을 사용하세요. 더 깔끔하고 정확한 분석이 가능합니다! ⭐
