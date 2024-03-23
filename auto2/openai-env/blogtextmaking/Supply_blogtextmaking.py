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
    Content_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\Contentjson\\Supply_Content.json'
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
    file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\Contentjson\\Supply_Content.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {"Content": []}

# 중복 방지 데이터 불러오기
Content_data = load_Content_data()

# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
existing_Content = [item[0] for item in Content_data.get("Supply_Content", [])]

# 기존 주제와 카테고리를 문자열로 변환
existing_topics_str = ", ".join(existing_Content)






# OpenAI 클라이언트 설정
client = OpenAI(api_key=os.environ.get(f"{API_KEY}"))
# GPT 모델을 사용해 요청 처리


# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
content_items = [item for item in Content_data.get("Supply_Content", [])]




topics_and_categories = []
additional_info = []
# mainKeyword="마(Dioscorea opposita)와 당화혈색소"

# 대화 맥락을 유지하기 위한 메시지 배열 초기화
messages = []

# 시스템 메시지에 전문가 역할과 맥락을 명확화하여 추가
system_message_role = {
    "role": "system",
    "content": "이 대화는 공급망 관리(SCM)의 모든 측면에 대해 심층적인 지식을 가진 20년 이상의 경력을 가진 전문가가 답변하는 것처럼 진행됩니다. 이 전문가는 공급망의 개념부터 주요 흐름, 포함되는 사항, 추진 효과 및 내/외재적 기능에 이르기까지 광범위한 영역에 걸쳐 실제 경험과 사례 연구를 바탕으로 구체적인 해결 방안, 최적화 전략, 고객 가치 창출 방법을 제시할 준비가 되어 있습니다. 이 전문가는 SCM 시스템의 최적화, 물류비용 및 구매비용 절감 방법, 생산 효율화 및 총체적 경쟁 우위 달성을 위한 전략적 접근법에 대해 논의할 것입니다."
}
messages.append(system_message_role)  # 전문가 역할을 설명하는 시스템 메시지를 메시지 배열에 추가


for content_item in content_items:
    # 첫 번째 요청에 대한 시스템 메시지 추가
    system_message_first = {
        "role": "system", 
        "content": f"({content_item}) 내용을 분석하여 아래 메뉴얼 대해 논의하고, 영업 전략의 구체적인 예시와 실제 적용 사례를 포함하여 해결 방안을 제시합니다."
    }

    # 첫 번째 요청
    initial_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages + [system_message_first, {
            "role": "user",
            "content": f"""
            아래 목차에 대해 심층적으로 설명하고, 성공적인전략 구축을 위한 실제 예시를 포함해 주세요.

1. 개념
    1.1. 물자, 정보, 재정 등이 원재료 공급업체, 도매상, 소매상, 소비자로 이동되는 흐름을 통합적으로 관리하는 시스템
    1.2. 공급망 내의 불필요한 낭비 요소를 제거한 최적화된 시스템
    1.3. 고객 가치 창출 및 경쟁 우위 달성이 최종 목표이다.

2. SCM 주요 흐름 3가지
    2.1. 제품 흐름
        1) 공급자로부터 고객으로의 상품 이동, 물품 반환 또는 A/S 요구
    2.2. 정보 흐름 
        1) 주문 전달과 배송 상황 갱신 등
    2.3. 재정 흐름
        1) 신용 조건, 지불 계획, 위탁 판매, 권리 소유권 합의 등
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
             아래 목차에 대해 심층적으로 설명하고, 성공적인전략 구축을 위한 실제 예시를 포함해 주세요.
3. SCM에 포함되는 사항
    3.1. 경영정보 시스템
    3.2. 공급 및 조달
    3.3. 생산 계획
    3.4. 주문 처리
        1) 현금 흐름
        2) 재고 관리
        3) 창고 관리
        4) 고객 관리
  """
        }]
    )

    # 두 번째 응답을 메시지 배열에 추가
    messages.append({
        "role": "assistant",
        "content": second_completion.choices[0].message.content
    })




    # 세 번째 요청
    second_completion2 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages + [system_message_first, {
            "role": "user",
            "content": f"""
            아래 목차에 대해 심층적으로 설명하고, 성공적인전략 구축을 위한 실제 예시를 포함해 주세요.
            4. 추진 효과
    4.1. 통합적 정보 시스템 운영
    4.2. 물류비용 및 구매비용 절감
    4.3. 고객만족, 시정 변화에 대한 대응력 강화
    4.4. 생산 효율화
    4.5. 총체적 경쟁 우위
            """
        }]
    )

    # 세번째 응답 확인 및 출력
    messages.append({
        "role": "assistant",
        "content": second_completion2.choices[0].message.content
    })



    # 세 번째 요청
    second_completion3 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages + [system_message_first, {
            "role": "user",
            "content": f"""
            아래 목차에 대해 심층적으로 설명하고, 성공적인전략 구축을 위한 실제 예시를 포함해 주세요.
5. 추진 효과
    5.1. 내재적 기능
        1) 공급자 네트워크에 의해 공급된 원자재 등을 변형시키는 데 사용하는 여러 프로세스
        2) 고객 주문을 실제 생산 작업으로 투입하기 위한 생산 일정계획 수립
    5.2. 외재적 기능
        1) 올바른 공급자의 선정
        2) 공급자와 긴밀한 파트너십 유지
"""
        }]
    )
    #  응답 확인 및 출력
    messages.append({
    "role": "assistant",
    "content": second_completion3.choices[0].message.content
    })



    total_response_text = initial_completion.choices[0].message.content+\
        second_completion.choices[0].message.content+\
        second_completion2.choices[0].message.content+\
        second_completion3.choices[0].message.content
    #응답 출력
    print("최종응답:\n", total_response_text)




    # print(total_response_text)

    # 이미지 생성을 위한 프롬프트 정의
    prompt = f"블로그에 쓰일 내용인데 ({content_item})를 분석하여 생산 및 공급망 관리에 연관하여 전문적이고 현대적인 스타일의 이미지를 생성해주세요. 상세하고 현실적인 표현을 원합니다."

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
        messages=[{"role": "system", "content": f"블로그에 쓰일 내용인데 ({content_item})를 분석하여 생산 및 공급망 관리에 같은 주제를 다루고 있습니다. 이와 관련하여 독자들의 관심을 끌 수 있는, 검색 최적화에 유용한 키워드 태그 5개를 제안해주세요. 숫자와 설명, '#'은 제외하고, 각 태그를 쉼표(,)로 구분하여 한글로 작성해주세요."}]
    )

    # 응답 텍스트 추출
    tags_response_text = blogtag_response.choices[0].message.content
    tags_array = re.sub(r'[\d#. ]+', '', tags_response_text).split(',')  # 숫자, #, . 제거 후 배열로 변환

    

    #json 파일 에 데이터 넣기
    additional_response = total_response_text
    
    topic="생산 및 공급망 관리"
    category="미분류"
    additional_info.append((topic, category, additional_response, image_metadata, tags_array))


# 파일 저장 경로와 이름 설정
results_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\result\\Supply_results.json'

# 지정된 경로에 디렉토리가 없으면 생성
os.makedirs(os.path.dirname(results_file_path), exist_ok=True)

# 결과를 JSON 형식으로 파일에 저장
with open(results_file_path, 'w', encoding='utf-8') as file:
    # JSON 형식으로 변환하여 저장
    json.dump({"additional_info": additional_info}, file, ensure_ascii=False, indent=4)

    print("응답이 Supply_results.json 파일에 저장되었습니다.")


# Python 코드 실행이 모두 끝난 후 실행될 부분
node_script_path = "C:/Users/yhc93/OneDrive/바탕 화면/사업문서/마/auto2/openai-env/uproad/Supply_uproad.js"
subprocess.run(["node", node_script_path], shell=True)