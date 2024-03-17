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
    Content_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\Contentjson\\financing_Content.json'
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
    file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\Contentjson\\financing_Content.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {"Content": []}

# 중복 방지 데이터 불러오기
Content_data = load_Content_data()

# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
existing_Content = [item[0] for item in Content_data.get("financing_Content", [])]

# 기존 주제와 카테고리를 문자열로 변환
existing_topics_str = ", ".join(existing_Content)






# OpenAI 클라이언트 설정
client = OpenAI(api_key=os.environ.get(f"{API_KEY}"))
# GPT 모델을 사용해 요청 처리


# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
content_items = [item for item in Content_data.get("financing_Content", [])]




topics_and_categories = []
additional_info = []
mainKeyword="마(Dioscorea opposita)와 당화혈색소"

# topics와 categories 리스트의 각 항목에 대해 루프를 돌면서 출력
for content_item in Content_data["financing_Content"]:
    # 첫 번째 completion 호출
    initial_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
             "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.

1. {mainKeyword}의 정책자금
    1.1. {mainKeyword}의 융자
        1){mainKeyword}의 중진공
        2){mainKeyword}의 기보
        3){mainKeyword}의 신보・・・
    1.2. {mainKeyword}의 출연
        1){mainKeyword}의 R&D
        2){mainKeyword}의 마케팅
        3){mainKeyword}의 수출
        4){mainKeyword}의 인증・・・
    1.3. {mainKeyword}의 투자
        1){mainKeyword}의 매칭펀드
        2){mainKeyword}의 크라우드펀딩
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
2. {mainKeyword}의 중소기업진흥공단
    1.1. {mainKeyword}의 일반창업기업지원
        1){mainKeyword}의 융자조건
        2){mainKeyword}의 신청유의사항
            (1){mainKeyword}의 자금조달 프로세스 숙지  
            (2){mainKeyword}의 시설 투자의 중소기업진흥공단자금
            (3){mainKeyword}의 청년전용창업자금
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
            "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
2. {mainKeyword}의 기술보증기금
    2.1. {mainKeyword}의 맞춤형 창업성장 분야 우대보증
        1){mainKeyword}의 지식문화창업
        2){mainKeyword}의 이공계챌린저 창업
            (1){mainKeyword}의 기술경력 뿌리창업 
            (2){mainKeyword}의 첨단 성장연계창업
    2.2. {mainKeyword}의 청년창업 특례보증
        1){mainKeyword}의 지식문화창업
        2){mainKeyword}의 이공계챌린저 창업
            (1){mainKeyword}의 기술경력 뿌리창업 
            (2){mainKeyword}의 첨단 성장연계창업
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
            "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
3. {mainKeyword}의 생존을 위한 R&D 지원사업 중요성
    2.1. {mainKeyword}의 상환의무가 없는 정책자금
        1){mainKeyword}의 스타트업 성장의 밑거름
        2){mainKeyword}의 스타트업 내부 R&D 시스템 구축
        3){mainKeyword}의 마케팅에 활용 
    2.2. {mainKeyword}의 창업 스타트업의 R&D 지원사업
        1){mainKeyword}의 창업 선도대학
        2){mainKeyword}의 창업성장 기술개발사업
        2){mainKeyword}의 TIPS기술창업투자
"""
        }]
    )
    # 세 번째 응답 확인 및 출력
    Third2_response_text = Third2_completion.choices[0].message.content



        # 세 번째2 completion 호출
    Third2_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
4. {mainKeyword}의 3종세트 인증을갖춰라
    4.1 {mainKeyword}의 ISO
    4.2 {mainKeyword}의 기업부설연구서
    4.3 {mainKeyword}의 벤처기업 or 이노비즈
"""
        }]
    )
    # 세 번째2 응답 확인 및 출력
    Third2_response_text = Third2_completion.choices[0].message.content




        # 세 번째2 completion 호출
    Third3_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
5. {mainKeyword}의 재무구조를 건전하게 만들자
    5.1. {mainKeyword}의 주요지표
        1){mainKeyword}의 부채비율
        2){mainKeyword}의 매출액증가율
        3){mainKeyword}의 유동비율
        4){mainKeyword}의 매출액영업이익률
        """
        }]
    )
    # 세 번째 응답 확인 및 출력
    Third3_response_text = Third3_completion.choices[0].message.content







        # 네 번째 completion 호출
    Fourth_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
6. {mainKeyword}의 정책자금에 탈락하는 기타요인
    6.1. {mainKeyword}의 경영자의 낮은 신용
    6.2 {mainKeyword}의 부족한 이력과 경력
    6.3 {mainKeyword}의 고급 인력, 기술력 부재
    6.4 {mainKeyword}의 트렌드에 뒤떨어지는 창업아이템
"""
        }]
    )
    # 네 번째 응답 확인 및 출력
    Fourth_response_text = Fourth_completion.choices[0].message.content






        # 네 번째2 completion 호출
    Fourth2_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
7. {mainKeyword}의 창업 자금 정보 제공 사이트
    6.1. {mainKeyword}의 기업마당
    6.2 {mainKeyword}의 K-startup
    6.3 {mainKeyword}의 창업지원센터
    6.4 {mainKeyword}의 중소기업기술정보진흥원
    6.5 (6.1~6.4 말고도 더보여줘)
"""
        }]
    )
    # 네 번째2 응답 확인 및 출력
    Fourth2_response_text = Fourth2_completion.choices[0].message.content






        # 네 번째3 completion 호출
    Fourth3_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
8. {mainKeyword}의 R&D 지원사업 준비(창성과제 기준)
    8.1. {mainKeyword}의 인증취득
    8.2 {mainKeyword}의 선행특허, 연구 검토
    8.3 {mainKeyword}의 연구원 고용 계획
    8.4 {mainKeyword}의 연구비 책정
    8.5 {mainKeyword}의 참여기업 선정
    8.6 {mainKeyword}의 R&D 지원사업 매칭
"""
        }]
    )
    # 네 번째3 응답 확인 및 출력
    Fourth3_response_text = Fourth3_completion.choices[0].message.content






        # 다섯 번째 completion 호출
    Five_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
9. {mainKeyword}의 스타트업 투자 단계
    9.1. {mainKeyword}의 Seed Money
    9.2 {mainKeyword}의 시리즈 A
    9.3 {mainKeyword}의 시리즈 B
    9.4 {mainKeyword}의 시리즈 C

"""
        }]
    )
    # 다섯번째 응답 확인 및 출력
    Five_response_text = Five_completion.choices[0].message.content





        # 다섯 번째 completion 호출
    Five2_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
10. {mainKeyword}의 IR 사업계획서 작성 요령
    10.1. {mainKeyword}의 MILESTONE
        1) {mainKeyword}의 투자자 유치 이후 고려 가능한 EXIT방법은(M&A,IPO 등)
        2) {mainKeyword}의 1년차/2년차/3년차 예상 손익은?
    10.2. {mainKeyword}의 FILANCIAL PROJEVTION
        1) {mainKeyword}의 제품/서비스의 수익원은 무엇인가?
    10.3. {mainKeyword}의 TEAM
        1) {mainKeyword}의 현재 Team Member의 skill과 Experience 제품/서비스 개발에 최적화 되었는가?
    10.4. {mainKeyword}의 DIFFRENTIATION
        1) {mainKeyword}의 거점 시장의 경쟁재/대체재와 차별화되는 우리 제품이 지닌 핵심 Key Offering?(경쟁업체가 지니지 못한 차별화 요소는)
    10.5. {mainKeyword}의 PRODUCT CONCEPT
        1){mainKeyword}의 제품/서비스의 기본 컨셉은 무엇인가?
    10.6. {mainKeyword}의 COMPETITION
        1){mainKeyword}의 거점 시장 내 존재하는 가장 중요한 갱쟁체 또는 대체재는?
    10.6. {mainKeyword}의 WHY NOW/CUSTOMER PAINS
        1){mainKeyword}의 타겟 고객은 누구인가?
        2){mainKeyword}의 왜 그들은 제품/서비스를 필요로 하는가?(타겟 고객의 문제점과 충족되지 않은 니즈는 무엇인가?)
    10.7. {mainKeyword}의 PRODUCT AS A SOLUTION
        1){mainKeyword}의 타겟 고객의 문제점/충족되지 않은 니즈를 해결하기 위해 구체적으로 제품/서비스가 제시하는 원리/방법은 무엇인가?
    10.8. {mainKeyword}의 MARKET
        1){mainKeyword}의 1차 거점 시장은 어디이며, 시장규모는?
        2){mainKeyword}의 확장 가능한 인접시장은 어디이며, 시장규모는?(1차 거점 시장에 주로 Focus)
"""
        }]
    )
    # 다섯번째 응답 확인 및 출력
    Five2_response_text = Five2_completion.choices[0].message.content



    total_response_text = first_response_text + \
    "========================================================================================================================================" + \
        second_response_text + \
        "========================================================================================================================================" + \
        Third_response_text + \
        "========================================================================================================================================" + \
        Third2_response_text + \
        "========================================================================================================================================" + \
        Third3_response_text + \
        "========================================================================================================================================" + \
        Fourth_response_text + \
        "========================================================================================================================================" + \
        Fourth2_response_text + \
        "========================================================================================================================================" + \
        Fourth3_response_text + \
        "========================================================================================================================================" + \
        Five_response_text + \
        "========================================================================================================================================" + \
        Five2_response_text


    print(total_response_text)

    # 이미지 생성을 위한 프롬프트 정의
    prompt = f"블로그에 쓰일 내용인데 ({content_item})이와 자금조달에 연관하여 이미지 보여줘"

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
        messages=[{"role": "system", "content": f"{mainKeyword}에 대한 블로그 내용인데 ({content_item})에 자금조달에 관하여 테그 5개를 작성해줘 숫자와 설명 과 #은 제외하고 ,로 구분하여 한글로 작성해줘"}]
    )

    # 응답 텍스트 추출
    tags_response_text = blogtag_response.choices[0].message.content
    tags_array = re.sub(r'[\d#. ]+', '', tags_response_text).split(',')  # 숫자, #, . 제거 후 배열로 변환

    

    #json 파일 에 데이터 넣기
    additional_response = total_response_text
    
    topic="자금조달"
    category="미분류"
    additional_info.append((topic, category, additional_response, image_metadata, tags_array))


# 파일 저장 경로와 이름 설정
results_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\result\\financing_results.json'

# 지정된 경로에 디렉토리가 없으면 생성
os.makedirs(os.path.dirname(results_file_path), exist_ok=True)

# 결과를 JSON 형식으로 파일에 저장
with open(results_file_path, 'w', encoding='utf-8') as file:
    # JSON 형식으로 변환하여 저장
    json.dump({"additional_info": additional_info}, file, ensure_ascii=False, indent=4)

    print("응답이 financing_results.json 파일에 저장되었습니다.")


# Python 코드 실행이 모두 끝난 후 실행될 부분
node_script_path = "C:/Users/yhc93/OneDrive/바탕 화면/사업문서/마/auto2/openai-env/uproad/financing_uproad.js"
subprocess.run(["node", node_script_path], shell=True)