import tkinter as tk
from tkinter import scrolledtext, messagebox  # messagebox 임포트
import json
import os
import subprocess
from threading import Thread  # Thread 임포트

def save_to_file():
    content = text_area.get("1.0", tk.END).strip()  # 입력받은 내용을 가져오고 양쪽 공백을 제거
    Content_file_path = 'Content.json'
    Content_data = {"Content": [content]}  # 새 내용으로 Content_data 초기화

    # 파일에 새 데이터를 저장합니다. 파일이 이미 존재하더라도 내용을 덮어씁니다.
    with open(Content_file_path, 'w', encoding='utf-8') as file:
        json.dump(Content_data, file, ensure_ascii=False, indent=4)
    
    text_area.delete("1.0", tk.END)  # 저장 후 텍스트 영역을 비웁니다.
    messagebox.showinfo("Saved", "Your input was saved to Content.json.")  # 저장 완료 메시지를 표시

def run_script():
    def execute():
        script_path = "C:/Users/yhc93/OneDrive/바탕 화면/사업문서/마/auto2/openai-env/2_blogtextmaking.py"
        subprocess.run(["python", script_path], shell=True)
        messagebox.showinfo("Completed", "Script execution completed.")
    
    # 스크립트 실행을 별도의 스레드에서 수행
    Thread(target=execute).start()

# Create the main window
root = tk.Tk()
root.title("Text to JSON and Run Script")
root.geometry("400x300")

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

save_button = tk.Button(root, text="Save to JSON", command=save_to_file)
save_button.pack(pady=5)

run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.pack(pady=5)

root.mainloop()
