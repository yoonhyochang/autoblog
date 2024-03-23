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

# 대화 맥락을 유지하기 위한 메시지 배열 초기화
messages = []

# 시스템 메시지에 전문가 역할과 맥락을 명확화하여 추가
system_message_role = {
    "role": "system",
    "content": "이 대화는 연구개발기획 및 시장조사에 깊이 관여하는 전문가의 관점으로 진행됩니다. 전문가는 신사업 탐색, 신기술 및 신상품 개발, 마케팅 전략 수립 등에서 중요한 역할을 하는 시장조사의 의의와 필요성, 그리고 그 실행 방법에 대한 깊은 이해를 바탕으로, 연구개발기획에 있어 시장조사의 핵심적인 역할을 탐구합니다. 이 과정에서 탐색조사, 기술조사, 인과조사, 정성 및 정량 조사의 유형과 프로세스, 시장조사의 윤리, 문제 진단, 목표 시장 및 고객 선정, 포지셔닝, STP 전략, 시장 현황 파악 방법론, 조사 문제 정의, 조사 기획서 작성 및 실행, 정성적 및 정량적 조사 방법론, 그리고 시장 조사 결과를 통한 전략 수립까지, 시장조사 전 과정에 대한 심도 있는 분석과 전략적 접근 방법을 제공합니다. 또한, 이 전문가는 국내외 시장조사의 복잡성과 특성을 고려한 맞춤형 조사 방법론과 해외시장조사의 문제점 및 사례 분석을 포함하여, 실제 사례를 바탕으로 한 실용적인 조언을 제공합니다."
}
messages.append(system_message_role)  # 전문가 역할을 설명하는 시스템 메시지를 메시지 배열에 추가

# topics와 categories 리스트의 각 항목에 대해 루프를 돌면서 출력
for content_item in content_items:
    # 첫 번째 요청에 대한 시스템 메시지 추가
    system_message_first = {
        "role": "system", 
        "content": f"({content_item}) 내용을 분석하여 B2B 영업 전략, 신규 고객 개발, 가치 제안, 고객 관리 및 서비스 우수성을 포함한 기본과 계획에 대해 논의하고, 영업 전략의 구체적인 예시와 실제 적용 사례를 포함하여 해결 방안을 제시합니다."
    }

    # 첫 번째 요청
    initial_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages + [system_message_first, {
            "role": "user",
             "content": f"""
             아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
1. 연구개발기획에 있어서 시장 조사의 의의
    1.1 시장조사의 의미 및 정의
    1.2 시장조사의 필요성 및 목적
        1) 신사업 탐색
        2) 신기술 개발
        3) 신상품 개발 및 MGPP 전략 수립
        4) 마케팅 전략 수립
            (1) 경쟁 상황
            (2) 컨셉 포지셔닝
            (3) 커뮤니케이션 프로그램으로 차별 아이디어를 강화한다. 
  """

        }]
    )
    # 첫 번째 응답을 메시지 배열에 추가
    messages.append(system_message_first)
    messages.append({
        "role": "assistant",
        "content": initial_completion.choices[0].message.content
    })




    # 두 번째 completion 호출
    second_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""
            아래 목차에 대해 심층적으로 설명하고, 성공적인전략 구축을 위한 실제 예시를 포함해 주세요.
2. 시장조사를 위한 사전 준비
    2.1 시장조사의 유형
        1) 조사목적별 유형
            (1) 탐색조사(exploratory research)
            (2) 기술조사(Descriptive Research)
            (3) 인과조사(Causal Research)
        2) 조사방법별 유형
            (1) 정성조사 (Qualitative research)
            (2) 정량조사(quantitative research)
    2.2 시장조사의 프로세스
        1) 시장 조사 프로젝트 팀 구성
        2) 시장 조사의 지원시스템
    2.3 시장 조사의 윤리
        1) 시장조사에서의 윤리의 중요성
        2) 응답자에 대한 조사자의 윤리
        3) 소비자 조사 보고서 왜곡 

  """
        }]
    )
    # 두 번째 응답을 메시지 배열에 추가
    messages.append({
        "role": "assistant",
        "content": second_completion.choices[0].message.content
    })




    # 세 번째 completion 호출
    Third_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""
            아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
    3.1 문제 진단 및 정의
        1)Consumer Drive
        2)Technology Drive
        3)Industry / Market Drive
    3.2 목표 시장/ 고객 선정과 포지셔닝
        1)STP의 이해
        2)시장 세분화 방법
            (2-1)시장 세분화의 요구사항
            (2-2)시장 세분화 절차
            (2-3)시장 세분화 분류 기준
            (2-4)시장 세분화 작성 자동차 시장 사례
            (2-5)세분 시장별 고객 Needs 분석
    3.3 타겟 시장 선정
        (1)타겟 마케팅의 이해
        (2)타겟 시장의 선택 및 세분화 평가 기준
        (3)타겟 시장 선정을 위한 평가 매트릭스
        (4)타겟 시장 선정을 위한 제품/시장 세분화 매트릭스 작성
        (5)타겟 시장 선정 방법 및 고려사항
    3.4포지셔닝의 이해
        (1)포지셔닝의 개념
        (2)포지셔닝의 종류
    3.5 포지셔닝 전략의 개발 단계
    3.6 STP 전략 사례
        (1)고정관념에서 벗어난 STP 사례
        (2)복수 경쟁상황에서의 효과적인 차별화 사례
        (3)행동을 유도하는 STP 사례"""
        }]
    )

    # 세 번째 응답을 메시지 배열에 추가
    messages.append({
        "role": "assistant",
        "content": Third_completion.choices[0].message.content
    })






    # Third_completion2 호출
    Third_completion2 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""
            아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
    3.3 시장 현황 파악 방법론
        1) 문헌 조사 및 2차 자료 수집 방법
            (1) 자료의 종류와 자료원
        2) 시장 경쟁 구도 및 가치 사슬 분석
            (1) 시장경쟁구조분석(Market Structure Analysis)
            (2) 가치사슬분석
        3) 산업 구조 및 해당 시장 분석
            (1) 산업구조분석의 기본 틀
            (2) 산업구조분석 (Forces at Work)
            (3) Five Forces 개념 설명
            (4) 시장 분석 (Market Analysis)
        4) 포트폴리오 분석, SWOT 분석
            (1) 포트폴리오 분석
            (2) 대표적인 포트폴리오 분석 방법
            (3) SWOT 분석
            (4) 환경분석과 SWOT 분석
            (5) SWOT분석 방법
"""
        }]
    )
    # Third_completion2 응답을 메시지 배열에 추가
    messages.append({
        "role": "assistant",
        "content": Third_completion2.choices[0].message.content
    })




    # Third_completion3 호출
    Third_completion3 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""
            아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
    3.4 시장조사 문제 정의 방법론
        1) QFD (Quality Function Deployment: 품질기능전개법)
            (1) 품질기능전개 (Quality Function Deployment)의 개념
            (2) QFD 진행 절차
        2) 시나리오 분석
            (1) 시나리오(Scenario) 기법의 개념
            (2) 시나리오(Scenario) 기법의 절차
        3) 생활 Scene 전개 방법
            (1) 생활 Scene 전개 방법의 개념
            (2) Scene 전개의 절차
        4) Consumer Needs 정의
            (1) 소비자 Needs와 소비자 만족의 관계
            (2) 소비자 Needs의 심층구조
        5) Trend 조사
            (1) Trend 분석의 절차
            (2) Trend 조사의 사례
"""
        }]
    )
    # Third_completion3 응답을 메시지 배열에 추가
    messages.append({
        "role": "assistant",
        "content": Third_completion3.choices[0].message.content
    })



    # Third_completion4 호출
    Third_completion4 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""
            아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
    3.5 조사 기획서의 작성
        1) 목표 설정
            (1) 개념적 정의(conceptual definition)
            (2) 조작적 정의(operational definition)
        2) 조사 기획서의 작성
            (1) 조사배경 및 목적
            (2) 조사설계
            (3) 실사진행관리
            (4) 조사항목 및 분석방안
            (5) 기타사항
        3) 마케팅 조사 기획서 평가
            (1) 타당성과 신뢰성
            (2) 현실성
"""
        }]
    )
    # Third_completion4 응답을 메시지 배열에 추가
    messages.append({
        "role": "assistant",
        "content": Third_completion4.choices[0].message.content
    })





    # Fourth_completion 호출
    Fourth_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""
            아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
4. 조사 방법론
    4.1 정성적 조사 방법론
        1) 심층면접법
        2) FGD(Focus Group Discussion)
            (1) 세부 진행절차
        3) 관찰조사법
        4) Ethnography
            (1) Ethnography 진행절차
        5) HUT(Home Usage Test)
            (1) HUT (Home Usage Test)의 진행방법
        6) 제품테스트
            (1) 제품 테스트의 목적
            (2) 제품 테스트 유형
            (3) 제품 테스트의 자료수집 방법
"""
        }]
    )
    # Fourth_completion 응답을 메시지 배열에 추가
    messages.append({
        "role": "assistant",
        "content": Fourth_completion.choices[0].message.content
    })






    # Fourth_completion2 호출
    Fourth_completion2 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""
            아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
    4.2 정량적 조사 방법론
        1) Gang Survey
            (1) 갱 서베이의 목적
        2) 설문 조사
            (1) 데이터 수집 계획 수립
            (2) 가설설정
            (3) 설문지 작성
            (4) 분석방법
        3) 온라인 조사
            (1)온라인 설문조사의 특징
            (2) 응답자 선정방법
            (3) 온라인조사의 유의사항
        4) 패널 조사
"""
        }]
    )
    # Fourth_completion2 응답을 메시지 배열에 추가
    messages.append({
        "role": "assistant",
        "content": Fourth_completion2.choices[0].message.content
    })






        # 네 번째3 completion 호출
    Fourth_completion3 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""
            아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
    4.3 새로운 조사 방법론
        1) 기존 시장 조사 기법의 진화
        2) 소비자의 행동을 관찰하는 기법
        3) 소비자의 신체반응을 관찰하는 기법
            (1) 뇌영상 촬영 기법
            (2) Eye Tracking
        4) 소비자의 무의식 세계를 탐사하는 기법
        5)조사기법의 진화
            (1) 정성 조사 기법의 상호보완을 위한 복합 적용
            (2) 정량 조사와 정성 조사의 결합
            (3) 토탈 솔루션으로 진화
"""
        }]
    )
    # Fourth_completion3 응답을 메시지 배열에 추가
    messages.append({
        "role": "assistant",
        "content": Fourth_completion3.choices[0].message.content
    })





    # Five_completion 호출
    Five_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""
            아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
5. 시장 조사 결과를 통한 전략 수립
    5.1 해결방안 도출의 의의
    5.2 개선 방안 도출 기법(Idea 발상법)
        1) 사다리 기법(Laddering)
            (1) 이론적 배경
            (2) 적용사례
        2) KJ법
            (1) KJ법의 장점
            (2) KJ법의 진행과정
        3) 고든법
            (1) 고든법의 특징
            (2) 고든법의 과정
        4) 유추발상법
            (1)특징 및 장단점
            (2) 절차에 따른 적용사례
        5) 특성분류법
            (1) 절차
            (2) 장점과 단점
        6) 친화도법
            (1) 절차
            (2) 장점 및 단점
"""
        }]
    )
    # Five_completion 응답을 메시지 배열에 추가
    messages.append({
        "role": "assistant",
        "content": Five_completion.choices[0].message.content
    })


    # Five_completion2 호출
    Five_completion2 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""
            아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
    5.5 해외 시장 조사 분석 방법론
        1) 해외시장 조사란 ?
        2) 해외시장 조사의 의의
        3) 해외시장 조사의 문제점
            (1) 해외시장 조사의 복수성과 특수성
            (2) 2차 자료의 부족과 낮은 신뢰성
            (3) 1차 자료 수집비용의 증대
            (4) 국가별 조사와 자료수집의 조정문제
            (5) 조사방법의 일반화의 문제
            (6) 조사관리에 관한 문제
            (7) 비용과 기간문제
        4) 조사계획의 수립
            (1) 문제의 규명에 의한 필요정보의 확정
            (2) 정보분석 단위의 결정
            (3) 조사실행상의 문제
            (4) 외부조사기관에 대한 의뢰 여부의 결정
            (5) 조사비용
            (6) 자료수집
        5) 해외시장조사의 내용
"""
        }]
    )
    # Five_completion2 응답을 메시지 배열에 추가
    messages.append({
        "role": "assistant",
        "content": Five_completion2.choices[0].message.content
    })



    # six_completion 호출
    six_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""
            아래 목차에 맞는 영업의 기본과 계획에 대해 심층적으로 설명하고, 성공적인 영업 전략 구축을 위한 실제 예시를 포함해 주세요.
6. 사례 분석
    사례1. 특허기술 가치평가를 위한 시장조사
    사례2. 상장기업 반기보고서 및 투자설명서 작성용 시장전망조사
    사례3. 시장조사분석 전문기관의 절차 및 기법 
"""
        }]
    )
    # six_completion 응답을 메시지 배열에 추가
    messages.append({
        "role": "assistant",
        "content": six_completion.choices[0].message.content
    })





    # total_response_text = initial_completion.choices[0].message.content


    total_response_text = initial_completion.choices[0].message.content+\
        second_completion.choices[0].message.content+\
        Third_completion.choices[0].message.content+\
        Third_completion2.choices[0].message.content+\
        Third_completion3.choices[0].message.content+\
        Third_completion4.choices[0].message.content+\
        Fourth_completion.choices[0].message.content+\
        Fourth_completion2.choices[0].message.content+\
        Fourth_completion3.choices[0].message.content+\
        Five_completion.choices[0].message.content+\
        Five_completion2.choices[0].message.content+\
        six_completion.choices[0].message.content
    
        #     Five2_response_text + \
        # "========================================================================================================================================" + \

    print(total_response_text)

    # 이미지 생성을 위한 프롬프트 정의
    prompt = f"블로그에 쓰일 내용인데 ({content_item})를 분석하여  연구개발기획,시장조사 내용과 연관하여 전문적이고 현대적인 스타일의 이미지를 생성해주세요. 상세하고 현실적인 표현을 원합니다."

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
    
    topic="연구개발기획,시장조사"
    category="미분류"
    additional_info.append((topic, category, additional_response, image_metadata, tags_array))


# 파일 저장 경로와 이름 설정
results_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\result\\market_research_results.json'

# 지정된 경로에 디렉토리가 없으면 생성
os.makedirs(os.path.dirname(results_file_path), exist_ok=True)

# 결과를 JSON 형식으로 파일에 저장
with open(results_file_path, 'w', encoding='utf-8') as file:
    # JSON 형식으로 변환하여 저장
    json.dump({"additional_info": additional_info}, file, ensure_ascii=False, indent=4)

    print("응답이 market_research_results.json 파일에 저장되었습니다.")


# Python 코드 실행이 모두 끝난 후 실행될 부분
node_script_path = "C:/Users/yhc93/OneDrive/바탕 화면/사업문서/마/auto2/openai-env/uproad/mamania_market_research_uproad.js"
subprocess.run(["node", node_script_path], shell=True)