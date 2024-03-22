import tkinter as tk
from tkinter import scrolledtext, messagebox  # messagebox 임포트
import json
import os
import subprocess
from threading import Thread  # Thread 임포트

def save_to_file():
    content = text_area.get("1.0", tk.END).strip()  # 입력받은 내용을 가져오고 양쪽 공백을 제거
    Content_file_path = 'C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\Contentjson\\Marketing_Content.json'
    
    # 파일이 이미 존재하면 기존 데이터를 로드하고, 존재하지 않으면 새로운 데이터 구조를 생성합니다.
    if os.path.exists(Content_file_path):
        with open(Content_file_path, 'r', encoding='utf-8') as file:
            Content_data = json.load(file)
            Content_data["Marketing_Content"].append(content)  # 기존 내용에 새 내용을 추가
    else:
        Content_data = {"Marketing_Content": [content]}  # 파일이 존재하지 않으면 새 데이터 구조를 생성

    # 변경된 데이터를 파일에 저장합니다.
    with open(Content_file_path, 'w', encoding='utf-8') as file:
        json.dump(Content_data, file, ensure_ascii=False, indent=4)
    
    text_area.delete("1.0", tk.END)  # 저장 후 텍스트 영역을 비웁니다.
    messagebox.showinfo("Saved", "Your input was saved to Marketing_Content.json.")  # 저장 완료 메시지를 표시

def run_script():
    def execute():
        script_path = "C:/Users/yhc93/OneDrive/바탕 화면/사업문서/마/auto2/openai-env/blogtextmaking/Marketing_blogtextmaking.py"
        # subprocess.run을 사용하여 스크립트를 실행. 이제 스크립트 내에서 Marketing_Content.json을 처리합니다.
        subprocess.run(["python", script_path], shell=True)
        messagebox.showinfo("Completed", "Script execution completed.")
    
    # 별도의 스레드에서 스크립트 실행
    Thread(target=execute).start()
# Create the main window
root = tk.Tk()
root.title("Text to JSON and Run Script")
root.geometry("400x680")

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

save_button = tk.Button(root, text="Save to JSON", command=save_to_file)
save_button.pack(pady=5)

run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.pack(pady=5)

root.mainloop()
