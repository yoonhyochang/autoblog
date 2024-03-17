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
    Content_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\Contentjson\\market_research_Content.json'
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
    file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\Contentjson\\market_research_Content.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {"Content": []}

# 중복 방지 데이터 불러오기
Content_data = load_Content_data()

# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
existing_Content = [item[0] for item in Content_data.get("market_research_Content", [])]

# 기존 주제와 카테고리를 문자열로 변환
existing_topics_str = ", ".join(existing_Content)






# OpenAI 클라이언트 설정
client = OpenAI(api_key=os.environ.get(f"{API_KEY}"))
# GPT 모델을 사용해 요청 처리


# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
content_items = [item for item in Content_data.get("market_research_Content", [])]




topics_and_categories = []
additional_info = []
mainKeyword="마(Dioscorea opposita)와 당화혈색소"

# topics와 categories 리스트의 각 항목에 대해 루프를 돌면서 출력
for content_item in Content_data["market_research_Content"]:
    # 첫 번째 completion 호출
    initial_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 사업계획을 할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
    1.1 {mainKeyword}의 전략 수립안 작성법
        1) {mainKeyword}의 사업계획서
            (1) {mainKeyword}의 사업계획서의 구성
        2) {mainKeyword}의 신상품/기술 Concept
            (1) {mainKeyword}의 컨셉(Concept) 개발
            (2) {mainKeyword}의 고객편익(Customer Benefit)
        3) {mainKeyword}의 마케팅 전략
            (1) {mainKeyword}의 마케팅 믹스전략(4P 전략)
            (2) {mainKeyword}의 가격전략
    1.2 {mainKeyword}의 실행방안 작성 및 평가
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
            "content": f"""({content_item}) 내용을 아래방식대로 사업계획을 할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
    2.1 {mainKeyword}의 신규사업 계획 수립
        1) {mainKeyword}의 운영계획
            (1) {mainKeyword}의 수요예측 및 판매계획
            (2) {mainKeyword}의 생산 및 시설계획
            (3) {mainKeyword}의 조직 및 인력계획
            (4) {mainKeyword}의 기술 및 연구개발계획
            (5) {mainKeyword}의 소요자금 및 조달계획
        2) {mainKeyword}의 마케팅 전략
            (1) {mainKeyword}의 수익 및 추정 재무계획
            (2) {mainKeyword}의 수익 전망
            (3) {mainKeyword}의 손익분기점 분석
            (4) {mainKeyword}의 계획 사업의 경제성 분석(NPV, IRR)
            (5) {mainKeyword}의 민감도 분석
        3) {mainKeyword}의 사업추진일정 수립
            (1) {mainKeyword}의 사업 실행

  """
        }]
    )

    # 두 번째 응답 확인 및 출력
    second_response_text = second_completion.choices[0].message.content


#     # 세 번째 completion 호출
#     Third_completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""({content_item}) 내용을 아래방식대로 사업계획을 할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
#     3.1 {mainKeyword}의 문제 진단 및 정의
#         1){mainKeyword}의 Consumer Drive
#         2){mainKeyword}의 Technology Drive
#         3){mainKeyword}의 Industry / Market Drive
#     3.2 {mainKeyword}의 목표 시장/ 고객 선정과 포지셔닝
#         1){mainKeyword}의 STP의 이해
#         2){mainKeyword}의 시장 세분화 방법
#             (2-1){mainKeyword}의 시장 세분화의 요구사항
#             (2-2){mainKeyword}의 시장 세분화 절차ㅌ
#             (2-3){mainKeyword}의 시장 세분화 분류 기준
#             (2-4){mainKeyword}의 시장 세분화 작성 자동차 시장 사례
#             (2-5){mainKeyword}의 세분 시장별 고객 Needs 분석
#     3.3 {mainKeyword}의 타겟 시장 선정
#         (1){mainKeyword}의 타겟 마케팅의 이해
#         (2){mainKeyword}의 타겟 시장의 선택 및 세분화 평가 기준
#         (3){mainKeyword}의 타겟 시장 선정을 위한 평가 매트릭스
#         (4){mainKeyword}의 타겟 시장 선정을 위한 제품/시장 세분화 매트릭스 작성
#         (5){mainKeyword}의 타겟 시장 선정 방법 및 고려사항
#     3.4{mainKeyword}의 포지셔닝의 이해
#         (1){mainKeyword}의 포지셔닝의 개념
#         (2){mainKeyword}의 포지셔닝의 종류
#     3.5 {mainKeyword}의 포지셔닝 전략의 개발 단계
#     3.6 {mainKeyword}의 STP 전략 사례
#         (1){mainKeyword}의 고정관념에서 벗어난 STP 사례
#         (2){mainKeyword}의 복수 경쟁상황에서의 효과적인 차별화 사례
#         (3){mainKeyword}의 행동을 유도하는 STP 사례"""
#         }]
#     )

#     # 세번째 응답 확인 및 출력
#     Third_response_text = Third_completion.choices[0].message.content


#     # 세 번째2 completion 호출
#     Third2_completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""({content_item}) 내용을 아래방식대로 사업계획을 할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
#     3.3 {mainKeyword}의 시장 현황 파악 방법론
#         1) {mainKeyword}의 문헌 조사 및 2차 자료 수집 방법
#             (1) {mainKeyword}의 자료의 종류와 자료원
#         2) {mainKeyword}의 시장 경쟁 구도 및 가치 사슬 분석
#             (1) {mainKeyword}의 시장경쟁구조분석(Market Structure Analysis)
#             (2) {mainKeyword}의 가치사슬분석
#         3) 산업 구조 및 해당 시장 분석
#             (1) {mainKeyword}의 산업구조분석의 기본 틀
#             (2) {mainKeyword}의 산업구조분석 (Forces at Work)
#             (3) {mainKeyword}의 Five Forces 개념 설명
#             (4) 시장 분석 (Market Analysis)
#         4) {mainKeyword}의 포트폴리오 분석, SWOT 분석
#             (1) {mainKeyword}의 포트폴리오 분석
#             (2) {mainKeyword}의 대표적인 포트폴리오 분석 방법
#             (3) {mainKeyword}의 SWOT 분석
#             (4) {mainKeyword}의 환경분석과 SWOT 분석
#             (5) {mainKeyword}의 SWOT분석 방법
# """
#         }]
#     )
#     # 세 번째 응답 확인 및 출력
#     Third2_response_text = Third2_completion.choices[0].message.content



#         # 세 번째2 completion 호출
#     Third2_completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""({content_item}) 내용을 아래방식대로 사업계획을 할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
#     3.4 {mainKeyword}의 시장조사 문제 정의 방법론
#         1) {mainKeyword}의 QFD (Quality Function Deployment: 품질기능전개법)
#             (1) {mainKeyword}의 품질기능전개 (Quality Function Deployment)의 개념
#             (2) {mainKeyword}의 QFD 진행 절차
#         2) {mainKeyword}의 시나리오 분석
#             (1) {mainKeyword}의 시나리오(Scenario) 기법의 개념
#             (2) {mainKeyword}의 시나리오(Scenario) 기법의 절차
#         3) {mainKeyword}의 생활 Scene 전개 방법
#             (1) {mainKeyword}의 생활 Scene 전개 방법의 개념
#             (2) {mainKeyword}의 Scene 전개의 절차
#         4) {mainKeyword}의 Consumer Needs 정의
#             (1) {mainKeyword}의 소비자 Needs와 소비자 만족의 관계
#             (2) {mainKeyword}의 소비자 Needs의 심층구조
#         5) {mainKeyword}의 Trend 조사
#             (1) {mainKeyword}의 Trend 분석의 절차
#             (2) {mainKeyword}의 Trend 조사의 사례
# """
#         }]
#     )
#     # 세 번째2 응답 확인 및 출력
#     Third2_response_text = Third2_completion.choices[0].message.content




#         # 세 번째2 completion 호출
#     Third3_completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""({content_item}) 내용을 아래방식대로 사업계획을 할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
#     3.5 {mainKeyword}의 조사 기획서의 작성
#         1) {mainKeyword}의 목표 설정
#             (1) {mainKeyword}의 개념적 정의(conceptual definition)
#             (2) {mainKeyword}의 조작적 정의(operational definition)
#         2) {mainKeyword}의 조사 기획서의 작성
#             (1) {mainKeyword}의 조사배경 및 목적
#             (2) {mainKeyword}의 조사설계
#             (3) {mainKeyword}의 실사진행관리
#             (4) {mainKeyword}의 조사항목 및 분석방안
#             (5) {mainKeyword}의 기타사항
#         3) {mainKeyword}의 마케팅 조사 기획서 평가
#             (1) {mainKeyword}의 타당성과 신뢰성
#             (2) {mainKeyword}의 현실성
# """
#         }]
#     )
#     # 세 번째 응답 확인 및 출력
#     Third3_response_text = Third3_completion.choices[0].message.content







#         # 네 번째 completion 호출
#     Fourth_completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""({content_item}) 내용을 아래방식대로 사업계획을 할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
# 4. {mainKeyword}의 조사 방법론
#     4.1 {mainKeyword}의 정성적 조사 방법론
#         1) {mainKeyword}의 심층면접법
#         2) {mainKeyword}의 FGD(Focus Group Discussion)
#             (1) {mainKeyword}의 세부 진행절차
#         3) {mainKeyword}의 관찰조사법
#         4) {mainKeyword}의 Ethnography
#             (1) {mainKeyword}의 Ethnography 진행절차
#         5) {mainKeyword}의 HUT(Home Usage Test)
#             (1) {mainKeyword}의 HUT (Home Usage Test)의 진행방법
#         6) {mainKeyword}의 제품테스트
#             (1) {mainKeyword}의 제품 테스트의 목적
#             (2) {mainKeyword}의 제품 테스트 유형
#             (3) {mainKeyword}의 제품 테스트의 자료수집 방법
# """
#         }]
#     )
#     # 네 번째 응답 확인 및 출력
#     Fourth_response_text = Fourth_completion.choices[0].message.content






#         # 네 번째2 completion 호출
#     Fourth2_completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""({content_item}) 내용을 아래방식대로 사업계획을 할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
#     4.2 {mainKeyword}의 정량적 조사 방법론
#         1) {mainKeyword}의 Gang Survey
#             (1) {mainKeyword}의 갱 서베이의 목적
#         2) {mainKeyword}의 설문 조사
#             (1) {mainKeyword}의 데이터 수집 계획 수립
#             (2) {mainKeyword}의 가설설정
#             (3) {mainKeyword}의 설문지 작성
#             (4) {mainKeyword}의 분석방법
#         3) {mainKeyword}의 온라인 조사
#             (1){mainKeyword}의 온라인 설문조사의 특징
#             (2) {mainKeyword}의 응답자 선정방법
#             (3) {mainKeyword}의 온라인조사의 유의사항
#         4) {mainKeyword}의 패널 조사
# """
#         }]
#     )
#     # 네 번째2 응답 확인 및 출력
#     Fourth2_response_text = Fourth2_completion.choices[0].message.content






#         # 네 번째3 completion 호출
#     Fourth3_completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""({content_item}) 내용을 아래방식대로 사업계획을 할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
#     4.3 {mainKeyword}의 새로운 조사 방법론
#         1) {mainKeyword}의 기존 시장 조사 기법의 진화
#         2) {mainKeyword}의 소비자의 행동을 관찰하는 기법
#         3) {mainKeyword}의 소비자의 신체반응을 관찰하는 기법
#             (1) {mainKeyword}의 뇌영상 촬영 기법
#             (2) {mainKeyword}의 Eye Tracking
#         4) {mainKeyword}의 소비자의 무의식 세계를 탐사하는 기법
#         5){mainKeyword}의 조사기법의 진화
#             (1) {mainKeyword}의 정성 조사 기법의 상호보완을 위한 복합 적용
#             (2) {mainKeyword}의 정량 조사와 정성 조사의 결합
#             (3) {mainKeyword}의 토탈 솔루션으로 진화
# """
#         }]
#     )
#     # 네 번째3 응답 확인 및 출력
#     Fourth3_response_text = Fourth3_completion.choices[0].message.content






#         # 다섯 번째 completion 호출
#     Five_completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""({content_item}) 내용을 아래방식대로 사업계획을 할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
# 5. {mainKeyword}의 시장 조사 결과를 통한 전략 수립
#     5.1 {mainKeyword}의 해결방안 도출의 의의
#     5.2 {mainKeyword}의 개선 방안 도출 기법(Idea 발상법)
#         1) {mainKeyword}의 사다리 기법(Laddering)
#             (1) {mainKeyword}의 이론적 배경
#             (2) {mainKeyword}의 적용사례
#         2) {mainKeyword}의 KJ법
#             (1) {mainKeyword}의 KJ법의 장점
#             (2) {mainKeyword}의 KJ법의 진행과정
#         3) {mainKeyword}의 고든법
#             (1) {mainKeyword}의 고든법의 특징
#             (2) {mainKeyword}의 고든법의 과정
#         4) {mainKeyword}의 유추발상법
#             (1){mainKeyword}의 특징 및 장단점
#             (2) {mainKeyword}의 절차에 따른 적용사례
#         5) {mainKeyword}의 특성분류법
#             (1) {mainKeyword}의 절차
#             (2) {mainKeyword}의 장점과 단점
#         6) {mainKeyword}의 친화도법
#             (1) {mainKeyword}의 절차
#             (2) {mainKeyword}의 장점 및 단점
# """
#         }]
#     )
#     # 다섯번째 응답 확인 및 출력
#     Five_response_text = Five_completion.choices[0].message.content





#         # 다섯 번째 completion 호출
#     Five2_completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""({content_item}) 내용을 아래방식대로 사업계획을 할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
#     5.3 {mainKeyword}의 전략 수립안 작성법
#         1) {mainKeyword}의 사업계획서
#             (1) {mainKeyword}의 사업계획서의 구성
#         2) {mainKeyword}의 신상품/기술 Concept
#             (1) {mainKeyword}의 컨셉(Concept) 개발
#             (2) {mainKeyword}의 고객편익(Customer Benefit)
#         3) {mainKeyword}의 마케팅 전략
#             (1) {mainKeyword}의 마케팅 믹스전략(4P 전략)
#             (2) {mainKeyword}의 가격전략
#     5.4 {mainKeyword}의 실행방안 작성 및 평가
# """
#         }]
#     )
#     # 다섯번째 응답 확인 및 출력
#     Five2_response_text = Five2_completion.choices[0].message.content




#         # 다섯 번째 completion 호출
#     Five3_completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""({content_item}) 내용을 아래방식대로 사업계획을 할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
#     5.5 {mainKeyword}의 해외 시장 조사 분석 방법론
#         1) {mainKeyword}의 해외시장 조사란 ?
#         2) {mainKeyword}의 해외시장 조사의 의의
#         3) {mainKeyword}의 해외시장 조사의 문제점
#             (1) {mainKeyword}의 해외시장 조사의 복수성과 특수성
#             (2) {mainKeyword}의 2차 자료의 부족과 낮은 신뢰성
#             (3) {mainKeyword}의 1차 자료 수집비용의 증대
#             (4) {mainKeyword}의 국가별 조사와 자료수집의 조정문제
#             (5) {mainKeyword}의 조사방법의 일반화의 문제
#             (6) {mainKeyword}의 조사관리에 관한 문제
#             (7) {mainKeyword}의 비용과 기간문제
#         4) {mainKeyword}의 조사계획의 수립
#             (1) {mainKeyword}의 문제의 규명에 의한 필요정보의 확정
#             (2) {mainKeyword}의 정보분석 단위의 결정
#             (3) {mainKeyword}의 조사실행상의 문제
#             (4) {mainKeyword}의 외부조사기관에 대한 의뢰 여부의 결정
#             (5) {mainKeyword}의 조사비용
#             (6) {mainKeyword}의 자료수집
#         5) {mainKeyword}의 해외시장조사의 내용
# """
#         }]
#     )
#     # 다섯번째 응답 확인 및 출력
#     Five3_response_text = Five3_completion.choices[0].message.content




#             # 여섯 번째 completion 호출
#     six_completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         messages=[{
#             "role": "system", 
#             "content": f"""({content_item}) 내용을 아래방식대로 사업계획을 할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
# 6. 사례 분석
#     사례1. {mainKeyword}의 특허기술 가치평가를 위한 시장조사
#     사례2. {mainKeyword}의 상장기업 반기보고서 및 투자설명서 작성용 시장전망조사
#     사례3. {mainKeyword}의 시장조사분석 전문기관의 절차 및 기법 
# """
#         }]
#     )
#     # 여섯번째 응답 확인 및 출력
#     six_response_text = six_completion.choices[0].message.content








    total_response_text = first_response_text + \
    "========================================================================================================================================" + \
        second_response_text
    
        #     Five2_response_text + \
        # "========================================================================================================================================" + \
    #  + \
    #     "========================================================================================================================================" + \
    #     Third_response_text + \
    #     "========================================================================================================================================" + \
    #     Third2_response_text + \
    #     "========================================================================================================================================" + \
    #     Third3_response_text + \
    #     "========================================================================================================================================" + \
    #     Fourth_response_text + \
    #     "========================================================================================================================================" + \
    #     Fourth2_response_text + \
    #     "========================================================================================================================================" + \
    #     Fourth3_response_text + \
    #     "========================================================================================================================================" + \
    #     Five_response_text + \
    #     "========================================================================================================================================" + \
    #     Five3_response_text + \
    #     "========================================================================================================================================" + \
    #     six_response_text

    print(total_response_text)

    # 이미지 생성을 위한 프롬프트 정의
    prompt = f"블로그에 쓰일 내용인데 ({content_item})이와 개발계획 내용과 연관하여 이미지 보여줘"

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
        messages=[{"role": "system", "content": f"{mainKeyword}에 대한 블로그 내용인데 ({content_item})에 개발계획에 관하여 테그 5개를 작성해줘 숫자와 설명 과 #은 제외하고 ,로 구분하여 한글로 작성해줘"}]
    )

    # 응답 텍스트 추출
    tags_response_text = blogtag_response.choices[0].message.content
    tags_array = re.sub(r'[\d#. ]+', '', tags_response_text).split(',')  # 숫자, #, . 제거 후 배열로 변환

    

    #json 파일 에 데이터 넣기
    additional_response = total_response_text
    
    topic="사업계획수립"
    category="미분류"
    additional_info.append((topic, category, additional_response, image_metadata, tags_array))


# 파일 저장 경로와 이름 설정
results_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\result\\business_plan_results.json'

# 지정된 경로에 디렉토리가 없으면 생성
os.makedirs(os.path.dirname(results_file_path), exist_ok=True)

# 결과를 JSON 형식으로 파일에 저장
with open(results_file_path, 'w', encoding='utf-8') as file:
    # JSON 형식으로 변환하여 저장
    json.dump({"additional_info": additional_info}, file, ensure_ascii=False, indent=4)

    print("응답이 business_plan_results.json 파일에 저장되었습니다.")


# Python 코드 실행이 모두 끝난 후 실행될 부분
node_script_path = "C:/Users/yhc93/OneDrive/바탕 화면/사업문서/마/auto2/openai-env/uproad/business_plan_uproad.js"
subprocess.run(["node", node_script_path], shell=True)