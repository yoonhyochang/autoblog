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
def update_Content_file(Content_new_item):
    Content_file_path = 'Content.json'
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
    file_path = 'Content.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {"Content": []}

# 중복 방지 데이터 불러오기
Content_data = load_Content_data()

# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
existing_Content = [item[0] for item in Content_data.get("Content", [])]

# 기존 주제와 카테고리를 문자열로 변환
existing_topics_str = ", ".join(existing_Content)






# OpenAI 클라이언트 설정
client = OpenAI(api_key=os.environ.get(f"{API_KEY}"))
# GPT 모델을 사용해 요청 처리


# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
content_items = [item for item in Content_data.get("Content", [])]




topics_and_categories = []
additional_info = []


# topics와 categories 리스트의 각 항목에 대해 루프를 돌면서 출력
for content_item in content_items:
    print(f"Content: {content_item}")

    # 첫 번째 completion 호출
    initial_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content": f"온리팬스 사업 본격적으로 시작 할려고 구체화 할려고 하는데 너가 사업을 한다고 생각하고 또 아래에 대한 블로그 내용인데 블로그내용: 일부분: ({content_items}) 이거를 블로그 내용을 한글로 워드 프레스(SEO 형식)에다 새롭게 작성 할 것이며, 최대한 길고 창의적으로 작성해주세요. 추가적인 설명은 넣지마."}]
    )



    # 첫 번째 응답 확인 및 출력
    first_response_text = initial_completion.choices[0].message.content
    print("첫 번째 응답:\n", first_response_text)


    # 두 번째 completion 호출
    second_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content":  f"{first_response_text}에 대한 본문 내용인데 실제로 적용 한 예제와 내용을 똑같이 따라해서 바로 적용할 수있게 해줘 또 소비자 입장에서 느끼는점과 문제점들 알려줘 "}]
    )


    # 두 번째 응답 확인 및 출력
    second_response_text = second_completion.choices[0].message.content
    print("두 번째 응답:\n", second_response_text)


    total_response_text = first_response_text + "====================================================================" + second_response_text

    print(total_response_text)

    # 이미지 생성을 위한 프롬프트 정의
    prompt = f"블로그에 쓰일 내용인데 ({content_item})이와 연관하여 이미지 보여줘"

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
        messages=[{"role": "system", "content": f"사업 본격적으로 시작 할려고 구체화 할려고 하는데 너가 사업을 한다고 생각하고 또 아래에 대한 블로그 내용인데 블로그내용: 일부분: ({first_response_text}) 에 관하여 테그 5개를 작성해줘 숫자와 설명 과 #은 제외하고 ,로 구분하여 한글로 작성해줘"}]
    )

    # 응답 텍스트 추출
    tags_response_text = blogtag_response.choices[0].message.content
    tags_array = re.sub(r'[\d#. ]+', '', tags_response_text).split(',')  # 숫자, #, . 제거 후 배열로 변환

    

    #json 파일 에 데이터 넣기
    additional_response = total_response_text
    
    topic="2차보완"
    category="미분류"
    additional_info.append((topic, category, additional_response, image_metadata,tags_array))

    # 결과를 JSON 형식으로 파일에 저장
    with open('results.json', 'w', encoding='utf-8') as file:
        # JSON 형식으로 변환하여 저장
        json.dump( {"additional_info": additional_info}, file, ensure_ascii=False, indent=4)

    print("응답이 results.json 파일에 저장되었습니다.")

# Python 코드 실행이 모두 끝난 후 실행될 부분
node_script_path = "C:/Users/yhc93/OneDrive/바탕 화면/사업문서/마/auto2/openai-env/biz_uproad.js"
subprocess.run(["node", node_script_path], shell=True)