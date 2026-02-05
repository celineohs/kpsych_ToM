"""
SST 시뮬레이션 데이터 생성 스크립트
15개의 샘플 응답을 생성하여 Google Sheets에 반영하고 CSV로 저장합니다.
"""
import toml
import random
import csv
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
import gspread

# Google Sheets 설정
GOOGLE_SHEETS_NAME = "SST_Responses"

# 질문 목록
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

# 샘플 응답 데이터
SAMPLE_RESPONSES = {
    "S1": [
        "닉과 마저리가 낚시를 하러 갔는데, 닉이 마저리에게 헤어지자고 말하는 내용입니다.",
        "옛 제재소 터에서 닉이 마저리와의 관계를 끝내는 이야기입니다.",
        "두 연인이 낚시를 하다가 닉이 이별을 통보하는 슬픈 이야기입니다.",
        "닉과 마저리가 호숫가에서 낚시를 하고, 닉이 관계가 끝났다고 말합니다.",
        "한 커플이 낚시를 하러 가서 남자가 여자에게 헤어지자고 하는 내용입니다."
    ],
    "C1": [
        "폐허가 된 제재소를 봅니다.",
        "옛 제재소의 잔해를 목격합니다.",
        "무너진 제재소 건물을 봅니다.",
        "제재소가 있던 자리의 폐허를 봅니다.",
        "호숫가의 오래된 제재소 터를 봅니다."
    ],
    "C2": [
        "닉이 저녁을 준비합니다.",
        "닉이 샌드위치를 꺼냅니다.",
        "닉이 음식을 챙겨왔습니다.",
        "닉이 가져온 음식으로 저녁을 먹습니다.",
        "닉이 준비해온 저녁 식사를 합니다."
    ],
    "C3": [
        "닉이 마저리에게 더 이상 재미가 없다고 말합니다.",
        "닉이 관계가 끝났다고 직접 말합니다.",
        "닉이 우리 사이가 끝났다고 합니다.",
        "닉이 더 이상 예전 같지 않다고 말합니다.",
        "닉이 이제 그만하자고 말합니다."
    ],
    "C4": [
        "마저리가 보트를 타고 떠납니다.",
        "마저리가 혼자 노를 저어 갑니다.",
        "마저리가 배를 타고 호수를 건너갑니다.",
        "마저리가 말없이 보트를 타고 사라집니다.",
        "마저리가 닉을 남겨두고 보트로 떠납니다."
    ],
    "M1": [
        "닉은 관계를 끝내야 한다고 생각하고 있었던 것 같습니다.",
        "닉은 이미 마음이 떠난 상태였던 것 같습니다.",
        "닉은 이별을 결심한 상태로 보입니다.",
        "닉은 마저리와의 미래가 없다고 느꼈던 것 같습니다.",
        "닉은 관계에 회의감을 느끼고 있었습니다."
    ],
    "M2": [
        "마저리는 충격을 받고 상처받았을 것 같습니다.",
        "마저리는 슬프고 당황스러웠을 것입니다.",
        "마저리는 예상치 못한 이별에 혼란스러웠을 것 같습니다.",
        "마저리는 배신감과 슬픔을 느꼈을 것입니다.",
        "마저리는 갑작스러운 통보에 마음이 아팠을 것입니다."
    ],
    "M3": [
        "빌은 닉의 친구로 닉을 위로하러 온 것 같습니다.",
        "빌은 닉이 힘든 일을 했다는 것을 알고 찾아온 것 같습니다.",
        "빌은 닉의 이별 소식을 알고 있었던 것 같습니다.",
        "빌은 닉을 지지하기 위해 나타났습니다.",
        "빌은 닉의 결정을 이미 알고 있었던 친구입니다."
    ],
    "M4": [
        "닉은 후회와 안도감이 섞인 복잡한 감정이었을 것 같습니다.",
        "닉은 홀가분하면서도 씁쓸했을 것입니다.",
        "닉은 해야 할 일을 했다는 안도감이 있었을 것 같습니다.",
        "닉은 미안하면서도 해방감을 느꼈을 것입니다.",
        "닉은 복잡한 심경이었을 것 같습니다."
    ],
    "M5": [
        "마저리는 닉이 더 이상 자신을 사랑하지 않는다고 생각했을 것입니다.",
        "마저리는 관계가 정말 끝났다고 받아들였을 것입니다.",
        "마저리는 닉의 마음이 변했다는 것을 깨달았을 것입니다.",
        "마저리는 자신이 버림받았다고 느꼈을 것입니다.",
        "마저리는 닉과의 미래가 없어졌다고 생각했을 것입니다."
    ],
    "M6": [
        "닉은 이별을 말하기가 어려웠을 것 같습니다.",
        "닉은 말을 꺼내기 힘들어했던 것 같습니다.",
        "닉은 오랫동안 고민했던 것 같습니다.",
        "닉은 마저리를 상처주고 싶지 않아서 망설였을 것입니다.",
        "닉은 어떻게 말해야 할지 몰라 힘들었을 것입니다."
    ],
    "M7": [
        "빌은 닉이 잘 해냈다고 생각했을 것 같습니다.",
        "빌은 닉을 걱정하면서도 지지하는 마음이었을 것입니다.",
        "빌은 닉이 힘들었을 것이라고 이해했을 것입니다.",
        "빌은 친구로서 닉 곁에 있어주고 싶었을 것입니다.",
        "빌은 닉의 결정을 존중하는 마음이었을 것입니다."
    ],
    "M8": [
        "마저리는 울고 싶거나 혼자 있고 싶었을 것 같습니다.",
        "마저리는 상황을 정리할 시간이 필요했을 것입니다.",
        "마저리는 슬픔을 삭이며 집에 가고 싶었을 것입니다.",
        "마저리는 닉에게서 멀리 떨어지고 싶었을 것입니다.",
        "마저리는 혼자만의 시간이 필요했을 것입니다."
    ],
    "C5": [
        "닉과 마저리의 관계가 끝났다는 의미인 것 같습니다.",
        "두 사람의 사랑이 끝났다는 뜻입니다.",
        "어떤 일, 즉 두 사람의 연애가 끝났다는 것을 의미합니다.",
        "관계의 종말을 상징하는 제목입니다.",
        "닉과 마저리 사이의 무언가가 끝났음을 나타냅니다."
    ]
}

# 샘플 참가자 데이터
SAMPLE_PARTICIPANTS = [
    {"age": 23, "gender": "여성", "education": "대학원 재학/수료/졸업"},
    {"age": 45, "gender": "남성", "education": "4년제 대학교 졸업"},
    {"age": 31, "gender": "여성", "education": "4년제 대학교 졸업"},
    {"age": 28, "gender": "남성", "education": "대학원 재학/수료/졸업"},
    {"age": 52, "gender": "여성", "education": "고등학교 졸업"},
    {"age": 19, "gender": "여성", "education": "고등학교 졸업"},
    {"age": 36, "gender": "남성", "education": "전문대학교 졸업"},
    {"age": 41, "gender": "여성", "education": "4년제 대학교 졸업"},
    {"age": 25, "gender": "남성", "education": "4년제 대학교 졸업"},
    {"age": 33, "gender": "여성", "education": "대학원 재학/수료/졸업"},
    {"age": 29, "gender": "남성", "education": "전문대학교 졸업"},
    {"age": 47, "gender": "여성", "education": "4년제 대학교 졸업"},
    {"age": 22, "gender": "남성", "education": "고등학교 졸업"},
    {"age": 38, "gender": "여성", "education": "대학원 재학/수료/졸업"},
    {"age": 26, "gender": "남성", "education": "4년제 대학교 졸업"},
]

def get_google_sheets_client():
    """Google Sheets 클라이언트 생성"""
    try:
        with open('.streamlit/secrets.toml', 'r') as f:
            secrets = toml.load(f)

        credentials_dict = secrets["gcp_service_account"]
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        print(f"Google Sheets 연결 실패: {e}")
        return None

def generate_simulation_data():
    """15개의 시뮬레이션 데이터 생성"""
    data = []
    base_time = datetime.now() - timedelta(days=7)

    for i in range(15):
        participant = SAMPLE_PARTICIPANTS[i]
        timestamp = (base_time + timedelta(hours=i*5, minutes=random.randint(0, 59))).strftime("%Y-%m-%d %H:%M:%S")

        # 사전 질문 응답 (일부는 "예", 일부는 "아니오")
        if i % 5 == 0:  # 5명 중 1명은 이전에 읽은 적 있음
            read_before = "예"
            read_when = random.choice(["5년 전", "고등학교 때", "3년 전", "대학교 때"])
            read_memory = random.choice(["대략적인 줄거리만 기억", "거의 기억 안 남", "줄거리와 인물 기억"])
            read_context = random.choice(["학교", "취미"])
            if read_context == "학교":
                read_grade = random.choice(["고등학교 2학년", "고등학교 3학년", "대학교 1학년"])
                read_class = random.choice(["문학", "국어", "영미문학"])
            else:
                read_grade = ""
                read_class = ""
        else:
            read_before = "아니오"
            read_when = ""
            read_memory = ""
            read_context = ""
            read_grade = ""
            read_class = ""

        if i % 4 == 0:  # 4명 중 1명은 이야기가 익숙함
            familiar = "예"
            familiar_knowledge = random.choice([
                "헤밍웨이의 단편소설이라고 들은 적 있습니다.",
                "제목만 들어본 적 있습니다.",
                "유명한 이별 이야기라고 알고 있습니다."
            ])
            familiar_discussion = random.choice([
                "친구와 이 소설에 대해 이야기한 적 있습니다.",
                "수업 시간에 토론한 적 있습니다.",
                "없습니다."
            ])
        else:
            familiar = "아니오"
            familiar_knowledge = ""
            familiar_discussion = ""

        # 응답 시간
        story_read_time = random.randint(180, 420)  # 3~7분
        total_time = story_read_time + random.randint(300, 600)  # 추가 5~10분

        row = {
            'timestamp': timestamp,
            'participant_id': f"P{str(i+1).zfill(3)}",
            'age': participant['age'],
            'gender': participant['gender'],
            'education': participant['education'],
            'story_read_time_sec': story_read_time,
            'total_time_sec': total_time,
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

        # 질문 응답 추가
        for q in QUESTIONS:
            row[f"response_{q['id']}"] = random.choice(SAMPLE_RESPONSES[q['id']])

        data.append(row)

    return data

def save_to_google_sheets(data):
    """Google Sheets에 데이터 저장"""
    client = get_google_sheets_client()
    if client is None:
        return False

    try:
        spreadsheet = client.open(GOOGLE_SHEETS_NAME)
        worksheet = spreadsheet.sheet1

        # 기존 데이터 삭제
        worksheet.clear()
        print("기존 데이터 삭제 완료")

        # 헤더 생성
        headers = list(data[0].keys())
        worksheet.append_row(headers)
        print(f"헤더 추가 완료: {len(headers)}개 컬럼")

        # 데이터 추가
        for row in data:
            worksheet.append_row(list(row.values()))

        print(f"✅ Google Sheets에 {len(data)}개 데이터 추가 완료")
        return True
    except Exception as e:
        print(f"❌ Google Sheets 저장 실패: {e}")
        return False

def save_to_csv(data, filename="simulation_results.csv"):
    """CSV 파일로 저장"""
    try:
        headers = list(data[0].keys())

        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

        print(f"✅ CSV 파일 저장 완료: {filename}")
        return True
    except Exception as e:
        print(f"❌ CSV 저장 실패: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("SST 시뮬레이션 데이터 생성")
    print("=" * 50)

    # 데이터 생성
    print("\n1. 데이터 생성 중...")
    data = generate_simulation_data()
    print(f"   {len(data)}개의 시뮬레이션 데이터 생성 완료")

    # Google Sheets에 저장
    print("\n2. Google Sheets에 저장 중...")
    save_to_google_sheets(data)

    # CSV로 저장
    print("\n3. CSV 파일로 저장 중...")
    save_to_csv(data)

    print("\n" + "=" * 50)
    print("완료!")
    print("=" * 50)
