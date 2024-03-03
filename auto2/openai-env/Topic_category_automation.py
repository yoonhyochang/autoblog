import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import json
import platform
from openai import OpenAI
from config import API_KEY

# JSON 파일 로드 및 저장 함수
def load_data():
    try:
        with open('Redundancy_prevention.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"Redundancy_prevention": []}

def save_data(data):
    with open('Redundancy_prevention.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

#  수정
def update2_redundancy_prevention_file(Redundancy_prevention_new_item):
    Redundancy_prevention_data = load_data()
    if Redundancy_prevention_new_item not in Redundancy_prevention_data["Redundancy_prevention"]:
        Redundancy_prevention_data["Redundancy_prevention"].append(Redundancy_prevention_new_item)
        save_data(Redundancy_prevention_data)

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
  
def call_openai_api(information):
    # OpenAI 클라이언트 설정
    try:
        client = OpenAI(api_key=os.environ.get(f"{API_KEY}"))
        # GPT 모델을 사용해 요청 처리
        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "system", "content": f"{information}에 관련된 카테고리와 주제 10개만 만들어서 분류해줘 양식은 주제(카테고리) 이렇게 해주고 추가적인 설명은 넣지마"}]
        )

        # 응답 텍스트 추출 및 출력
        # 응답 텍스트 추출
        response = completion.choices[0].message.content

        lines = response.split('\n')
        topics_and_categories = []
        print("existing_categories_str :", topics_and_categories)



        for line in lines:
            if '(' in line and ')' in line:
                parts = line.split('(')
                topic_with_number = parts[0].strip()
                category = parts[1].rstrip(')').strip()
                if '. ' in topic_with_number:
                    topic = topic_with_number.split('. ', 1)[1]
                else:
                    topic = topic_with_number
                #topics_and_categories.append((topic, category))
                print("topic :", topic)
                update2_redundancy_prevention_file((topic, category))

    except Exception as e:
        messagebox.showerror("호출 오류", str(e))


# Tkinter GUI 설정
def setup_gui():
    window = tk.Tk()
    window.title("Redundancy Prevention and OpenAI API Caller")

    # 입력 필드
    ttk.Label(window, text="원하는 정보 입력:").pack(padx=10, pady=5)
    information_entry = ttk.Entry(window, width=50)
    information_entry.pack(padx=10, pady=5)

    # 제출 버튼
    def on_submit():
        information = information_entry.get()
        if information:
            call_openai_api(information)
        else:
            messagebox.showwarning("경고", "정보를 입력해주세요.")

    submit_button = ttk.Button(window, text="API 호출", command=on_submit)
    submit_button.pack(padx=10, pady=10)


    # 데이터 관리 프레임
    manage_frame = ttk.Frame(window, padding="10 10 10 10")
    manage_frame.pack(fill=tk.BOTH, expand=True)

    # 스크롤 가능한 체크박스 목록
    canvas = tk.Canvas(manage_frame)
    scrollbar = ttk.Scrollbar(manage_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # 마우스 휠 이벤트 바인딩
    def on_mousewheel(event):
        if platform.system() == "Windows":
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif platform.system() == "Darwin":
            canvas.yview_scroll(int(-1*event.delta), "units")
        else:
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # 체크박스 상태 저장
    checkbox_states = {}

    # 체크박스와 항목 추가
    def update_checkboxes():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        data = load_data()
        for i, item in enumerate(data['Redundancy_prevention']):
            checkbox_states[i] = tk.BooleanVar()
            ttk.Checkbutton(scrollable_frame, text=f"{item[0]} - {item[1]}", variable=checkbox_states[i]).pack()

    # 선택된 항목 일괄 삭제
    def delete_selected():
        data = load_data()
        data['Redundancy_prevention'] = [item for i, item in enumerate(data['Redundancy_prevention']) if not checkbox_states[i].get()]
        save_data(data)
        update_checkboxes()

    # 항목 추가
    def add_item():
        category = simpledialog.askstring("입력", "카테고리 입력:")
        description = simpledialog.askstring("입력", "주제 입력:")
        if category and description:
            update2_redundancy_prevention_file((description, category))
            update_checkboxes()

    # 데이터 관리 버튼
    ttk.Button(manage_frame, text="선택 항목 삭제", command=delete_selected).pack(fill=tk.X, expand=True)
    ttk.Button(manage_frame, text="항목 추가", command=add_item).pack(fill=tk.X, expand=True)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    update_checkboxes()

    window.mainloop()

if __name__ == "__main__":
  setup_gui()