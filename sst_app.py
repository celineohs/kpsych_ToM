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
STORY_TITLE = "어떤 일의 끝"

# 이야기 본문
STORY_TEXT = """
예전에 호턴스베이는 나무를 베어 목재를 만드는 마을이었다. 그 마을에 사는 사람이면 누구나 호숫가의 목재소에서 들리는 큰 톱 소리를 듣지 않을 수 없었다. 그러던 어느 해 더 이상 벌목할 나무들이 없어지고 말았다. 목재를 싣는 범선들이 만에 들어와서는 마당에 차곡차곡 쌓아 둔 목재를 실었다. 그러고는 산더미 같은 목재를 모두 싣고 떠났다. 커다란 목재소 건물에서 운반할 수 있는 기계는 모조리 일꾼들이 철거하여 범선 한 척에 끌어 올렸다. 범선은 큰 톱 두 개, 회전 원형 톱, 통나무를 들어 올리는 운반차, 롤러, 바퀴, 벨트, 쇠붙이 등을 뱃전까지 수북이 싣고 만에서 빠져나가 광활한 호수로 나아갔다. 무개(無蓋) 선창은 범포로 덮였고, 짐은 밧줄로 단단히 동여졌으며, 범선의 돛은 바람을 안고 잔뜩 부풀었다. 범선은 그 공장을 목재소로, 호턴스베이를 마을로 만들었던 그 모든 것을 싣고 널찍한 호수 한가운데로 움직여 나아갔다.

일 층짜리 합숙소며, 식당이며, 구내매점이며, 목재소 사무실이며, 그리고 목재소 자체가 만의 호반 옆 늪지 들판을 뒤덮은 수천 평의 톱밥 속에 그대로 버려졌다.

십 년 뒤 닉과 마저리가 호숫가를 따라 노를 저어 갈 때 이곳엔 주춧돌에서 깨진 흰 석회석만이 벌목한 뒤 늪지에 다시 자란 나무들 사이로 드러나 보일 뿐 목재소의 흔적은 하나도 없었다. 두 사람은 모래가 있는 얕은 수심에서 갑자기 3미터 반이 넘는 수심으로 떨어지는 수로의 둑을 따라 견지낚시를 하고 있었다. 무지개송어를 잡으려고 밤낚시 줄을 장치하기 위해 견지낚시를 하며 곶으로 가던 중이었다.

"저기 폐허가 된 우리 마을이 보이네, 닉." 마저리가 말했다.

노를 저으며 닉은 초록 나무 사이로 보이는 하얀 돌을 쳐다보았다.

"저기 보이는군." 닉이 말했다.

"목재소가 있던 때 기억나?" 마저리가 물었다.

"희미하게 기억나지." 닉이 대답했다.

"오히려 성(城)처럼 보이는데." 마저리가 말했다.

닉은 아무 말도 하지 않았다. 호반을 따라 계속 노를 저어 가자 목재소마저 시야에서 사라졌다. 그러고 나서 닉은 곧장 만을 가로질러 나아갔다.

"녀석들이 덤벼들질 않는군." 닉이 말했다.

"그러네." 마저리가 대꾸했다. 견지낚시를 하는 내내 그녀는 말할 때조차 낚싯대에 주의를 집중했다. 그녀는 낚시를 좋아했다. 닉과 함께하는 낚시를 좋아했다.

뱃전 가까이에서 큼직한 송어 한 마리가 수면을 갈랐다. 닉은 노 하나를 세게 잡아당겨 배가 돌면서 훨씬 뒤쪽에 있는 견지 미끼가 미끼를 먹고 있는 송어 쪽에 스쳐 가도록 했다. 송어의 등이 수면에서 솟아오르자 작은 물고기들이 마구 뛰었다. 작은 물고기들은 마치 탄환 한 줌을 물에 던진 것처럼 수면에 물을 흩뿌렸다. 송어 한 마리가 또 물을 가로지르며 배의 다른 쪽에서 먹이를 먹었다.

"지금 미끼를 먹고 있어." 마저리가 말했다.

"물려고 덤비지는 않을 거야." 닉이 말했다.

그는 배를 돌려 미끼를 먹는 물고기 두 마리를 스쳐 견지낚시를 한 뒤 곶을 향해 나아갔다. 마저리는 배가 호반에 닿을 때까지는 낚싯줄을 감아 들이지 않았다.

두 사람은 배를 호반 위로 끌어 올렸고, 닉은 살아 있는 농어를 담은 양동이를 들어 올렸다. 농어들은 양동이 물속에서 헤엄을 쳤다. 닉은 두 손으로 세 마리를 잡아 대가리를 잘라 내고 껍질을 벗겼다. 마저리도 두 손으로 양동이에 있는 물고기를 쫓다가 마침내 농어 한 마리를 잡아 대가리를 잘라 내고 껍질을 벗겼다. 닉은 그녀가 고기 잡는 모습을 지켜보았다.

"배지느러미를 떼어 내는 건 좋지 않아. 미끼로 사용하는 데야 상관없지만, 그래도 남겨 두는 게 나아." 닉이 말했다.

그는 껍질을 벗긴 농어를 한 마리씩 낚싯바늘로 꼬리를 엮어 붙잡아 맸다. 낚싯대마다 목줄에 바늘이 두 개씩 달려 있었다. 그러고 나서 마저리는 이빨에 낚싯줄을 물고 닉 쪽을 바라보며 노를 저어 수로의 둑 너머로 나아갔다. 닉은 호반에 서서 얼레에서 낚싯대를 들고 낚싯줄을 풀어 주었다.

"그쯤이면 될 것 같아." 닉이 소리를 질렀다.

"이제 줄 던질까?" 마저리도 손에 낚싯줄을 붙잡은 채 닉에게 큰 소리로 물었다.

"그래. 던져." 마저리는 뱃전 밖으로 낚싯줄을 던지고는 미끼가 물속으로 가라앉는 모습을 지켜보았다.

그녀는 배를 타고 돌아와 똑같은 방법으로 두 번째 낚싯줄을 던졌다. 그럴 때마다 닉은 육중한 유목(流木) 조각을 낚싯대 손잡이에 가로질러 놓아 단단하게 지탱시키고, 또 그 위에 작은 유목 조각으로 각이 지도록 버텨 놓았다. 늘어진 낚싯줄을 감아 미끼가 수로의 모랫바닥 위에 놓여 있는 곳까지 줄이 팽팽해지도록 하고, 소리가 나도록 얼레에 방울을 달았다. 호수 바닥에서 먹이를 먹던 송어가 미끼를 문다면 미끼와 함께 움직이면서 갑자기 얼레로부터 낚싯줄을 끌고 갈 것이고, 그렇게 되면 얼레에서 방울 소리가 날 것이다.

마저리는 낚싯줄을 방해하지 않으려고 곶 조금 위쪽으로 노를 저어 갔다. 노를 힘차게 저어 배를 물가 위까지 올려놓았다. 배와 함께 작은 파도가 밀려왔다. 마저리는 배에서 내렸고, 닉은 배를 호반 훨씬 위쪽으로 밀었다.

"왜 그래, 닉?" 마저리가 물었다.

"나도 잘 모르겠어." 닉이 불을 피울 나무를 모으면서 대답했다.

그들은 유목으로 불을 피웠다. 마저리가 배에 가서 담요 한 장을 가지고 왔다. 저녁 바람에 연기가 곶 쪽으로 불자 마저리는 불과 호수 사이에 담요를 깔았다.

마저리는 불을 등지고 담요 위에 앉아서 닉이 오기를 기다렸다. 그가 다가와 그녀 옆 담요 위에 앉았다. 그들 뒤쪽으로는 벌목한 뒤 두 번째로 자란 나무들이 이제는 제법 빽빽하게 들어찬 곶이 있었고, 앞쪽으로는 호턴스크릭 하구가 있는 만이 있었다. 아직 완전히 어두워진 건 아니었다. 모닥불의 불빛이 멀리 호수 물 위로도 어른거렸다. 어두운 물 위로 각도를 이루고 있는 금속 낚싯대 두 개가 보였다. 얼레 위에도 불빛이 밝게 비쳤다.

마저리는 저녁 식사를 담아 온 바구니를 풀었다.

"별로 먹고 싶지 않은데." 닉이 말했다.

"자, 어서 먹어 봐, 닉."

"그러지."

그들은 말없이 저녁을 먹으며 낚싯대 두 개와 물에 비치는 불빛을 지켜보았다.

"오늘 밤에는 달이 뜰 것 같은데." 닉이 말했다. 그는 만을 가로질러 하늘을 배경으로 윤곽이 점차 선명해지는 언덕을 바라보았다. 언덕 너머로 곧 달이 뜬다는 걸 그는 알았다.

"그건 나도 알아." 마저리가 행복한 듯이 말했다.

"넌 모르는 게 없지." 닉이 대꾸했다.

"아, 닉, 제발 그만 집어치워. 제발, 제발 그런 식으로 굴지 좀 마!"

"어쩔 수 없는걸. 사실이잖아. 넌 모르는 게 하나도 없어. 그게 문제야. 그건 너도 잘 알 테지." 닉이 말했다.

마저리는 아무런 대꾸도 하지 않았다.

"내가 모든 걸 가르쳐 줬지. 그건 너도 알 거야. 어쨌든 네가 모르는 게 도대체 뭐야?"

"아, 입 다물어." 마저리가 말했다. "저기 달이 뜬다."

그들은 서로 몸을 만지지도 않은 채 담요 위에 앉아 달이 뜨는 것을 지켜보았다.

"바보 같은 소리는 그만해. 진짜 고민이 뭐야?" 마저리가 물었다.

"잘 모르겠어."

"알잖아."

"아냐, 정말 몰라."

"그러지 말고 어디 말해 봐."

닉은 언덕 위에 떠오르고 있는 달을 계속 쳐다보았다.

"이런 일이 이젠 즐겁지 않아."

그는 마저리를 쳐다보기가 두려웠다. 조금 뒤 그는 그녀를 쳐다보았다. 그녀는 그에게 등을 지고 앉아 있었다. 그는 그녀의 등을 바라보았다. "이런 일이 이젠 즐겁지 않아. 이젠 재미가 없어. 모든 게 말이야."

마저리는 아무 말이 없었다. 닉은 다시 말을 이었다. "내 마음속에서 모든 게 엉망이 된 기분이야. 마지, 잘 모르겠어. 어떻게 말해야 될지 잘 모르겠어."

닉은 그녀의 등을 바라보았다.

"사랑도 이제 재미가 없는 거야?" 마저리가 물었다.

"응, 없어." 닉이 대답했다. 그러자 마저리는 자리에서 일어났다. 닉은 두 손으로 머리를 감싸고 그 자리에 그대로 앉아 있었다.

"난 배를 갖고 갈게. 넌 곶을 돌아서 걸어와." 마저리가 그에게 소리를 질렀다.

"좋아. 배를 밀어 줄게." 닉이 말했다.

"그럴 필요 없어." 그녀가 말했다. 달빛을 받으며 그녀는 배를 타고 물 위에 떠 있었다. 닉은 돌아가 모닥불 옆 담요에 이불을 파묻고 누웠다. 마저리가 물 위에서 노를 젓는 소리가 들렸다.

닉은 오랫동안 그곳에 누워 있었다. 빌이 숲 속을 지나 걸어서 개간지로 오는 동안에도 그는 누워 있었다. 빌이 모닥불로 다가오는 것이 느껴졌다. 빌은 그에게 손을 대지도 않았다.

"마저리는 잘 갔어?" 빌이 물었다.

"응." 닉이 담요에 얼굴을 파묻고 누운 채 대답했다.

"소란 피웠니?"

"아니, 그러지 않았어."

"지금 기분이 어때?"

"아, 제발 좀 가, 빌! 잠깐만 다른 곳에 가 있어 줘."

빌은 점심 바구니에서 샌드위치 하나를 고른 뒤 낚싯대를 보려고 걸어갔다.
"""

# 질문 목록 설정
# 각 질문은 딕셔너리 형태: {"id": 고유ID, "type": 질문유형, "text": 질문내용}
# type: "spontaneous" (자발적 추론), "mental_state" (정신상태 추론), "comprehension" (이해력)

QUESTIONS = [
    # 1. 자발적 정신상태 추론 (1문항)
    {
        "id": "S1",
        "type": "spontaneous",
        "text": "지금까지 읽은 단편 소설을 간단히 요약해 주세요."
    },

    # 2. 이해력 질문 (4문항)
    {
        "id": "C1",
        "type": "comprehension",
        "text": "닉과 마저리가 낚싯줄을 설치하러 곶으로 노를 저어가는 동안, 해안선에서 무엇을 목격하나요?"
    },
    {
        "id": "C2",
        "type": "comprehension",
        "text": "닉이 \"(물고기들이) 물려고 덤비지는 않을 거야.\"라고 한 것은 어떤 의미인가요?"
    },
    {
        "id": "C3",
        "type": "comprehension",
        "text": "닉과 마저리는 왜 농어 양동이를 가지고 있었나요?"
    },
    {
        "id": "C4",
        "type": "comprehension",
        "text": "마저리의 행동이 그녀가 낚시에 익숙한지 그렇지 않은지 보여주나요? 왜 그렇게 생각하시나요?"
    },

    # 3. 명시적 정신상태 추론 (8문항)
    {
        "id": "M1",
        "type": "mental_state",
        "text": "닉이 마저리에게 \"넌 모르는 게 없지.\"라고 말하는 이유는 무엇인가요?"
    },
    {
        "id": "M2",
        "type": "mental_state",
        "text": "마저리가 \"아, 닉, 제발 그만 집어치워. 제발, 제발 그런 식으로 굴지 좀 마!\"라고 대답하는 이유는 무엇인가요?"
    },
    {
        "id": "M3",
        "type": "mental_state",
        "text": "닉이 마저리를 똑바로 바라보기 두려워하는 이유는 무엇인가요?"
    },
    {
        "id": "M4",
        "type": "mental_state",
        "text": "닉이 \"이런 일이 이젠 즐겁지 않아.\"라고 한 것은 어떤 의미인가요?"
    },
    {
        "id": "M5",
        "type": "mental_state",
        "text": "마저리가 \"사랑도 이제 재미가 없는 거야?\"라고 물을 때, 마저리가 닉에게 등을 돌리고 앉아 있는 이유는 무엇인가요?"
    },
    {
        "id": "M6",
        "type": "mental_state",
        "text": "마저리가 보트를 타고 떠나는 이유는 무엇이고, 그 순간 그녀는 어떤 감정을 느끼고 있나요?"
    },
    {
        "id": "M7",
        "type": "mental_state",
        "text": "빌은 누구이고, 그가 닉에게 \"마저리는 잘 갔어? ... 소란 피웠니?\"라고 묻는 장면은 어떤 것을 드러내나요?"
    },
    {
        "id": "M8",
        "type": "mental_state",
        "text": "닉이 \"아, 제발 좀 가, 빌! 잠깐만 다른 곳에 가 있어 줘.\"라고 말할 때, 닉은 어떤 감정을 느끼고 있나요?"
    },

    # 4. 이해력 질문 (1문항)
    {
        "id": "C5",
        "type": "comprehension",
        "text": "이 이야기의 제목은 \"어떤 일의 끝\"입니다. 이 제목은 무엇을 가리키나요?"
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

    이제 귀하께서는 "어떤 일의 끝"이라는 단편 소설을 읽게 됩니다.

    이 소설은 몇 페이지밖에 되지 않지만, 천천히 읽어 주시길 바랍니다.

    무슨 일이 일어나는지, 등장인물들 간의 관계가 어떤지 파악하려고 노력해 주세요.

    다 읽으신 후에, 귀하께서는 이야기와 관련된 설문을 진행하시게 됩니다.

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
        age = st.number_input("나이", min_value=18, max_value=100, value=None, placeholder="나이를 입력하세요")
        gender = st.selectbox("성별", ["선택하세요", "남성", "여성"])
        education = st.selectbox(
            "최종 학력",
            ["선택하세요", "중학교 졸업 이하", "고등학교 졸업", "전문대학교 졸업", "4년제 대학교 졸업", "대학원 재학/수료/졸업"]
        )

        submitted = st.form_submit_button("다음", type="primary", use_container_width=True)

        if submitted:
            if not participant_id:
                st.error("참가자 ID를 입력해주세요.")
            elif age is None:
                st.error("나이를 입력해주세요.")
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

    이제 귀하께서는 **"{STORY_TITLE}"**이라는 단편 소설을 읽게 됩니다.

    이 소설은 몇 페이지밖에 되지 않지만, 천천히 읽어 주시길 바랍니다.

    무슨 일이 일어나는지, 등장인물들 간의 관계가 어떤지 파악하려고 노력해 주세요.

    다 읽으신 후에, 귀하께서는 이야기와 관련된 설문을 진행하시게 됩니다.

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
            ["예", "아니오"],
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
            ["예", "아니오"],
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

    **대부분의 질문에는 정답이 없으며, 짧은 응답으로 답할 수 있습니다.**

    **질문에 해당되는 경우, 등장인물의 생각, 감정, 의도에 대해서도 말씀해 주세요.**

    필요하시면 이야기 내용을 다시 참고하실 수 있습니다.
    """)

    # 이야기 다시 보기 (접을 수 있는 섹션)
    with st.expander("📖 이야기 다시 보기"):
        st.markdown(STORY_TEXT)

    st.markdown("---")

    with st.form("questions_form"):
        responses = {}

        for i, q in enumerate(QUESTIONS):
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

if __name__ == "__main__":
    main()
