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
    Content_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\Contentjson\\ItemDiscovery_Content.json'
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
    file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\Contentjson\\ItemDiscovery_Content.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {"Content": []}

# 중복 방지 데이터 불러오기
Content_data = load_Content_data()

# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
existing_Content = [item[0] for item in Content_data.get("ItemDiscovery_Content", [])]

# 기존 주제와 카테고리를 문자열로 변환
existing_topics_str = ", ".join(existing_Content)






# OpenAI 클라이언트 설정
client = OpenAI(api_key=os.environ.get(f"{API_KEY}"))
# GPT 모델을 사용해 요청 처리


# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
content_items = [item for item in Content_data.get("ItemDiscovery_Content", [])]




topics_and_categories = []
additional_info = []
# mainKeyword="마(Dioscorea opposita)와 당화혈색소"

# 대화 맥락을 유지하기 위한 메시지 배열 초기화
messages = []

# 시스템 메시지에 전문가 역할과 맥락을 명확화하여 추가
system_message_role = {
    "role": "system",
    "content": "이 대화는 해당 키워드들을 중심으로 혁신적인 사업 아이디어를 발굴하고, 특정 시장 내에서의 사업화 가능성을 탐색하는 데 초점을 맞춘 창업 전문가와의 상담으로 진행됩니다. 전문가는 시장 분석, 소비자 행동 이해, 기술적 실현 가능성, 비즈니스 모델 혁신 등 다양한 분야에 걸친 깊이 있는 인사이트를 제공합니다. 이를 통해 제시된 키워드를 기반으로 한 창의적이고 실행 가능한 사업 아이디어를 도출하고, 이를 구체화하여 사업 계획으로 발전시킬 수 있는 방향을 제안합니다."
}
messages.append(system_message_role)  # 전문가 역할을 설명하는 시스템 메시지를 메시지 배열에 추가


for content_item in content_items:
    # 첫 번째 요청에 대한 시스템 메시지 추가
    system_message_first = {
        "role": "system", 
        "content": f"({content_item}) 내용을 분석하여 시장 분석, 소비자 행동 이해, 기술적 실현 가능성, 비즈니스 모델 혁신 등 다양한 분야에 걸친 깊이 있는 인사이트의 구체적인 예시와 실제 적용 사례를 포함하여 해결 방안을 제시합니다."
    }

    # 첫 번째 요청
    initial_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages + [system_message_first, {
            "role": "user",
            "content": f"""
사업화계획을 할건데 단계별로 설명해줘 1단계: 시장 조사 및 분석,2단계: 사업 계획 수립,3단계: 자금 조달,4단계: 브랜드 및 제품 개발,5단계: 생산 및 공급망 관리,6단계: 마케팅 전략 수립,7단계: 영업 및 배송
  """

        }]
    )

    # 첫 번째 응답을 메시지 배열에 추가
    messages.append(system_message_first)
    messages.append({
        "role": "assistant",
        "content": initial_completion.choices[0].message.content
    })




    # second_completion 호출
    second_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages + [system_message_first, {
            "role": "user",
            "content": f"""
각단게별로 보완 설명,예시, 근거, 수익 창출방법, 추가적인생각넣어줘
  """
        }]
    )

    # 두 번째 응답을 메시지 배열에 추가
    messages.append({
        "role": "assistant",
        "content": second_completion.choices[0].message.content
    })

#     # Third_completion 호출
#     Third_completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=messages + [system_message_first, {
#             "role": "user",
#             "content": f"""
#             아래 목차에 대해 심층적으로 설명하고, 성공적인전략 구축을 위한 실제 예시를 포함해 주세요.
# 3.  기술보증기금
#     2.1.  맞춤형 창업성장 분야 우대보증
#         1) 지식문화창업
#         2) 이공계챌린저 창업
#             (1) 기술경력 뿌리창업 
#             (2) 첨단 성장연계창업
#     2.2.  청년창업 특례보증
#         1) 지식문화창업
#         2) 이공계챌린저 창업
#             (1) 기술경력 뿌리창업 
#             (2) 첨단 성장연계창업
#             """
#         }]
#     )

#     # Third_completion 응답을 메시지 배열에 추가
#     messages.append({
#         "role": "assistant",
#         "content": Third_completion.choices[0].message.content
#     })





#     # Third_completion2n 호출
#     Third_completion2 = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=messages + [system_message_first, {
#             "role": "user",
#             "content": f"""
#             아래 목차에 대해 심층적으로 설명하고, 성공적인전략 구축을 위한 실제 예시를 포함해 주세요.
# 4.  생존을 위한 R&D 지원사업 중요성
#     2.1.  상환의무가 없는 정책자금
#         1) 스타트업 성장의 밑거름
#         2) 스타트업 내부 R&D 시스템 구축
#         3) 마케팅에 활용 
#     2.2.  창업 스타트업의 R&D 지원사업
#         1) 창업 선도대학
#         2) 창업성장 기술개발사업
#         2) TIPS기술창업투자
# """
#         }]
#     )
#      # Third_completio2 응답을 메시지 배열에 추가
#     messages.append({
#         "role": "assistant",
#         "content": Third_completion2.choices[0].message.content
#     })



#         # Third_completion3 호출
#     Third_completion3 = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=messages + [system_message_first, {
#             "role": "user",
#             "content": f"""
#             아래 목차에 대해 심층적으로 설명하고, 성공적인전략 구축을 위한 실제 예시를 포함해 주세요.
# 5.  3종세트 인증을갖춰라
#     4.1  ISO
#     4.2  기업부설연구서
#     4.3  벤처기업 or 이노비즈
# """
#         }]
#     )
#      # Third_completion3 응답을 메시지 배열에 추가
#     messages.append({
#         "role": "assistant",
#         "content": Third_completion3.choices[0].message.content
#     })




#     # Third_completion4 호출
#     Third_completion4 = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""
#             아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
# 6.  재무구조를 건전하게 만들자
#     5.1.  주요지표
#         1) 부채비율
#         2) 매출액증가율
#         3) 유동비율
#         4) 매출액영업이익률
#         """
#         }]
#     )
#      # Third_completion4 응답을 메시지 배열에 추가
#     messages.append({
#         "role": "assistant",
#         "content": Third_completion4.choices[0].message.content
#     })







#         # 네 번째 completion 호출
#     Fourth_completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""
#             아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
# 7.  정책자금에 탈락하는 기타요인
#     6.1.  경영자의 낮은 신용
#     6.2  부족한 이력과 경력
#     6.3  고급 인력, 기술력 부재
#     6.4  트렌드에 뒤떨어지는 창업아이템
# """
#         }]
#     )
#      # Fourth_completion 응답을 메시지 배열에 추가
#     messages.append({
#         "role": "assistant",
#         "content": Fourth_completion.choices[0].message.content
#     })





#     # Fourth_completion2 호출
#     Fourth_completion2 = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""
#             아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
# 7.  창업 자금 정보 제공 사이트
#     6.1.  기업마당
#     6.2  K-startup
#     6.3  창업지원센터
#     6.4  중소기업기술정보진흥원
#     6.5 (6.1~6.4 말고도 더보여줘)
# """
#         }]
#     )
#      # Fourth_completion2 응답을 메시지 배열에 추가
#     messages.append({
#         "role": "assistant",
#         "content": Fourth_completion2.choices[0].message.content
#     })





#     # Fourth_completion3 호출
#     Fourth_completion3 = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""
#             아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
# 8.  R&D 지원사업 준비(창성과제 기준)
#     8.1.  인증취득
#     8.2  선행특허, 연구 검토
#     8.3  연구원 고용 계획
#     8.4  연구비 책정
#     8.5  참여기업 선정
#     8.6  R&D 지원사업 매칭
# """
#         }]
#     )
#      # Fourth_completion3 응답을 메시지 배열에 추가
#     messages.append({
#         "role": "assistant",
#         "content": Fourth_completion3.choices[0].message.content
#     })





#     # Five_completion 호출
#     Five_completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""
#             아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
# 9.  스타트업 투자 단계
#     9.1.  Seed Money
#     9.2  시리즈 A
#     9.3  시리즈 B
#     9.4  시리즈 C

# """
#         }]
#     )
#      # Five_completion 응답을 메시지 배열에 추가
#     messages.append({
#         "role": "assistant",
#         "content": Five_completion.choices[0].message.content
#     })




#     # Five_completion2 호출
#     Five_completion2 = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""
#             아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
# 10.  IR 사업계획서 작성 요령
#     10.1.  MILESTONE
#         1)  투자자 유치 이후 고려 가능한 EXIT방법은(M&A,IPO 등)
#         2)  1년차/2년차/3년차 예상 손익은?
#     10.2.  FILANCIAL PROJEVTION
#         1)  제품/서비스의 수익원은 무엇인가?
#     10.3.  TEAM
#         1)  현재 Team Member의 skill과 Experience 제품/서비스 개발에 최적화 되었는가?
#     10.4.  DIFFRENTIATION
#         1)  거점 시장의 경쟁재/대체재와 차별화되는 우리 제품이 지닌 핵심 Key Offering?(경쟁업체가 지니지 못한 차별화 요소는)
#     10.5.  PRODUCT CONCEPT
#         1) 제품/서비스의 기본 컨셉은 무엇인가?
#     10.6.  COMPETITION
#         1) 거점 시장 내 존재하는 가장 중요한 갱쟁체 또는 대체재는?
#     10.6.  WHY NOW/CUSTOMER PAINS
#         1) 타겟 고객은 누구인가?
#         2) 왜 그들은 제품/서비스를 필요로 하는가?(타겟 고객의 문제점과 충족되지 않은 니즈는 무엇인가?)
#     10.7.  PRODUCT AS A SOLUTION
#         1) 타겟 고객의 문제점/충족되지 않은 니즈를 해결하기 위해 구체적으로 제품/서비스가 제시하는 원리/방법은 무엇인가?
#     10.8.  MARKET
#         1) 1차 거점 시장은 어디이며, 시장규모는?
#         2) 확장 가능한 인접시장은 어디이며, 시장규모는?(1차 거점 시장에 주로 Focus)
# """
#         }]
#     )
#      # Five_completion 응답을 메시지 배열에 추가
#     messages.append({
#         "role": "assistant",
#         "content": Five_completion2.choices[0].message.content
#     })

    total_response_text = initial_completion.choices[0].message.content+\
        second_completion.choices[0].message.content
    

    # total_response_text = initial_completion.choices[0].message.content+\
    #     second_completion.choices[0].message.content+\
    #     Third_completion.choices[0].message.content+\
    #     Third_completion2.choices[0].message.content+\
    #     Third_completion3.choices[0].message.content+\
    #     Third_completion4.choices[0].message.content+\
    #     Fourth_completion.choices[0].message.content+\
    #     Fourth_completion2.choices[0].message.content+\
    #     Fourth_completion3.choices[0].message.content+\
    #     Five_completion.choices[0].message.content+\
    #     Five_completion2.choices[0].message.content

    print(total_response_text)

    # 이미지 생성을 위한 프롬프트 정의
    prompt = f"블로그에 쓰일 내용인데 ({content_item})를 분석하여  융자, 출연, 투자를 포함한 자금 조달 옵션의 세부사항과 그 접근 방법, 중소기업진흥공단과 기술보증기금을 통한 지원 프로그램, 스타트업의 성장을 촉진하는 R&D 지원의 중요성, 기업 인증과 재무 건전성의 역할, 그리고 트렌드, 경영자 신용, 기술력 및 인력의 중요성을 포함하여, 자금 조달 내용과 연관하여 전문적이고 현대적인 스타일의 이미지를 생성해주세요. 상세하고 현실적인 표현을 원합니다."
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
        messages=[{"role": "system", "content": f"블로그에 쓰일 내용인데 ({content_item})를 분석하여 융자, 출연, 투자를 포함한 자금 조달 옵션의 세부사항과 그 접근 방법, 중소기업진흥공단과 기술보증기금을 통한 지원 프로그램, 스타트업의 성장을 촉진하는 R&D 지원의 중요성, 기업 인증과 재무 건전성의 역할, 그리고 트렌드, 경영자 신용, 기술력 및 인력의 중요성을 포함하여, 자금 조달리에 같은 주제를 다루고 있습니다. 이와 관련하여 독자들의 관심을 끌 수 있는, 검색 최적화에 유용한 키워드 태그 5개를 제안해주세요. 숫자와 설명, '#'은 제외하고, 각 태그를 쉼표(,)로 구분하여 한글로 작성해주세요."}]
    )

    # 응답 텍스트 추출
    tags_response_text = blogtag_response.choices[0].message.content
    tags_array = re.sub(r'[\d#. ]+', '', tags_response_text).split(',')  # 숫자, #, . 제거 후 배열로 변환

    

    #json 파일 에 데이터 넣기
    additional_response = total_response_text
    
    topic="사업계획 수립"
    category="미분류"
    additional_info.append((topic, category, additional_response, image_metadata, tags_array))
    additional_info.append((additional_response))


# 파일 저장 경로와 이름 설정
results_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\result\\ItemDiscovery_results.json'

# 지정된 경로에 디렉토리가 없으면 생성
os.makedirs(os.path.dirname(results_file_path), exist_ok=True)

# 결과를 JSON 형식으로 파일에 저장
with open(results_file_path, 'w', encoding='utf-8') as file:
    # JSON 형식으로 변환하여 저장
    json.dump({"additional_info": additional_info}, file, ensure_ascii=False, indent=4)

    print("응답이 ItemDiscovery_results.json 파일에 저장되었습니다.")


# Python 코드 실행이 모두 끝난 후 실행될 부분
node_script_path = "C:/Users/yhc93/OneDrive/바탕 화면/사업문서/마/auto2/openai-env/uproad/ItemDiscovery_uproad.js"
subprocess.run(["node", node_script_path], shell=True)