# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, scrolledtext
from snownlp import SnowNLP
import datetime

# ============ 1. 题库设计 ============
# 每题包含：题干 + 3 个选项（每个选项带一个"情绪倾向分"，0~1，越低越消极）
QUESTIONS = [
    {
        "q": "1. 最近一周，你早上醒来的第一感觉是？",
        "options": [
            ("充满期待，想快点开始新的一天", 0.9),
            ("还行，没什么特别感觉", 0.55),
            ("不想起床，感觉累", 0.2),
        ],
    },
    {
        "q": "2. 面对突如其来的任务或挑战，你通常？",
        "options": [
            ("兴奋，觉得是机会", 0.85),
            ("有点压力，但能应付", 0.55),
            ("很烦躁，想逃避", 0.15),
        ],
    },
    {
        "q": "3. 和好朋友相处时，你的状态是？",
        "options": [
            ("放松、开心、愿意分享", 0.9),
            ("正常聊天，还行", 0.55),
            ("不想说话，觉得累", 0.2),
        ],
    },
    {
        "q": "4. 晚上睡前，你脑子里想的最多的是？",
        "options": [
            ("今天开心的事，期待明天", 0.85),
            ("日常琐事，很快入睡", 0.55),
            ("烦心事、焦虑、睡不着", 0.15),
        ],
    },
    {
        "q": "5. 用一句话描述你最近的心情：",
        "options": [
            ("阳光、积极、有动力", 0.9),
            ("平淡、安静、还好", 0.55),
            ("低落、烦躁、迷茫", 0.2),
        ],
    },
]

# ============ 2. 情感分析（用 SnowNLP）============
def analyze_free_text(text):
    """对用户自由输入的文字做情感分析，返回 0~1 分数"""
    if not text.strip():
        return 0.5
    try:
        return SnowNLP(text).sentiments
    except Exception:
        return 0.5

# ============ 3. 综合评分 -> 心理倾向 ============
def get_conclusion(score):
    if score >= 0.8:
        return "🌟 阳光乐观型", "你精力充沛、情绪稳定，面对压力有良好的自我调节能力。保持这份心态！", "#2ecc71"
    elif score >= 0.65:
        return "🙂 积极稳定型", "整体状态良好，偶有压力但能自我消化。建议继续保持规律作息。", "#27ae60"
    elif score >= 0.5:
        return "😐 平和均衡型", "情绪较平稳，没有大起大落。可以尝试给自己增加一些小目标和乐趣。", "#f39c12"
    elif score >= 0.35:
        return "😕 轻度压力型", "近期可能有一些压力和困扰，建议找朋友聊聊，或做些运动放松一下。", "#e67e22"
    else:
        return "😢 焦虑低落型", "情绪偏低落，建议多关注自己的心理状态，必要时寻求专业帮助。", "#e74c3c"

# ============ 4. GUI 主程序 ============
class PsychApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI 心理测试问答系统")
        self.root.geometry("720x640")
        self.root.configure(bg="#f5f7fa")

        self.answers = [None] * len(QUESTIONS)   # 记录每题选择的倾向分
        self.option_vars = []                    # Tkinter 变量
        self.current_q = 0                       # 当前题号
        self.free_text = ""                      # 用户的自由描述

        self.build_welcome()

    # ---------- 欢迎页 ----------
    def build_welcome(self):
        self.clear()
        tk.Label(self.root, text="🧠 AI 心理测试问答系统",
                 font=("微软雅黑", 22, "bold"), bg="#f5f7fa", fg="#2c3e50").pack(pady=30)
        tk.Label(self.root, text="基于 NLP 情感分析 · 5 道题 · 约 2 分钟",
                 font=("微软雅黑", 12), bg="#f5f7fa", fg="#7f8c8d").pack(pady=5)

        intro = (
            "本测试通过 5 道情境题 + 一段自由描述，\n"
            "结合自然语言处理（NLP）情感分析，\n"
            "给出你的情绪状态与心理倾向参考。\n\n"
            "⚠️ 结果仅供自我了解，不构成医学诊断。"
        )
        tk.Label(self.root, text=intro, font=("微软雅黑", 12),
                 bg="#ffffff", fg="#34495e", justify="left",
                 padx=20, pady=20, relief="ridge", bd=1).pack(pady=20)

        tk.Button(self.root, text="开始测试 →", font=("微软雅黑", 14, "bold"),
                  bg="#3498db", fg="white", padx=30, pady=10,
                  command=self.start_test).pack(pady=20)

    # ---------- 逐题问答 ----------
    def start_test(self):
        self.answers = [None] * len(QUESTIONS)
        self.option_vars = []
        self.current_q = 0
        self.build_question()

    def build_question(self):
        self.clear()
        q = QUESTIONS[self.current_q]

        # 进度条
        progress = f"第 {self.current_q + 1} / {len(QUESTIONS)} 题"
        tk.Label(self.root, text=progress, font=("微软雅黑", 10),
                 bg="#f5f7fa", fg="#95a5a6").pack(pady=(15, 5))
        tk.Label(self.root, text="━" * int(30 * (self.current_q + 1) / len(QUESTIONS)),
                 font=("微软雅黑", 12), bg="#f5f7fa", fg="#3498db").pack()

        # 题干
        tk.Label(self.root, text=q["q"], font=("微软雅黑", 15, "bold"),
                 bg="#f5f7fa", fg="#2c3e50", wraplength=640,
                 justify="left").pack(pady=20)

        # 选项
        var = tk.IntVar(value=-1)
        self.option_vars.append(var)
        for i, (text, _score) in enumerate(q["options"]):
            tk.Radiobutton(
                self.root, text=text, variable=var, value=i,
                font=("微软雅黑", 12), bg="#ffffff", fg="#34495e",
                activebackground="#ecf0f1", selectcolor="#d6eaf8",
                anchor="w", padx=15, pady=10, width=60,
                relief="ridge", bd=1, highlightthickness=0,
                justify="left", wraplength=600,
            ).pack(pady=6)

        # 按钮
        btn_frame = tk.Frame(self.root, bg="#f5f7fa")
        btn_frame.pack(pady=20)
        if self.current_q > 0:
            tk.Button(btn_frame, text="← 上一题", font=("微软雅黑", 12),
                      bg="#bdc3c7", fg="white", padx=15, pady=6,
                      command=self.prev_question).pack(side="left", padx=5)
        tk.Button(btn_frame, text="下一题 →" if self.current_q < len(QUESTIONS) - 1 else "进入自由描述 →",
                  font=("微软雅黑", 12, "bold"),
                  bg="#3498db", fg="white", padx=20, pady=6,
                  command=self.next_question).pack(side="left", padx=5)

    def prev_question(self):
        self.current_q -= 1
        self.build_question()

    def next_question(self):
        var = self.option_vars[self.current_q]
        if var.get() == -1:
            messagebox.showwarning("提示", "请先选择一个选项")
            return
        self.answers[self.current_q] = QUESTIONS[self.current_q]["options"][var.get()][1]
        self.current_q += 1
        if self.current_q < len(QUESTIONS):
            self.build_question()
        else:
            self.build_free_input()

    # ---------- 自由描述页 ----------
    def build_free_input(self):
        self.clear()
        tk.Label(self.root, text="✍️ 用一句话描述你最近的心情（可留空）",
                 font=("微软雅黑", 15, "bold"),
                 bg="#f5f7fa", fg="#2c3e50").pack(pady=30)
        tk.Label(self.root, text="例如：最近有点累，但还能坚持 / 最近挺开心的 / 感觉迷茫……",
                 font=("微软雅黑", 10), bg="#f5f7fa", fg="#95a5a6").pack()

        self.free_box = scrolledtext.ScrolledText(self.root, width=60, height=6,
                                                   font=("微软雅黑", 12))
        self.free_box.pack(pady=20)

        tk.Button(self.root, text="生成分析报告 →", font=("微软雅黑", 13, "bold"),
                  bg="#27ae60", fg="white", padx=25, pady=10,
                  command=self.show_result).pack(pady=20)

    # ---------- 结果页 ----------
    def show_result(self):
        self.free_text = self.free_box.get("1.0", tk.END).strip()

        # 1) 问卷平均分
        choice_avg = sum(self.answers) / len(self.answers)

        # 2) 自由文本情感分
        text_score = analyze_free_text(self.free_text) if self.free_text else None

        # 3) 综合评分（问卷占 70%，文本占 30%；无文本则纯问卷）
        if text_score is None:
            final_score = choice_avg
        else:
            final_score = choice_avg * 0.7 + text_score * 0.3

        title, desc, color = get_conclusion(final_score)

        self.clear()
        tk.Label(self.root, text="📊 你的心理状态分析报告",
                 font=("微软雅黑", 18, "bold"),
                 bg="#f5f7fa", fg="#2c3e50").pack(pady=20)

        # 结论卡片
        card = tk.Frame(self.root, bg="white", relief="ridge", bd=2)
        card.pack(padx=40, pady=10, fill="x")

        tk.Label(card, text=title, font=("微软雅黑", 20, "bold"),
                 bg="white", fg=color).pack(pady=(20, 5))
        tk.Label(card, text=f"综合情感分：{final_score:.3f}",
                 font=("微软雅黑", 12), bg="white", fg="#7f8c8d").pack()
        tk.Label(card, text=desc, font=("微软雅黑", 12),
                 bg="white", fg="#34495e", wraplength=580,
                 justify="left", padx=20).pack(pady=15)

        # 明细
        detail = (
            f"📝 问卷平均分：{choice_avg:.3f}\n"
            f"💬 文字情感分：{('%.3f' % text_score) if text_score is not None else '未填写'}\n"
            f"🕐 测试时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        tk.Label(self.root, text=detail, font=("微软雅黑", 11),
                 bg="#f5f7fa", fg="#7f8c8d", justify="left").pack(pady=15)

        # 按钮
        btn_frame = tk.Frame(self.root, bg="#f5f7fa")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="重新测试", font=("微软雅黑", 12, "bold"),
                  bg="#3498db", fg="white", padx=20, pady=8,
                  command=self.build_welcome).pack(side="left", padx=8)
        tk.Button(btn_frame, text="保存报告", font=("微软雅黑", 12),
                  bg="#27ae60", fg="white", padx=20, pady=8,
                  command=lambda: self.save_report(final_score, title, desc)).pack(side="left", padx=8)

    def save_report(self, score, title, desc):
        filename = f"心理报告_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("===== AI 心理测试报告 =====\n")
            f.write(f"时间：{datetime.datetime.now()}\n")
            f.write(f"结论：{title}\n")
            f.write(f"综合评分：{score:.3f}\n\n")
            f.write(f"分析：{desc}\n\n")
            for i, (q, ans) in enumerate(zip(QUESTIONS, self.answers)):
                f.write(f"{q['q']}\n   → 得分 {ans}\n")
            if self.free_text:
                f.write(f"\n自由描述：{self.free_text}\n")
        messagebox.showinfo("已保存", f"报告已保存为：\n{filename}")

    # ---------- 工具 ----------
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

# ============ 5. 入口 ============
if __name__ == "__main__":
    root = tk.Tk()
    app = PsychApp(root)
    root.mainloop()