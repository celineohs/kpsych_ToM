# SST 배포 가이드

## Streamlit Cloud + Google Sheets 배포 방법

### 1단계: Google Cloud 설정

#### 1.1 Google Cloud 프로젝트 생성
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 (예: `sst-data-collection`)

#### 1.2 Google Sheets API 활성화
1. 왼쪽 메뉴 → "API 및 서비스" → "라이브러리"
2. "Google Sheets API" 검색 후 **사용 설정**
3. "Google Drive API"도 동일하게 **사용 설정**

#### 1.3 서비스 계정 생성
1. "API 및 서비스" → "사용자 인증 정보"
2. "사용자 인증 정보 만들기" → "서비스 계정"
3. 서비스 계정 이름 입력 (예: `sst-streamlit`)
4. 생성 완료 후, 서비스 계정 클릭
5. "키" 탭 → "키 추가" → "새 키 만들기" → **JSON** 선택
6. JSON 파일이 다운로드됨 (이 파일을 안전하게 보관!)

### 2단계: Google Sheets 준비

#### 2.1 스프레드시트 생성
1. [Google Sheets](https://sheets.google.com/) 접속
2. 새 스프레드시트 생성
3. 이름을 `SST_Responses`로 변경 (또는 sst_app.py의 `GOOGLE_SHEETS_NAME` 값과 일치)

#### 2.2 서비스 계정에 접근 권한 부여
1. 스프레드시트 열기
2. 오른쪽 상단 "공유" 버튼 클릭
3. 서비스 계정 이메일 추가 (JSON 파일의 `client_email` 값)
   - 형식: `xxx@xxx.iam.gserviceaccount.com`
4. **편집자** 권한 부여

### 3단계: GitHub 저장소 준비

#### 3.1 저장소 생성
1. GitHub에 새 저장소 생성 (예: `sst-task`)
2. 다음 파일들 업로드:
   - `sst_app.py`
   - `requirements.txt`

#### 3.2 .gitignore 추가 (선택)
```
.streamlit/secrets.toml
*.json
__pycache__/
```

### 4단계: Streamlit Cloud 배포

#### 4.1 Streamlit Cloud 연결
1. [Streamlit Cloud](https://share.streamlit.io/) 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. 저장소, 브랜치, 메인 파일(`sst_app.py`) 선택

#### 4.2 Secrets 설정 (중요!)
1. "Advanced settings" 클릭
2. "Secrets" 섹션에 다음 형식으로 입력:

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```

> **주의**: JSON 파일의 내용을 위 형식으로 변환해야 합니다.
> - `private_key`의 줄바꿈은 `\n`으로 변환

#### 4.3 배포 완료
1. "Deploy!" 클릭
2. 몇 분 후 앱이 배포됨
3. URL 형식: `https://your-app-name.streamlit.app`

### 5단계: 테스트

1. 배포된 URL 접속
2. 사이드바에서 "🟢 Google Sheets 연결됨" 확인
3. 테스트 응답 제출
4. Google Sheets에서 데이터 확인

---

## 로컬 테스트 방법

로컬에서 Google Sheets 연동을 테스트하려면:

### 1. secrets.toml 파일 생성

```bash
mkdir -p .streamlit
```

`.streamlit/secrets.toml` 파일 생성:

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
# ... (위와 동일)
```

### 2. 앱 실행

```bash
streamlit run sst_app.py
```

---

## 문제 해결

### "스프레드시트를 찾을 수 없습니다" 오류
- 스프레드시트 이름이 `GOOGLE_SHEETS_NAME`과 일치하는지 확인
- 서비스 계정에 스프레드시트 접근 권한이 있는지 확인

### "Google Sheets 연결 실패" 오류
- Secrets 설정이 올바른지 확인
- `private_key`의 줄바꿈 형식 확인

### 데이터가 저장되지 않음
- Google Sheets API가 활성화되어 있는지 확인
- 서비스 계정에 "편집자" 권한이 있는지 확인

---

## 보안 주의사항

1. **JSON 키 파일을 절대 GitHub에 업로드하지 마세요**
2. Streamlit Secrets만 사용하여 인증 정보 관리
3. 스프레드시트 공유 설정을 최소 권한으로 유지
