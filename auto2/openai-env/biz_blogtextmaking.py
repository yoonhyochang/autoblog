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
from config import API_KEY

#가상환경 세팅 openai-env\Scripts\activate



# 중복 방지 데이터를 저장하거나 업데이트하는 함수
def update_redundancy_prevention_file(Redundancy_prevention_new_item):
    Redundancy_prevention_file_path = 'Redundancy_prevention.json'
    # 파일에서 기존 데이터를 로드하거나, 기본 데이터 구조를 초기화합니다.
    if os.path.exists(Redundancy_prevention_file_path):
        with open(Redundancy_prevention_file_path, 'r', encoding='utf-8') as file:
            Redundancy_prevention_data = json.load(file)
    else:
        Redundancy_prevention_data = {"Redundancy_prevention": []}

    # 중복 검사: 새 아이템이 기존 데이터에 없는 경우에만 추가
    if Redundancy_prevention_new_item not in Redundancy_prevention_data["Redundancy_prevention"]:
        Redundancy_prevention_data["Redundancy_prevention"].append(Redundancy_prevention_new_item)
        with open(Redundancy_prevention_file_path, 'w', encoding='utf-8') as file:
            json.dump(Redundancy_prevention_data, file, ensure_ascii=False, indent=4)

# 중복 방지 데이터를 파일에서 불러오는 함수
def load_redundancy_prevention_data():
    file_path = 'Redundancy_prevention.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {"Redundancy_prevention": []}

# 중복 방지 데이터 불러오기
Redundancy_prevention_data = load_redundancy_prevention_data()

# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
existing_topics = [item[0] for item in Redundancy_prevention_data.get("Redundancy_prevention", [])]
existing_categories = [item[1] for item in Redundancy_prevention_data.get("Redundancy_prevention", [])]

# 기존 주제와 카테고리를 문자열로 변환
existing_topics_str = ", ".join(existing_topics)
existing_categories_str = ", ".join(existing_categories)






# OpenAI 클라이언트 설정
client = OpenAI(api_key=os.environ.get(f"{API_KEY}"))
# GPT 모델을 사용해 요청 처리


# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
topics = [item[0] for item in Redundancy_prevention_data.get("Redundancy_prevention", [])]
categories = [item[1] for item in Redundancy_prevention_data.get("Redundancy_prevention", [])]




topics_and_categories = []
additional_info = []


# topics와 categories 리스트의 각 항목에 대해 루프를 돌면서 출력
for topic, category in zip(topics, categories):
    print(f"Topic: {topic}, Category: {category}")

    # 첫 번째 completion 호출
    initial_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content": f"사업 관련내용을 작성할건데 카테고리 :{category}와 주제 :{topic} 를 연관지어서 내용을 바탕으로 블로그 내용을 한글로 워드 프레스(SEO 형식)에다 작성 할 것이며, 최대한 길고 창의적으로 작성해주세요. 추가적인 설명은 넣지마."}]
    )
       
    # 첫 번째 응답 확인 및 출력
    first_response_text = initial_completion.choices[0].message.content
    print("첫 번째 응답:\n", first_response_text)


    # 두 번째 completion 호출
    second_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content":  f"{first_response_text}에 대한 본문 내용인데 본문내용은 제외하고 본문마다(소제목) 모두 -보완설명,-예시,-근거,-수익 창출 방법,-추가적인 생각을 양식에 맞춰 작성해주세요. "}]
    )
    # 두 번째 응답 확인 및 출력
    second_response_text = second_completion.choices[0].message.content
    print("두 번째 응답:\n", second_response_text)


    total_response_text = first_response_text + "====================================================================" + second_response_text

    print(total_response_text)

    # 이미지 생성을 위한 프롬프트 정의
    prompt = f"음식 마(Dioscorea polystachya)에서 관련된 카테고리:{category}, 주제:{topic} 에 연관하여 이미지 보여줘"

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
        messages=[{"role": "system", "content": f"사업에 대한 블로그 내용인데 {first_response_text}에 관하여 테그 5개를 작성해줘 숫자와 설명 과 #은 제외하고 ,로 구분하여 한글로 작성해줘"}]
    )

    # 응답 텍스트 추출
    tags_response_text = blogtag_response.choices[0].message.content
    tags_array = re.sub(r'[\d#. ]+', '', tags_response_text).split(',')  # 숫자, #, . 제거 후 배열로 변환

    

    #json 파일 에 데이터 넣기
    additional_response = total_response_text
    
    # additional_info.append((topic, category, additional_response, image_metadata,tags_array, image_metadata2, summary_response_text))

    additional_info.append((topic, category, additional_response, image_metadata,tags_array))

    # 결과를 JSON 형식으로 파일에 저장
    with open('results.json', 'w', encoding='utf-8') as file:
        # JSON 형식으로 변환하여 저장
        json.dump( {"additional_info": additional_info}, file, ensure_ascii=False, indent=4)

    print("응답이 results.json 파일에 저장되었습니다.")

# Python 코드 실행이 모두 끝난 후 실행될 부분
node_script_path = "C:/Users/yhc93/OneDrive/바탕 화면/사업문서/마/auto2/openai-env/biz_uproad.js"
subprocess.run(["node", node_script_path], shell=True)