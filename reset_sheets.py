"""
Google Sheets 초기화 스크립트
헤더만 생성하고 기존 데이터는 모두 삭제합니다.
"""
import toml
from google.oauth2.service_account import Credentials
import gspread

# Google Sheets 설정
GOOGLE_SHEETS_NAME = "SST_Responses"

# 질문 목록 (sst_app.py와 동일)
QUESTIONS = [
    {"id": "S1", "type": "spontaneous"},
    {"id": "C1", "type": "comprehension"},
    {"id": "C2", "type": "comprehension"},
    {"id": "C3", "type": "comprehension"},
    {"id": "C4", "type": "comprehension"},
    {"id": "M1", "type": "mental_state"},
    {"id": "M2", "type": "mental_state"},
    {"id": "M3", "type": "mental_state"},
    {"id": "M4", "type": "mental_state"},
    {"id": "M5", "type": "mental_state"},
    {"id": "M6", "type": "mental_state"},
    {"id": "M7", "type": "mental_state"},
    {"id": "M8", "type": "mental_state"},
    {"id": "C5", "type": "comprehension"},
]

def get_google_sheets_client():
    """Google Sheets 클라이언트 생성"""
    try:
        # .streamlit/secrets.toml 읽기
        with open('.streamlit/secrets.toml', 'r') as f:
            secrets = toml.load(f)

        credentials_dict = secrets["gcp_service_account"]

        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        credentials = Credentials.from_service_account_info(
            credentials_dict,
            scopes=scopes
        )

        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        print(f"Google Sheets 연결 실패: {e}")
        return None

def reset_spreadsheet():
    """스프레드시트 초기화"""
    client = get_google_sheets_client()

    if client is None:
        print("클라이언트 생성 실패")
        return False

    try:
        # 스프레드시트 열기
        spreadsheet = client.open(GOOGLE_SHEETS_NAME)
        worksheet = spreadsheet.sheet1

        # 모든 데이터 삭제
        worksheet.clear()
        print("기존 데이터 삭제 완료")

        # 헤더 생성
        headers = [
            'timestamp', 'participant_id', 'age', 'gender', 'education',
            'story_read_time_sec', 'total_time_sec',
            'read_before', 'read_when', 'read_memory', 'read_context',
            'read_grade', 'read_class', 'familiar', 'familiar_knowledge',
            'familiar_discussion'
        ]
        for q in QUESTIONS:
            headers.append(f"response_{q['id']}")

        # 헤더 추가
        worksheet.append_row(headers)
        print(f"헤더 생성 완료: {len(headers)}개 컬럼")
        print(f"헤더: {headers[:5]}... (총 {len(headers)}개)")

        return True

    except Exception as e:
        print(f"초기화 실패: {e}")
        return False

if __name__ == "__main__":
    print("Google Sheets 초기화 시작...")
    success = reset_spreadsheet()
    if success:
        print("✅ 초기화 완료!")
    else:
        print("❌ 초기화 실패")
