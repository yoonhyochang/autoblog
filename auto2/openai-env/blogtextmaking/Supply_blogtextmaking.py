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
mainKeyword="마(Dioscorea opposita)와 당화혈색소"

# topics와 categories 리스트의 각 항목에 대해 루프를 돌면서 출력
for content_item in Content_data["Supply_Content"]:
    # 첫 번째 completion 호출
    initial_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
             "content": f"""({content_item}) 내용을 아래방식대로 생산 및 공급망 관리를를를 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.

1. {mainKeyword}의 개념
    1.1. 물자, 정보, 재정 등이 원재료 공급업체, 도매상, 소매상, 소비자로 이동되는 흐름을 통합적으로 관리하는 시스템
    1.2. 공급망 내의 불필요한 낭비 요소를 제거한 최적화된 시스템
    1.3. 고객 가치 창출 및 경쟁 우위 달성이 최종 목표이다.

2. {mainKeyword}의 SCM 주요 흐름 3가지
    2.1. {mainKeyword}의 제품 흐름
        1) {mainKeyword}의 공급자로부터 고객으로의 상품 이동, 물품 반환 또는 A/S 요구
    2.2. {mainKeyword}의 정보 흐름 
        1) 주문 전달과 배송 상황 갱신 등
    2.3. {mainKeyword}의 재정 흐름
        1) 신용 조건, 지불 계획, 위탁 판매, 권리 소유권 합의 등
  """

        }]
    )

    print(f"content_item 내용:\n{content_item}")
    print("content_item 내용:\n", content_item)

    # 첫 번째 응답 확인 및 출력
    first_response_text = initial_completion.choices[0].message.content
    print("첫 번째 응답:\n", first_response_text)




    # 두 번째 completion 호출
    second_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 생산 및 공급망 관리를 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
3. {mainKeyword}의 SCM에 포함되는 사항
    3.1. {mainKeyword}의 경영정보 시스템
    3.2. {mainKeyword}의 공급 및 조달
    3.3. {mainKeyword}의 생산 계획
    3.4. {mainKeyword}의 주문 처리
        1) {mainKeyword}의 현금 흐름
        2) {mainKeyword}의 재고 관리
        3) {mainKeyword}의 창고 관리
        4) {mainKeyword}의 고객 관리
  """
        }]
    )

    # 두 번째 응답 확인 및 출력
    second_response_text = second_completion.choices[0].message.content


    # 세 번째 completion 호출
    Third_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 생산 및 공급망 관리를 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
4. {mainKeyword}의 추진 효과
    4.1. {mainKeyword}의 통합적 정보 시스템 운영
    4.2. {mainKeyword}의 물류비용 및 구매비용 절감
    4.3. {mainKeyword}의 고객만족, 시정 변화에 대한 대응력 강화
    4.4. {mainKeyword}의 생산 효율화
    4.5. {mainKeyword}의 총체적 경쟁 우위
            """
        }]
    )

    # 세번째 응답 확인 및 출력
    Third_response_text = Third_completion.choices[0].message.content


    # 세 번째2 completion 호출
    Third2_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 생산 및 공급망 관리를 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
5. {mainKeyword}의 추진 효과
    5.1. {mainKeyword}의 내재적 기능
        1) 공급자 네트워크에 의해 공급된 원자재 등을 변형시키는 데 사용하는 여러 프로세스
        2) 고객 주문을 실제 생산 작업으로 투입하기 위한 생산 일정계획 수립
    5.2. {mainKeyword}의 외재적 기능
        1) {mainKeyword}의 올바른 공급자의 선정
        2) {mainKeyword}의 공급자와 긴밀한 파트너십 유지
"""
        }]
    )
    # 세 번째 응답 확인 및 출력
    Third2_response_text = Third2_completion.choices[0].message.content


    total_response_text = first_response_text + \
    "========================================================================================================================================" + \
        second_response_text + \
        "========================================================================================================================================" + \
        Third_response_text + \
        "========================================================================================================================================" + \
        Third2_response_text


    print(total_response_text)

    # 이미지 생성을 위한 프롬프트 정의
    prompt = f"블로그에 쓰일 내용인데 ({content_item})이와 생산 및 공급망 관리에 연관하여 이미지 보여줘"

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
        messages=[{"role": "system", "content": f"{mainKeyword}에 대한 블로그 내용인데 ({content_item})에 생산 및 공급망 관리에 관하여 테그 5개를 작성해줘 숫자와 설명 과 #은 제외하고 ,로 구분하여 한글로 작성해줘"}]
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