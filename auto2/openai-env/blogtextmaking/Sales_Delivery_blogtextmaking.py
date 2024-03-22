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

# topics와 categories 리스트의 각 항목에 대해 루프를 돌면서 출력
for content_item in Content_data["Sales_Delivery_Content"]:
    # 첫 번째 completion 호출
    initial_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
             "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.

1. {mainKeyword}의 영업의 기본과 계획
    1.1. {mainKeyword}의 영업이란
    1.2. {mainKeyword}의 영업의 위치
    1.3. {mainKeyword}의 영업의 철학
    1.4. {mainKeyword}의 영업사원
    1.5. {mainKeyword}의 방문준비
    1.6. {mainKeyword}의 상품지식
    1.7. {mainKeyword}의 판매요점
    1.8. {mainKeyword}의 역할연기
    1.9. {mainKeyword}의 영업 목표 세우기
    1.10. {mainKeyword}의 판매 목표 세우기
    1.11. {mainKeyword}의 판매 목표 나누기
    1.12. {mainKeyword}의 고객만족을 위한 마음가짐
    1.13. {mainKeyword}의 서비스를 위한 마음가짐
    1.14. {mainKeyword}의 마케팅을 위한 마음가짐
    1.15. {mainKeyword}의 판매 지역도
    1.16. {mainKeyword}의 시간관리


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
            "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
2. {mainKeyword}의 영업의 실천과 행동
    2.1. {mainKeyword}의 자기소개
    2.2. {mainKeyword}의 구매심리
    2.3. {mainKeyword}의 판매화법
    2.4. {mainKeyword}의 임기응변
    2.5. {mainKeyword}의 점두판매
    2.6. {mainKeyword}의 매장연출
    2.7. {mainKeyword}의 현장영업
    2.8. {mainKeyword}의 신규개척
    2.9. {mainKeyword}의 판촉관리
    2.10. {mainKeyword}의 영업물류
    2.11. {mainKeyword}의 진열관리
    2.12. {mainKeyword}의 수금관리

  """
        }]
    )

    # 두 번째 응답 확인 및 출력
    second_response_text = second_completion.choices[0].message.content


    # 두 번째 completion2 호출
    second_completion2 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
            d)제품/시장 성장 전략 분석
    2.13. {mainKeyword}의 재고관리
    2.14. {mainKeyword}의 주문관리
    2.15. {mainKeyword}의 가격조사
    2.16. {mainKeyword}의 고충처리
    2.17. {mainKeyword}의 시장조사
    2.18. {mainKeyword}의 등급, 유형별 거래처 관리
    2.19. {mainKeyword}의 고객접대
    2.20. {mainKeyword}의 정보수집
    2.21. {mainKeyword}의 대리점 전략
    2.22. {mainKeyword}의 루트 판매

3. {mainKeyword}의 영업의 점검과 평가
    3.1. {mainKeyword}의 부실채권 관리
    3.2. {mainKeyword}의 계수관리
    3.3. {mainKeyword}의 그래프의 활용
    3.4. {mainKeyword}의 문제해결
    3.5. {mainKeyword}의 업적평가"""
        }]
    )

    # 두 번째 응답 확인 및 출력
    second_response_text2 = second_completion2.choices[0].message.content



 

    total_response_text = first_response_text + \
    "========================================================================================================================================" + \
        second_response_text + \
        "========================================================================================================================================" + \
        second_response_text2


    print(total_response_text)

    # 이미지 생성을 위한 프롬프트 정의
    prompt = f"블로그에 쓰일 내용인데 ({content_item})이와 영업에 연관하여 이미지 보여줘"

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
        messages=[{"role": "system", "content": f"{mainKeyword}에 대한 블로그 내용인데 ({content_item})에 영업에 관하여 테그 5개를 작성해줘 숫자와 설명 과 #은 제외하고 ,로 구분하여 한글로 작성해줘"}]
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