"""
Short Story Task (SST) - 데이터 수집 플랫폼
마음이론(Theory of Mind) 평가를 위한 Streamlit 애플리케이션

Based on: Dodell-Feder et al. (2013). Using Fiction to Assess Mental State Understanding.

배포: Streamlit Cloud + Google Sheets
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Google Sheets 연동을 위한 import
try:
    from google.oauth2.service_account import Credentials
    import gspread
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

# ============================================
# 설정 영역 - 여기에 텍스트와 질문을 입력하세요
# ============================================

# 이야기 제목
STORY_TITLE = "무언가의 끝"

# 이야기 본문 (한국어 번역본을 여기에 붙여넣으세요)
STORY_TEXT = """
[여기에 '무언가의 끝' 한국어 번역본 텍스트를 입력하세요]

번역본 파일 경로: ToM/무언가의 끝_한국어번역.txt
"""

# 질문 목록 설정
# 각 질문은 딕셔너리 형태: {"id": 고유ID, "type": 질문유형, "text": 질문내용}
# type: "spontaneous" (자발적 추론), "mental_state" (정신상태 추론), "comprehension" (이해력)

QUESTIONS = [
    # 1. 자발적 정신상태 추론 (1문항) - 가장 먼저 제시
    {
        "id": "S1",
        "type": "spontaneous",
        "text": "이 이야기를 간단히 요약해 주세요."
    },

    # 2. 명시적 정신상태 추론 (8문항)
    {
        "id": "M1",
        "type": "mental_state",
        "text": "[정신상태 추론 질문 1을 입력하세요]"
    },
    {
        "id": "M2",
        "type": "mental_state",
        "text": "[정신상태 추론 질문 2를 입력하세요]"
    },
    {
        "id": "M3",
        "type": "mental_state",
        "text": "[정신상태 추론 질문 3을 입력하세요]"
    },
    {
        "id": "M4",
        "type": "mental_state",
        "text": "[정신상태 추론 질문 4를 입력하세요]"
    },
    {
        "id": "M5",
        "type": "mental_state",
        "text": "[정신상태 추론 질문 5를 입력하세요]"
    },
    {
        "id": "M6",
        "type": "mental_state",
        "text": "[정신상태 추론 질문 6을 입력하세요]"
    },
    {
        "id": "M7",
        "type": "mental_state",
        "text": "[정신상태 추론 질문 7을 입력하세요]"
    },
    {
        "id": "M8",
        "type": "mental_state",
        "text": "[정신상태 추론 질문 8을 입력하세요]"
    },

    # 3. 이해력 질문 (5문항)
    {
        "id": "C1",
        "type": "comprehension",
        "text": "[이해력 질문 1을 입력하세요]"
    },
    {
        "id": "C2",
        "type": "comprehension",
        "text": "[이해력 질문 2를 입력하세요]"
    },
    {
        "id": "C3",
        "type": "comprehension",
        "text": "[이해력 질문 3을 입력하세요]"
    },
    {
        "id": "C4",
        "type": "comprehension",
        "text": "[이해력 질문 4를 입력하세요]"
    },
    {
        "id": "C5",
        "type": "comprehension",
        "text": "[이해력 질문 5를 입력하세요]"
    },
]

# Google Sheets 설정
GOOGLE_SHEETS_NAME = "SST_Responses"  # 스프레드시트 이름

# ============================================
# Google Sheets 연동 함수
# ============================================

def get_google_sheets_client():
    """Google Sheets 클라이언트 생성"""
    if not GSPREAD_AVAILABLE:
        return None

    try:
        # Streamlit secrets에서 credentials 가져오기
        credentials_dict = st.secrets["gcp_service_account"]

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
        st.error(f"Google Sheets 연결 실패: {e}")
        return None

def save_to_google_sheets(participant_info: dict, responses: dict, pre_story_responses: dict, timing: dict):
    """응답 데이터를 Google Sheets에 저장"""
    client = get_google_sheets_client()

    if client is None:
        return False, "Google Sheets 연결 실패"

    try:
        # 스프레드시트 열기 (없으면 생성)
        try:
            spreadsheet = client.open(GOOGLE_SHEETS_NAME)
        except gspread.SpreadsheetNotFound:
            return False, f"스프레드시트 '{GOOGLE_SHEETS_NAME}'를 찾을 수 없습니다."

        # 첫 번째 시트 선택
        worksheet = spreadsheet.sheet1

        # 헤더 확인 및 추가
        existing_data = worksheet.get_all_values()

        if len(existing_data) == 0:
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

            worksheet.append_row(headers)

        # 데이터 행 구성
        row = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            participant_info.get('id', ''),
            str(participant_info.get('age', '')),
            participant_info.get('gender', ''),
            participant_info.get('education', ''),
            str(round(timing.get('story_read_time', 0), 1)),
            str(round(timing.get('total_time', 0), 1)),
            pre_story_responses.get('read_before', ''),
            pre_story_responses.get('read_when', ''),
            pre_story_responses.get('read_memory', ''),
            pre_story_responses.get('read_context', ''),
            pre_story_responses.get('read_grade', ''),
            pre_story_responses.get('read_class', ''),
            pre_story_responses.get('familiar', ''),
            pre_story_responses.get('familiar_knowledge', ''),
            pre_story_responses.get('familiar_discussion', ''),
        ]

        for q in QUESTIONS:
            row.append(responses.get(q['id'], ''))

        # 행 추가
        worksheet.append_row(row)

        return True, "저장 완료"

    except Exception as e:
        return False, f"저장 실패: {str(e)}"

# ============================================
# 앱 기능 구현
# ============================================

def init_session_state():
    """세션 상태 초기화"""
    if 'page' not in st.session_state:
        st.session_state.page = 'intro'
    if 'participant_info' not in st.session_state:
        st.session_state.participant_info = {}
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    if 'pre_story_responses' not in st.session_state:
        st.session_state.pre_story_responses = {}
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'story_read_time' not in st.session_state:
        st.session_state.story_read_time = None

def check_google_sheets_config():
    """Google Sheets 설정 확인"""
    try:
        _ = st.secrets["gcp_service_account"]
        return True
    except (KeyError, FileNotFoundError):
        return False

def render_intro_page():
    """소개 페이지"""
    st.title("Short Story Task (SST)")
    st.subheader("마음이론 평가 과제")

    st.markdown("""
    ---
    ### 안내사항

    이 과제에서는 짧은 이야기를 읽고 몇 가지 질문에 답하게 됩니다.

    **진행 순서:**
    1. 기본 정보 입력
    2. 이야기 읽기
    3. 질문에 대한 응답

    **유의사항:**
    - 이야기는 몇 페이지밖에 되지 않지만, 천천히 읽어주세요.
    - 무슨 일이 일어나는지, 등장인물들의 관계가 어떤지 파악하려고 노력해 주세요.
    - 이야기를 다 읽으신 후에 몇 가지 질문을 드리고 응답을 녹음할 것입니다.

    ---
    """)

    if st.button("시작하기", type="primary", use_container_width=True):
        st.session_state.page = 'participant_info'
        st.session_state.start_time = datetime.now()
        st.rerun()

def render_participant_info_page():
    """참가자 정보 입력 페이지"""
    st.title("참가자 정보")

    with st.form("participant_form"):
        participant_id = st.text_input("참가자 ID", placeholder="예: P001")
        age = st.number_input("나이", min_value=18, max_value=100, value=25)
        gender = st.selectbox("성별", ["선택하세요", "남성", "여성", "기타", "응답하지 않음"])
        education = st.selectbox(
            "최종 학력",
            ["선택하세요", "고등학교 졸업", "대학교 재학", "대학교 졸업", "대학원 재학", "대학원 졸업"]
        )

        submitted = st.form_submit_button("다음", type="primary", use_container_width=True)

        if submitted:
            if not participant_id:
                st.error("참가자 ID를 입력해주세요.")
            elif gender == "선택하세요":
                st.error("성별을 선택해주세요.")
            elif education == "선택하세요":
                st.error("최종 학력을 선택해주세요.")
            else:
                st.session_state.participant_info = {
                    'id': participant_id,
                    'age': age,
                    'gender': gender,
                    'education': education
                }
                st.session_state.page = 'instruction'
                st.rerun()

def render_instruction_page():
    """지시문 페이지"""
    st.title("과제 안내")

    st.markdown(f"""
    ---

    이제 **"{STORY_TITLE}"**이라는 단편소설을 읽게 됩니다.

    이 이야기는 몇 페이지밖에 되지 않지만, **천천히 읽어주세요.**

    무슨 일이 일어나는지, 등장인물들 간의 관계가 어떤지 파악하려고 노력해 주세요.

    다 읽으신 후에 몇 가지 질문을 드리고 응답을 녹음할 것입니다.

    ---

    **대부분의 질문에는 정답이 없으며, 짧은 응답으로 답할 수 있습니다.**

    **질문에 해당되는 경우, 등장인물의 생각, 감정, 의도에 대해서도 말씀해 주세요.**

    ---
    """)

    st.info("💡 시작하기 전에 질문이 있으시면 연구자에게 문의해 주세요.")

    if st.button("이야기 읽기 시작", type="primary", use_container_width=True):
        st.session_state.story_start_time = datetime.now()
        st.session_state.page = 'story'
        st.rerun()

def render_story_page():
    """이야기 읽기 페이지"""
    st.title(f"📖 {STORY_TITLE}")

    st.markdown("---")

    # 이야기 본문을 스크롤 가능한 컨테이너에 표시
    st.markdown(
        f"""
        <div style="
            background-color: #f9f9f9;
            padding: 30px;
            border-radius: 10px;
            font-size: 1.1em;
            line-height: 1.8;
            max-height: 500px;
            overflow-y: auto;
            border: 1px solid #ddd;
        ">
        {STORY_TEXT.replace(chr(10), '<br>')}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.info("이야기를 다 읽으셨으면 아래 버튼을 눌러주세요.")

    if st.button("다 읽었습니다", type="primary", use_container_width=True):
        # 이야기 읽기 시간 계산
        if hasattr(st.session_state, 'story_start_time'):
            read_duration = (datetime.now() - st.session_state.story_start_time).total_seconds()
            st.session_state.story_read_time = read_duration
        st.session_state.page = 'pre_questions'
        st.rerun()

def render_pre_questions_page():
    """이야기 읽은 후 사전 질문 페이지"""
    st.title("사전 확인 질문")

    st.markdown("""
    ---
    이야기에 대한 몇 가지 간단한 질문을 드리겠습니다.
    """)

    with st.form("pre_questions_form"):
        # 1. 이전에 읽은 적 있는지
        st.subheader("1. 이야기 경험")
        read_before = st.radio(
            "이 이야기를 전에 읽어본 적 있으신가요?",
            ["아니오", "예"],
            key="read_before"
        )

        # 읽어본 적 있는 경우 추가 질문
        read_when = ""
        read_memory = ""
        read_context = ""
        read_grade = ""
        read_class = ""

        if read_before == "예":
            st.markdown("---")
            read_when = st.text_input(
                "얼마나 오래 전에 읽으셨나요?",
                placeholder="예: 5년 전, 고등학교 때 등"
            )
            read_memory = st.text_input(
                "이야기를 얼마나 잘 기억하시나요?",
                placeholder="예: 대략적인 줄거리만, 세부 내용까지 등"
            )
            read_context = st.radio(
                "학교에서 읽으셨나요, 아니면 취미로 읽으셨나요?",
                ["취미", "학교", "기타"],
                key="read_context"
            )

            if read_context == "학교":
                read_grade = st.text_input("몇 학년 때였나요?", placeholder="예: 고등학교 2학년")
                read_class = st.text_input("어떤 수업이었나요?", placeholder="예: 문학, 국어 등")

        st.markdown("---")

        # 2. 이야기가 익숙한지
        st.subheader("2. 이야기 친숙도")
        familiar = st.radio(
            "이 이야기가 익숙하신가요?",
            ["아니오", "예"],
            key="familiar"
        )

        # 익숙한 경우 추가 질문
        familiar_knowledge = ""
        familiar_discussion = ""

        if familiar == "예":
            st.markdown("---")
            familiar_knowledge = st.text_area(
                "이 이야기에 대해 아시는 것이 있으신가요? 무엇을 아시나요?",
                placeholder="알고 계신 내용을 자유롭게 작성해 주세요...",
                height=100
            )
            familiar_discussion = st.text_area(
                "누군가와 이 이야기에 대해 이야기한 적 있으신가요? 어떤 내용이었나요?",
                placeholder="대화 내용을 자유롭게 작성해 주세요...",
                height=100
            )

        st.markdown("---")

        submitted = st.form_submit_button("다음", type="primary", use_container_width=True)

        if submitted:
            # 응답 저장
            st.session_state.pre_story_responses = {
                'read_before': read_before,
                'read_when': read_when,
                'read_memory': read_memory,
                'read_context': read_context,
                'read_grade': read_grade,
                'read_class': read_class,
                'familiar': familiar,
                'familiar_knowledge': familiar_knowledge,
                'familiar_discussion': familiar_discussion
            }
            st.session_state.page = 'questions'
            st.rerun()

def render_questions_page():
    """질문 응답 페이지"""
    st.title("질문")

    st.markdown("""
    ---
    아래 질문들에 대해 자유롭게 응답해 주세요.

    필요하시면 이야기 내용을 다시 참고하실 수 있습니다.
    """)

    # 이야기 다시 보기 (접을 수 있는 섹션)
    with st.expander("📖 이야기 다시 보기"):
        st.markdown(STORY_TEXT)

    st.markdown("---")

    # 질문 유형별 라벨
    type_labels = {
        "spontaneous": "이야기 요약",
        "mental_state": "등장인물의 마음 상태",
        "comprehension": "이야기 이해"
    }

    with st.form("questions_form"):
        responses = {}

        current_type = None
        for i, q in enumerate(QUESTIONS):
            # 질문 유형이 바뀌면 구분선 표시
            if q['type'] != current_type:
                current_type = q['type']
                st.subheader(type_labels.get(current_type, current_type))

            # 질문 표시 및 응답 입력
            st.markdown(f"**{i+1}. {q['text']}**")
            responses[q['id']] = st.text_area(
                label=f"응답 {q['id']}",
                key=f"response_{q['id']}",
                height=100,
                label_visibility="collapsed",
                placeholder="여기에 응답을 입력하세요..."
            )
            st.markdown("---")

        submitted = st.form_submit_button("제출하기", type="primary", use_container_width=True)

        if submitted:
            # 빈 응답 확인
            empty_responses = [q['id'] for q in QUESTIONS if not responses.get(q['id'], '').strip()]

            if empty_responses:
                st.warning(f"아직 응답하지 않은 질문이 있습니다: {', '.join(empty_responses)}")
                st.info("모든 질문에 응답해 주세요.")
            else:
                st.session_state.responses = responses
                st.session_state.page = 'complete'
                st.rerun()

def render_complete_page():
    """완료 페이지"""
    # 전체 소요 시간 계산
    if st.session_state.start_time:
        total_time = (datetime.now() - st.session_state.start_time).total_seconds()
    else:
        total_time = 0

    timing = {
        'story_read_time': st.session_state.get('story_read_time', 0),
        'total_time': total_time
    }

    st.title("과제 완료")

    # Google Sheets에 저장 시도
    if check_google_sheets_config():
        with st.spinner("응답을 저장하는 중..."):
            success, message = save_to_google_sheets(
                st.session_state.participant_info,
                st.session_state.responses,
                st.session_state.pre_story_responses,
                timing
            )

        if success:
            st.success("응답이 성공적으로 저장되었습니다!")
        else:
            st.error(f"저장 중 오류 발생: {message}")
    else:
        st.warning("Google Sheets가 설정되지 않았습니다. 로컬 테스트 모드입니다.")
        st.info("배포 시 Streamlit secrets에 Google 서비스 계정 정보를 설정하세요.")

    st.markdown(f"""
    ---

    ### 참여해 주셔서 감사합니다!

    **소요 시간:**
    - 이야기 읽기: {timing['story_read_time']:.1f}초
    - 전체 과제: {timing['total_time']:.1f}초

    ---
    """)

    if st.button("새 참가자 시작", type="primary", use_container_width=True):
        # 세션 상태 초기화
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def render_admin_page():
    """관리자 페이지 - 수집된 데이터 확인"""
    st.title("📊 수집된 데이터")

    if not check_google_sheets_config():
        st.error("Google Sheets가 설정되지 않았습니다.")
        st.markdown("""
        ### 설정 방법
        1. Google Cloud Console에서 서비스 계정 생성
        2. Google Sheets API 활성화
        3. Streamlit secrets에 credentials 추가
        """)
        return

    client = get_google_sheets_client()

    if client:
        try:
            spreadsheet = client.open(GOOGLE_SHEETS_NAME)
            worksheet = spreadsheet.sheet1

            # 모든 값을 가져와서 수동으로 DataFrame 생성
            all_values = worksheet.get_all_values()

            if len(all_values) > 1:  # 헤더 + 최소 1개 데이터
                headers = all_values[0]
                data_rows = all_values[1:]
                df = pd.DataFrame(data_rows, columns=headers)

                st.markdown(f"**총 {len(df)}개의 응답이 수집되었습니다.**")
                st.dataframe(df, use_container_width=True)

                # CSV 다운로드 버튼
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="CSV 파일 다운로드",
                    data=csv,
                    file_name=f"sst_responses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime='text/csv',
                    use_container_width=True
                )
            elif len(all_values) == 1:
                st.info("헤더만 있고 아직 수집된 데이터가 없습니다.")
            else:
                st.info("아직 수집된 데이터가 없습니다.")

        except gspread.SpreadsheetNotFound:
            st.error(f"스프레드시트 '{GOOGLE_SHEETS_NAME}'를 찾을 수 없습니다.")
        except Exception as e:
            st.error(f"데이터 로드 실패: {e}")

    st.markdown("---")

    if st.button("돌아가기", use_container_width=True):
        st.session_state.page = 'intro'
        st.rerun()

def main():
    """메인 함수"""
    st.set_page_config(
        page_title="Short Story Task (SST)",
        page_icon="📖",
        layout="centered"
    )

    # 세션 상태 초기화
    init_session_state()

    # 사이드바에 진행 상황 표시
    with st.sidebar:
        st.markdown("### 진행 상황")
        pages = ['intro', 'participant_info', 'instruction', 'story', 'pre_questions', 'questions', 'complete']
        page_names = ['시작', '참가자 정보', '안내', '이야기 읽기', '사전 질문', '질문 응답', '완료']

        current_idx = pages.index(st.session_state.page) if st.session_state.page in pages else 0

        for i, (page, name) in enumerate(zip(pages, page_names)):
            if i < current_idx:
                st.markdown(f"✅ {name}")
            elif i == current_idx:
                st.markdown(f"👉 **{name}**")
            else:
                st.markdown(f"⬜ {name}")

        st.markdown("---")

        # 연결 상태 표시
        if check_google_sheets_config():
            st.success("🟢 Google Sheets 연결됨")
        else:
            st.warning("🟡 로컬 테스트 모드")

        st.markdown("---")
        st.markdown("**관리자 메뉴**")
        if st.button("데이터 확인", use_container_width=True):
            st.session_state.page = 'admin'
            st.rerun()

    # 페이지 라우팅
    if st.session_state.page == 'intro':
        render_intro_page()
    elif st.session_state.page == 'participant_info':
        render_participant_info_page()
    elif st.session_state.page == 'instruction':
        render_instruction_page()
    elif st.session_state.page == 'story':
        render_story_page()
    elif st.session_state.page == 'pre_questions':
        render_pre_questions_page()
    elif st.session_state.page == 'questions':
        render_questions_page()
    elif st.session_state.page == 'complete':
        render_complete_page()
    elif st.session_state.page == 'admin':
        render_admin_page()

if __name__ == "__main__":
    main()
