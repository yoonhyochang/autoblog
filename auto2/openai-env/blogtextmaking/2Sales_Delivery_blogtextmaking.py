import os
import subprocess
import json
import re
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from openai import OpenAI
import sys
sys.path.append('C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env')
from config import API_KEY

#가상환경 세팅 openai-env\Scripts\activate


# 중복 방지 데이터를 저장하거나 업데이트하는 함수
def update_Content_file(Content_new_item):
    Content_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\Contentjson\\Sales_Delivery_Content.json'
    # 파일에서 기존 데이터를 로드하거나, 기본 데이터 구조를 초기화합니다.
    if os.path.exists(Content_file_path):
        with open(Content_file_path, 'r', encoding='utf-8') as file:
            Content_data = json.load(file)
    else:
        Content_data = {"Content": []}

    # 중복 검사: 새 아이템이 기존 데이터에 없는 경우에만 추가
    if Content_new_item not in Content_data["Content"]:
        Content_data["Content"].append(Content_new_item)
        with open(Content_file_path, 'w', encoding='utf-8') as file:
            json.dump(Content_data, file, ensure_ascii=False, indent=4)

# 중복 방지 데이터를 파일에서 불러오는 함수
def load_Content_data():
    file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\Contentjson\\Sales_Delivery_Content.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {"Content": []}

# 중복 방지 데이터 불러오기
Content_data = load_Content_data()

# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
existing_Content = [item[0] for item in Content_data.get("Sales_Delivery_Content", [])]

# 기존 주제와 카테고리를 문자열로 변환
existing_topics_str = ", ".join(existing_Content)



# OpenAI 클라이언트 설정
client = OpenAI(api_key=os.environ.get(f"{API_KEY}"))
# GPT 모델을 사용해 요청 처리

# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
content_items = [item for item in Content_data.get("Sales_Delivery_Content", [])]

topics_and_categories = []
additional_info = []
mainKeyword="마(Dioscorea opposita)와 당화혈색소"

# 대화 맥락을 유지하기 위한 메시지 배열 초기화
messages = []

# 시스템 메시지에 전문가 역할과 맥락을 명확화하여 추가
system_message_role = {
    "role": "system",
    "content": "이 대화는 B2B 영업 전략, 신규 고객 개발, 가치 제안, 고객 관리 및 서비스 우수성을 포함한 다양한 산업 분야에서 20년 경력을 보유한 영업 관리 전문가의 관점으로 진행됩니다. 전문가는 고객 만족과 장기적인 관계 구축에 중점을 두며, 실제 성공 사례와 실패 사례를 통해 얻은 깊은 통찰력을 공유합니다."
}
messages.append(system_message_role)  # 전문가 역할을 설명하는 시스템 메시지를 메시지 배열에 추가

for content_item in content_items:
    # 첫 번째 요청에 대한 시스템 메시지 추가
    system_message_first = {
        "role": "system", 
        "content": f"({content_item}) 내용을 분석하여 영업의 기본과 계획에 대해 논의하고, 영업 전략의 구체적인 예시와 실제 적용 사례를 포함하여 해결 방안을 제시합니다."
    }

    # 첫 번째 요청
    initial_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages + [system_message_first, {
            "role": "user",
            "content": f"""
             아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
1.영업의 기본과 계획
    1.1.영업이란
    1.2.영업의 위치
    1.3.영업의 철학
    1.4.영업사원
    1.5.방문준비
    1.6.상품지식
    1.7.판매요점
    1.8.역할연기
    1.9.영업 목표 세우기
    1.10.판매 목표 세우기
    1.11.판매 목표 나누기
    1.12.고객만족을 위한 마음가짐
    1.13.서비스를 위한 마음가짐
    1.14.마케팅을 위한 마음가짐
    1.15.판매 지역도
    1.16.시간관리
            """
        }]
    )

    # 첫 번째 응답을 메시지 배열에 추가
    messages.append(system_message_first)
    messages.append({
        "role": "assistant",
        "content": initial_completion.choices[0].message.content
    })




    # 두 번째 요청
    second_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages + [system_message_first, {
            "role": "user",
            "content": f"""
            아래 목차에 맞는 영업 실천과 행동을 구체적인 상황 예시와 함께 설명해 주세요. 특히, 고객과의 상호작용, 판매 전략, 그리고 고객 관리 방법에 대한 실제 사례를 포함해 주세요.
2.영업의 실천과 행동
    2.1.자기소개
    2.2.구매심리
    2.3.판매화법
    2.4.임기응변
    2.5.점두판매
    2.6.매장연출
    2.7.현장영업
    2.8.신규개척
    2.9.판촉관리
    2.10.영업물류
    2.11.진열관리
    2.12.수금관리
            """
        }]
    )

    # 두 번째 응답을 메시지 배열에 추가
    messages.append({
        "role": "assistant",
        "content": second_completion.choices[0].message.content
    })



    # 두 번째2 요청
    second_completion2 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages + [system_message_first, {
            "role": "user",
            "content": f"""
    2.13.재고관리
    2.14.주문관리
    2.15.가격조사
    2.16.고충처리
    2.17.시장조사
    2.18.등급, 유형별 거래처 관리
    2.19.고객접대
    2.20.정보수집
    2.21.대리점 전략
    2.22.루트 판매

3.영업의 점검과 평가
    3.1.부실채권 관리
    3.2.계수관리
    3.3.그래프의 활용
    3.4.문제해결
    3.5.업적평가
            """
        }]
    )

    # 두 번째 응답을 메시지 배열에 추가
    messages.append({
        "role": "assistant",
        "content": second_completion2.choices[0].message.content
    })



    


    # 첫 번째 및 두 번째 응답 출력
    print("첫 번째 응답:\n", initial_completion.choices[0].message.content)
    first_response_text=initial_completion.choices[0].message.content

    print("두 번째 응답:\n", second_completion.choices[0].message.content)
    second_response_text=second_completion.choices[0].message.content

    print("두 번째 응답2:\n", second_completion2.choices[0].message.content)
    second_response_text2=second_completion2.choices[0].message.content



    total_response_text = first_response_text + \
    "========================================================================================================================================" + \
        second_response_text+ \
    "========================================================================================================================================" + \
        second_response_text2
 

    # 이미지 생성을 위한 프롬프트 정의
    prompt = f"블로그에 쓰일 내용인데, '{content_item}'와 관련된 영업 전략, 고객 만남, 제품 데모 혹은 영업 회의의 모습을 포함한 전문적이고 현대적인 스타일의 이미지를 생성해주세요. 상세하고 현실적인 표현을 원합니다."

    # DALL-E를 사용하여 이미지 생성
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    # 이미지 URL 추출
    image_url = response.data[0].url


    # 이미지 메타데이터를 JSON 파일로 저장
    image_metadata = {
        "image_url": image_url,  # 원격 이미지 URL
    }



    #블로그 태그
    blogtag_response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content": f"{mainKeyword}와 관련된 블로그 내용에서, 특히 '{content_item}'에 초점을 맞춘 영업 전략, 고객 만족, 제품 소개, 신규 시장 개척, 그리고 고객 관계 관리와 같은 주제를 다루고 있습니다. 이와 관련하여, 해당 내용을 잘 반영하면서 독자들의 관심을 끌 수 있는, 검색 최적화에 유용한 키워드 태그 5개를 제안해주세요. 숫자와 설명, '#'은 제외하고, 각 태그를 쉼표(,)로 구분하여 한글로 작성해주세요."}]
    )

    # 응답 텍스트 추출
    tags_response_text = blogtag_response.choices[0].message.content
    tags_array = re.sub(r'[\d#. ]+', '', tags_response_text).split(',')  # 숫자, #, . 제거 후 배열로 변환

    

    #json 파일 에 데이터 넣기
    additional_response = total_response_text
    
    topic="영업"
    category="미분류"
    additional_info.append((topic, category, additional_response, image_metadata, tags_array))

# 파일 저장 경로와 이름 설정
results_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\result\\Sales_Delivery_results.json'

# 지정된 경로에 디렉토리가 없으면 생성
os.makedirs(os.path.dirname(results_file_path), exist_ok=True)

# 결과를 JSON 형식으로 파일에 저장
with open(results_file_path, 'w', encoding='utf-8') as file:
    # JSON 형식으로 변환하여 저장
    json.dump({"additional_info": additional_info}, file, ensure_ascii=False, indent=4)

    print("응답이 Sales_Delivery_results.json 파일에 저장되었습니다.")


# Python 코드 실행이 모두 끝난 후 실행될 부분
node_script_path = "C:/Users/yhc93/OneDrive/바탕 화면/사업문서/마/auto2/openai-env/uproad/Sales_Delivery_uproad.js"
subprocess.run(["node", node_script_path], shell=True)