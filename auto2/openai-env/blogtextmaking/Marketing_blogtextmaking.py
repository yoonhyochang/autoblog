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
    Content_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\Contentjson\\Marketing_Content.json'
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
    file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\Contentjson\\Marketing_Content.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {"Content": []}

# 중복 방지 데이터 불러오기
Content_data = load_Content_data()

# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
existing_Content = [item[0] for item in Content_data.get("Marketing_Content", [])]

# 기존 주제와 카테고리를 문자열로 변환
existing_topics_str = ", ".join(existing_Content)



# OpenAI 클라이언트 설정
client = OpenAI(api_key=os.environ.get(f"{API_KEY}"))
# GPT 모델을 사용해 요청 처리

# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
content_items = [item for item in Content_data.get("Marketing_Content", [])]

topics_and_categories = []
additional_info = []
mainKeyword="마(Dioscorea opposita)와 당화혈색소"

# topics와 categories 리스트의 각 항목에 대해 루프를 돌면서 출력
for content_item in Content_data["Marketing_Content"]:
    # 첫 번째 completion 호출
    initial_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
             "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.

1. {mainKeyword}의 마케팅 플랜 수립 개요
    1.1. {mainKeyword}의 마케팅 플랜(기획) 이란?
    1.2. {mainKeyword}의 마케팅 플랜(기획서) 작성 절차 개괄
        1) {mainKeyword}의 마케팅 플랜 수행 내용 요약
        2) {mainKeyword}의 서론
        3) {mainKeyword}의 상황 (환경) 분석
            a) {mainKeyword}의 외부 상황
            b) {mainKeyword}의 중립(Neutral) 환경
            c) {mainKeyword}의 경쟁 환경
            d) {mainKeyword}의 자사 상황
        4) {mainKeyword}의 목표시장
        5) {mainKeyword}의 문제와 기회
        6) {mainKeyword}의 마케팅 목적(Objective)과 목표치(Goal)
        7) {mainKeyword}의 마케팅 전략
        8) {mainKeyword}의 마케팅 전술
        9) {mainKeyword}의 재무적 분석
        10) {mainKeyword}의 요약 및 부록
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
2. {mainKeyword}의 마케팅 플랜 수립 매뉴얼
    2.1. {mainKeyword}의 제목 표지와 주요 목차
        1) {mainKeyword}의 제목 표지
        2) {mainKeyword}의 주요 목차
    2.2. {mainKeyword}의 마케팅 목표와 전략 Summary
    2.3. {mainKeyword}의 상황(Situation) 분석
                            -{mainKeyword}의 상황 분석을 위한 기본 체크리스트
        1) {mainKeyword}의 시장/고객 분석
            a) {mainKeyword}의 시장 분석
            b) {mainKeyword}의 고객 분석
            c) {mainKeyword}의 시장 포트폴리오 분석
                a.1){mainKeyword}의 BCG Matrix
                    ○{mainKeyword}의 BCG 매트릭스 작성 예
                    ○{mainKeyword}의 BCG 모형에 따른 SBU전략 유형
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
                d.1){mainKeyword}의 Product/Market Growth Matrix
                    ○ {mainKeyword}의 시장 침투전략 (Market penetration strategy)
                       ({mainKeyword}의 기존 시장에서 기존 제품으로 시장 점유율을 증대 시키는 전략)
                    ○ {mainKeyword}의 제품 개발전략(Product Development Strategy)
                        ({mainKeyword}의 기존 시장의 소비자가 잠재적으로 관심 있는 신제품을 개발하는 전략)
                    ○ {mainKeyword}의 시장 개발전략(Market Development Strategy)
                        ({mainKeyword}의 기존 제품을 가지고 새로운 시장을 발견· 개발하는 전략)
                    ○ {mainKeyword}의 다각화 전략(Diversification Strategy)
                        ({mainKeyword}의 현재의 사업과 직접적인 관련이 없는 다른 분야(새로운 시장)에서 새로운 성장기회를 발견하는 전략)
  """
        }]
    )

    # 두 번째 응답 확인 및 출력
    second_response_text2 = second_completion2.choices[0].message.content



    # 두 번째 completion3 호출
    second_completion3 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
        2) {mainKeyword}의 SWOT(환경) 분석
                        ● {mainKeyword}의 SO 전략(강점-기회전략):시장의 기회를 활용하기 위해 강점을 사용하는 전략
                        ● {mainKeyword}의 ST 전략(강점-위협전략):시장의 위협을 회피하기 위해 강점을 사용하는 전략
                        ● {mainKeyword}의 WO 전략(약점-기회전략):약점을 극복함으로써 시장의 기회를 활용하는 전략
                        ● {mainKeyword}의 WT 전략(약점-위협전략):시장의 위협을 회피하고 약점을 최소화하는 전략
                            - {mainKeyword}의 SWOT analysis를 위한 매트릭스 표 작성 
            a) {mainKeyword}의 외부 환경 분석
                a.1){mainKeyword}의 작성방법
            b) {mainKeyword}의 내부 및 산업 환경 분석
                b.1){mainKeyword}의 작성방법
  """
        }]
    )

    # 두 번째 응답 확인 및 출력
    second_response_text3 = second_completion3.choices[0].message.content




    # 두 번째 completion4 호출
    second_completion4 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
        3) {mainKeyword}의 경쟁 분석
                            [표 3]{mainKeyword}의 경쟁 분석의 주요 비교 항목
        4) {mainKeyword}의 제품/서비스 분석
                            [표 4] {mainKeyword}의 모든 제품/서비스별 현황 분석 표 (작성 예)
        5) {mainKeyword}의 스피드 상황 분석 체크리스트
                            -{mainKeyword}의 모든 제품/서비스별 현황 분석 표 (작성 예)
                            - {mainKeyword}의 경쟁 분석
            a){mainKeyword}의 외부요인
            b){mainKeyword}의 내부요인
            c){mainKeyword}의 내부/외부 요인
                            [표 5] {mainKeyword}의 스피드 상황 분석 체크리스트 1
                            [표 6] {mainKeyword}의 스피드 상황 분석 체크리스트 2
                            [표 7] {mainKeyword}의 스피드 상황 분석 체크리스트 3
"""
        }]
    )

    # 두 번째 응답 확인 및 출력
    second_response_text3 = second_completion3.choices[0].message.content


    # 두 번째 completion4 호출
    second_completion4 = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
    2.4 {mainKeyword}의 마케팅 전략
        1) {mainKeyword}의 마케팅 미션과 재무적 목표
        2) {mainKeyword}의 시장 세분화를 통한 타겟 시장
            a) {mainKeyword}의 시장 세분화의 이해
            b) {mainKeyword}의 시장세분화의 종류
                b.1){mainKeyword}의 경쟁적 좌표에 의한 시장 세분화
                b.2){mainKeyword}의 개개인의 집합으로서의 시장 세분화(인구통계변수, 생활유형변수,라이프스타일, 지리적변수, 개성변수)
                b.3){mainKeyword}의 구매와 사용주체에 의한 시장 세분화(어린이 시장, 주부시장, 가계시장, 조직체 시장으로 세분화)
                b.4) {mainKeyword}의 구매행동 측면에서의 시장 세분화
                b.5){mainKeyword}의 제품 및 시장개발 측면에서의 시장 세분화(제품개념의 확대, 제품이 사용되는 장소와 용도 측면, 시장개발과 시장진입 순서 측면, 제품공간)
                b.6){mainKeyword}의 소비자 선호에 따른 시장 세분화
            c){mainKeyword}의 시장 세분화의 기준( 욕구(needs)와 구매행동이 서로 비슷한 소비자들을 묶어 하나의 집단으로 설정)
                c.1){mainKeyword}의 Four generic dimensions에 의한 분류
                c.2){mainKeyword}의 소비자 시장에서의 변수 분류
                c.3){mainKeyword}의 산업재 시장에서의 변수 분류
  """
        }]
    )

    # 두 번째 응답 확인 및 출력
    second_response_text4 = second_completion4.choices[0].message.content



    # 세 번째 completion 호출
    Third_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
            "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.
            d) {mainKeyword}의 시장 세분화 절차
                d.1) {mainKeyword}의 1단계 : 조사 단계
                d.2) {mainKeyword}의 2단계 : 분석 단계
                d.3) {mainKeyword}의 3단계 : 세부 요약 및 설명 단계
                            [표 8] 자동차 라이프스타일 조사를 통한 세분 시장 도출
            e) {mainKeyword}의 타겟 시장의 선택 및 세분화 평가
                    e.1){mainKeyword}의 시장 매력도 평가
                            [표 9] 시장의 매력도 평가
                    e.2) {mainKeyword}의 세분화 평가를 위한 제품/ 시장 세분화 매트릭스 작성
                            [표 10] 세분화 평가 요소
                    e.3){mainKeyword}의 세분 시장별 고객 니즈 분석(KBF(Key Buying Factors 찾기)
                            [표 11] 고객 니즈 분석 방법
                    ○{mainKeyword}의 고객 니즈 분석 방법(제품 특성/성능,디자인 품질,브랜드 이미지,이용 편리성,서비스 품질/AS,납 기,제품 폭/다양성,유행/패션,신뢰관계,가 격,지불조건)
                    ○{mainKeyword}의 표적시장 선정방법(단일 세분시장 집중,; 제품전문화,선택적 전문화,시장 전문화,전체 시장 확보)
                    ○{mainKeyword}의 표적시장 선택 시 고려사항,기업의 지원 정도,제품의 동질성,제품수명주기,; 시장의 동질성,경쟁자의 마케팅 전략)

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
        3){mainKeyword}의 포지셔닝(Positioning)
            a){mainKeyword}의 포지셔닝의 유형
                a.1){mainKeyword}의 속성에 의한 포지셔닝
                a.2){mainKeyword}의 사용상황에 의한 포지셔닝
                a.3){mainKeyword}의 제품사용자에 의한 포지셔닝
                a.4){mainKeyword}의 가격· 품질에 의한 포지셔닝
                a.5){mainKeyword}의 문화적 심벌에 의한 포지셔닝
            b){mainKeyword}의 포지셔닝 전략의 개발 단계
                b.1) {mainKeyword}의 1단계: 소비자 분석 
                b.2) {mainKeyword}의 2단계: 경쟁자 확인
                b.3) {mainKeyword}의 3단계: 경쟁제품의 포지션 분석
                b.4) {mainKeyword}의 4단계: 각 포지션에서의 차이를 분석
                b.5) {mainKeyword}의 5단계: 자사 제품의 포지션 개발
                b.6) {mainKeyword}의 6단계: 포지셔닝의 확인 및 재포지셔닝 
            c) {mainKeyword}의 포지셔닝 맵 작성 방법
                            [표 12] {mainKeyword}의 자사와 경쟁사의 경쟁우위 비교 (작성 예)
                                [ 참고] {mainKeyword}의 시장세분화와 타겟 시장 결정을 위한 체크리스트
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
        4) {mainKeyword}의 마케팅 믹스 전략
            a) {mainKeyword}의 제품 전략 (P roduct Strategies)
                a.1) {mainKeyword}의 제품 수명주기 전략
                    ○{mainKeyword}의 제품수명주기의 각 단계별 전략 방안
                a.2){mainKeyword}의 제품 라인과 제품 믹스 관리 전략
                    ○{mainKeyword}의 제품 믹스 작성
                    ○{mainKeyword}의 제품군별 상세 분석 작성
                            [표 15] 세탁세제 상품군 상세 분석 (작성 예)
                a.3){mainKeyword}의 전략적 브랜드 관리
                    ○{mainKeyword}의 자사 브랜드 체계 작성
                    ○{mainKeyword}의 브랜드별 분석
                    ○{mainKeyword}의 Brand Positioning Map 작성
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
            b) {mainKeyword}의 가격 전략 (P ricing Strategies)
                b.1){mainKeyword}의 가격의 이해
                b.2){mainKeyword}의 가격 전략의 목표와 종류
                    ○{mainKeyword}의 상대적 고가격 전략 (Skimming Pricing)
                    ○{mainKeyword}의 상대적 저가격 전략 (Penetration Pricing)
                    ○{mainKeyword}의 대등가격전략
                b.3){mainKeyword}의 가격 결정 기준과 방법
                    ○{mainKeyword}의 원가원가기준 가격책정(Cost- based pricing)
                    ○{mainKeyword}의 경쟁기준 가격책정
                    ○{mainKeyword}의 소비자 기준 가격책정
                b.4){mainKeyword}의 가격 정책 일반
                b.5){mainKeyword}의 제품별 가격 정책 분석
                            [참 고] {mainKeyword}의 제품 수명주기에 따른 가격 결정법
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
            c) {mainKeyword}의 프로모션 전략 (P romotion Strategies)
                c.1){mainKeyword}의 프로모션 전략의 이해 및 특징
                            [표 16] {mainKeyword}의 커뮤니케이션 믹스의 특징
                c.2){mainKeyword}의 프로모션 4 요소의 활용 수단
                            [표 17] {mainKeyword}의 프로모션 4요소의 주요 수단
                c.3){mainKeyword}의 프로모션 전략 개괄
                c.4){mainKeyword}의 세부 프로모션 전략
                    ○{mainKeyword}의 광고 전략
                            [표 18] {mainKeyword}의 광고 전략 모델 (그리드 모델)
                            [표 19] {mainKeyword}의 주요매체의 장· 단점
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
                    ○{mainKeyword}의 홍보/PR 전략
                        ● {mainKeyword}의 Media Relations (대언론 PR)
                            [표 20] {mainKeyword}의 매체/보도 전략 작성 시 체크리스트
                        ● {mainKeyword}의 Special Event
                            [표 21] {mainKeyword}의 Special Event 실행 시 체크리스트
                    ○{mainKeyword}의 인적 판매 전략
                    ○{mainKeyword}의 판매 촉진 전략
                            [표 22] {mainKeyword}의 소비자 유형별 판촉전략 및 수단
                    ○{mainKeyword}의 다이렉트 마케팅 전략
                    ○{mainKeyword}의 웹 프로모션 전략
                c.5){mainKeyword}의 제품별 프로모션 전략
                    ○{mainKeyword}의 제품 수명 주기별 프로모션 전략
                            [표 23] {mainKeyword}의 제품 수명주기별 프로모션 전략
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
            d){mainKeyword}의 유통 전략 (P lace Strategies)
                d.1){mainKeyword}의 유통의 개념 및 이해
                d.2){mainKeyword}의 유통경로의 구조
                d.3){mainKeyword}의 유통경로의 전략과 선택
                            [표 24] {mainKeyword}의 유통경로의 전략과 선택
                d.4){mainKeyword}의 유통경로의 갈등에 대한 이해
                d.5){mainKeyword}의 유통 환경의 변화와 신유통업태의 출현
                d.6){mainKeyword}의 유통 경로 설계
            e){mainKeyword}의 마케팅 믹스 전략 종합 점검
                            [표 25] {mainKeyword}의 마케팅 믹스 전략 도출을 위한 체크리스트
        5){mainKeyword}의 마케팅 조사
            a){mainKeyword}의 마케팅 조사 업무 진행 과정
            b){mainKeyword}의 마케팅 조사 기획서 작성법
                            [표 26] 조사 일정표 (작성 예: 간트 차트 형식)
                (a){mainKeyword}의 조사 일정표
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
    2.5{mainKeyword}의 재무적 분석
        1){mainKeyword}의 손익분기점 분석
                            [표 27] {mainKeyword}의 손익분기점 분석을 위한 재무 현황표
        2){mainKeyword}의 수요(판매량) 예측
            a){mainKeyword}의 수요 예측의 이해
            b){mainKeyword}의 수요 예측 실전
                            [표 28] {mainKeyword}의 평균이동법을 이용한 기초자료와 예측치
        3){mainKeyword}의 마케팅 전략과 연계된 비용 예측(5% 이내 정도로 책정하는 것이 보통)
                            [표 29] {mainKeyword}의 마케팅 비용 예산표 (작성 예)
                            [참고] 공헌이익Contribution margin)
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
    2.6{mainKeyword}의 실행 및 보완
        1){mainKeyword}의 마케팅 전략 실행과 통제
                        [표 30] {mainKeyword}의 마케팅 실행 마일스톤 (작성 예)
        2){mainKeyword}의 마케팅 전략 점검 및 평가
                        [표 31] {mainKeyword}의  마케팅 전략 점검 체크리스트 (작성 예)
        3){mainKeyword}의 참고 자료 목록 리스트 및 자료 첨부
"""
        }]
    )
    # 다섯번째 응답 확인 및 출력
    Five2_response_text = Five2_completion.choices[0].message.content



    total_response_text = first_response_text + \
    "========================================================================================================================================" + \
        second_response_text + \
        "========================================================================================================================================" + \
        second_response_text2 + \
        "========================================================================================================================================" + \
        second_response_text3 + \
        "========================================================================================================================================" + \
        second_response_text4 + \
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
results_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\result\\Marketing_results.json'

# 지정된 경로에 디렉토리가 없으면 생성
os.makedirs(os.path.dirname(results_file_path), exist_ok=True)

# 결과를 JSON 형식으로 파일에 저장
with open(results_file_path, 'w', encoding='utf-8') as file:
    # JSON 형식으로 변환하여 저장
    json.dump({"additional_info": additional_info}, file, ensure_ascii=False, indent=4)

    print("응답이 Marketing_results.json 파일에 저장되었습니다.")


# Python 코드 실행이 모두 끝난 후 실행될 부분
node_script_path = "C:/Users/yhc93/OneDrive/바탕 화면/사업문서/마/auto2/openai-env/uproad/Marketing_uproad.js"
subprocess.run(["node", node_script_path], shell=True)