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
    Content_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\Contentjson\\development_Content.json'
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
    file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\Contentjson\\development_Content.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {"Content": []}

# 중복 방지 데이터 불러오기
Content_data = load_Content_data()

# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
existing_Content = [item for item in Content_data.get("development_Content", [])]

# 기존 주제와 카테고리를 문자열로 변환
existing_topics_str = ", ".join(existing_Content)






# OpenAI 클라이언트 설정
client = OpenAI(api_key=os.environ.get(f"{API_KEY}"))
# GPT 모델을 사용해 요청 처리


# 기존 주제와 카테고리의 전체 목록을 분리하여 준비
content_items = [item for item in Content_data.get("development_Content", [])]




topics_and_categories = []
additional_info = []
mainKeyword="마(Dioscorea opposita)와 당화혈색소"

# topics와 categories 리스트의 각 항목에 대해 루프를 돌면서 출력
for content_item in Content_data["development_Content"]:
    # 첫 번째 completion 호출
    initial_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system", 
             "content": f"""({content_item}) 내용을 아래방식대로 정책자금을 마련할건데 구체적인 해답과 예시를 넣고 추가적인 설명은 넣지마.

1. {mainKeyword}의 제품개발규정
    1.1. {mainKeyword}의 신제품개발규정
        1){mainKeyword}의 적용범위
        2){mainKeyword}의 적용목적
            (1){mainKeyword}의 최종고객
            (2){mainKeyword}의 체인점(총판, 대리점, 가맹점)
            (3){mainKeyword}의 최고경영자
            (4){mainKeyword}의 법적, 사회적 관련 법규 및 규정
            (5){mainKeyword}의 전략상 마케팅 특성
        3){mainKeyword}의 용어 및 정의
            (1){mainKeyword}의 신제품
            (2){mainKeyword}의 시제품
        4){mainKeyword}의 책임과 권한
            (1){mainKeyword}의 대표이사
            (2){mainKeyword}의 상품개발팀장
            (3){mainKeyword}의 개발 담당자
            (4){mainKeyword}의 관련부서
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
2. {mainKeyword}의 신제품 개발 PROCESS
    1.1. {mainKeyword}의 개발 업무 Flow
        1){mainKeyword}의 상품기획
            (1) 각 관련부서장은 소비자 Needs(요구 및 기호도), 제품Trends 및 경쟁사 제품동향 등을 파악한다.
            (2) 전 사원은 신제품 개발에 대한 정보 및 아이디어가 있는 경우 관련부서에 적절한 의사소통 수단을 이용하여 제안한다.
            (3) 상품개발팀은 인터넷 정보검색, 전문 도서 및 잡지, 시장 조사(Market Survey),전시회 참석, 인적 자원을 통한 정보 수집 등을 통하여 신제품 개발 기획 수립에 활용한다.
            (4) 정보 입수 분석 결과는 필요시 시장조사결과보고서에 기록, 유지한다.
        2){mainKeyword}의 개발계획
            (1) 제품 개발 담당자는 상품 기획 정보에 따라 법률적 요건, 공정 및 설비 능력 등을 파악하고 제품개발 계획서 작성하여 팀장의 승인을 득한다.
            (2) 제품 개발 계획서는 생산설비, 개발능력, 포장기술, 유효기간, 자제확보 등을 고려하여 단계별로 제품 개발 계획을 수립한다.
        3) 시제품 생산 및 평가
            (1) 시제품 생산 계획 수립
                ① 제품개발담당자는 개발 계획서에 따라 시제품계획을 수립하고 팀장의 승인을 받는다.
                ② 시제품계획의 수립은 공급자의 공정 및 설비능력을 고려한다.
                ③ 각 사업부문에서 별도로 시제품 제조 의뢰서에 의해 의뢰를 한 경우 시제품계획서를 작성하여 테스트를 한 후 통보한다.
            (2) 시제품 평가/신제품 개발 검토 및 검증
                ① 제품개발담당자는 시제품 생산단계부터 개발 완료 때까지 필요한 검사 및 시험을 실행한다.
                ② 필요한 경우 외부기관에 검사 및 시험을 의뢰할 수 있다.
                ③ 시제품 생산후 모니터 요원을 활용하여 품평설문조사를 실시한다.
                ④ 필요시 특정 계층대상을 지정하여 품평설문조사를 실시할 수 있다.
                ⑤ 품평설문조사 결과는 품평설문조사 결과보고서에 기록, 유지한다.





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
        4) 개발 타당성 검토
            (1) 제품개발 담당자는 배합비에 따라 사전원가계산서를 작성한다.
            (2) 원, 부재료 가격은 구매가격과 업체의 납품 희망가를 근거로 하여 제품의 수율을 적용하여 Kg당 단가를 계산한다
            (3) 제품개발담당자는 파악된 생산설비를 기초로 시제품의 생산 가능성을 검토하고 관련부서와 협의한다.
        5) 시생산 및 검토/검증
            (1) 시생산(Prelaunch Production) 준비
                ① 제품개발담당자는 제조보고서를 관련 공급자로부터 접수하여 관련부서(구매팀 등)에 배포한다.
                ② OEM업체 생산 적용 Test를 행한다.
                ③ 제품개발담당자는 법적 표기사항을 작성하여 포장디자인을 의뢰한다. 
                ④ 제품개발담당자는 디자인 시안을 접수하여 자재소요량, 표기사항 확인 및 포장규격서를 작성하여 관련부서에 통보 후 보관한다.
                ⑤ 개발담당자는 교정된 포장자재의 인쇄상태 및 표기사항을 확인하고 한도 견본을 접수, 관리한다.
            (2) 시생산(Prelaunch Production)
                ① 시제 생산 준비가 완료되면 제품개발담당자는 관련부서 담당자와 공급자를 방문하여 작업표준서에 따라 시생산을 주도한다.
                ② 시생산시 발생한 기록물은 제품개발 완료보고시 활용한다.
            (3) 검토 및 검증
                ① 제품개발담당자는 시생산 후 모니터요원을 활용하여 품평설문조사를 실시한다.
                ② 필요시 특정 계층대상을 지정하여 품평설문조사를 실시할 수 있다.
                ③ 결과는 품평설문조사 결과보고서에 기록, 유지한다.
                ④ 검토 및 검증결과를 참조하여 개발완료보고서를 작성하여, 출시여부를 최종 의사 결정한다.
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
2. {mainKeyword}의 신제품 개발 PROCESS MAP
    2.1. {mainKeyword}의 상품기획
        1){mainKeyword}의 신제품 개발 정보, 아이디어, 시장조사
        2){mainKeyword}의 신제품 개발 기획
        3){mainKeyword}의 관련 양식(기록)
            ① {mainKeyword}의 시장조사결과보고서
            ② {mainKeyword}의 개발계획서
            ③ {mainKeyword}의 시제계획서
            ④ {mainKeyword}의 시제품제조의뢰서
    2.2. {mainKeyword}의 개발계획
        1){mainKeyword}의 신제품 개발 입력
    2.3. {mainKeyword}의 시제 및 평가
        1){mainKeyword}의 계획수립
        2){mainKeyword}의 시제품생산
        3){mainKeyword}의 평가, 검토 검증
        4){mainKeyword}의 관련 양식(기록)
            ⑤ {mainKeyword}의 Pilot실험일지
            ⑥ {mainKeyword}의 품평설문조사결과보고서
            ⑦ {mainKeyword}의 사전원가계산서
            ⑧ {mainKeyword}의 개발완료보고서
    2.4. {mainKeyword}의 타당성 검토
        1){mainKeyword}의 개발 타당성 검토
    2.5. {mainKeyword}의 시 생산 및 검토, 검증
        1){mainKeyword}의 시 생산준비
        2){mainKeyword}의 시 생산
        3){mainKeyword}의 검토 및 검증
        4){mainKeyword}의 관련 표준
            (1) {mainKeyword}의 검사 및 시험규정
            (2) {mainKeyword}의 시정/예방조치규정
            (3) {mainKeyword}의 구매관리규정
            (4) {mainKeyword}의 공급자관리규정
            (5) {mainKeyword}의 고객불만관리규정
            (6) {mainKeyword}의 수입검사지침(품목별)
            (7) {mainKeyword}의 검사 및 시험지침(항목별)
            (8) {mainKeyword}의 고객만족 모니터 규정
            (9) {mainKeyword}의 체인점운영규정
    2.5. {mainKeyword}의 설계변경
        1){mainKeyword}의 핵심성과지표(KPI)
            (1){mainKeyword}의 실적보고(주간,월간,분기,반기,년간)
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
3. {mainKeyword}의 제품공급가격
    3.1 {mainKeyword}의 권장 소비자가
    3.2 {mainKeyword}의 최저 판매가
    3.3 {mainKeyword}의 가맹점
    3.4 {mainKeyword}의 대리점
    3.5 {mainKeyword}의 총판
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
4. {mainKeyword}의 제품현황
    5.1. {mainKeyword}의 제품개요
        1){mainKeyword}의 제품명
        2){mainKeyword}의 제품내용
        3){mainKeyword}의 제품유형
        4){mainKeyword}의 제품특징
        5){mainKeyword}의 원료
        6){mainKeyword}의 섭취또는 사용방법
        """
        }]
    )
    # 세 번째 응답 확인 및 출력
    Third3_response_text = Third3_completion.choices[0].message.content


    # total_response_text = first_response_text 
    
    total_response_text = first_response_text + \
    "========================================================================================================================================" + \
    second_response_text + \
    "========================================================================================================================================" + \
    Third_response_text + \
    "========================================================================================================================================" + \
    Third2_response_text + \
    "========================================================================================================================================" + \
    Third3_response_text


    print(total_response_text)

    # 이미지 생성을 위한 프롬프트 정의
    prompt = f"블로그에 쓰일 내용인데 ({content_item})이와 제품개발 내용과 연관하여 이미지 보여줘"

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
        messages=[{"role": "system", "content": f"{mainKeyword}에 대한 블로그 내용인데 ({content_item})에 제품개발에 관하여 테그 5개를 작성해줘 숫자와 설명 과 #은 제외하고 ,로 구분하여 한글로 작성해줘"}]
    )

    # 응답 텍스트 추출
    tags_response_text = blogtag_response.choices[0].message.content
    tags_array = re.sub(r'[\d#. ]+', '', tags_response_text).split(',')  # 숫자, #, . 제거 후 배열로 변환

    

    #json 파일 에 데이터 넣기
    additional_response = total_response_text
    
    topic="제품개발"
    category="미분류"
    additional_info.append((topic, category, additional_response, image_metadata, tags_array))


# 파일 저장 경로와 이름 설정
results_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\result\\development_results.json'

# 지정된 경로에 디렉토리가 없으면 생성
os.makedirs(os.path.dirname(results_file_path), exist_ok=True)

# 결과를 JSON 형식으로 파일에 저장
with open(results_file_path, 'w', encoding='utf-8') as file:
    # JSON 형식으로 변환하여 저장
    json.dump({"additional_info": additional_info}, file, ensure_ascii=False, indent=4)

    print("응답이 development_results.json 파일에 저장되었습니다.")


# Python 코드 실행이 모두 끝난 후 실행될 부분
node_script_path = "C:/Users/yhc93/OneDrive/바탕 화면/사업문서/마/auto2/openai-env/uproad/development_uproad.js"
subprocess.run(["node", node_script_path], shell=True)