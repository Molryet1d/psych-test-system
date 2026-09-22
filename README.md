# AI 心理测试问答系统

基于 NLP 的 AI 心理测试问答系统，通过 5 道情境选择题 + 1 段自由文本，
结合 SnowNLP 情感分析给出综合心理倾向报告。

## 功能
- 5 道情境化选择题
- 自由文本情感分析（SnowNLP）
- 问卷 + 文本加权融合评分
- 5 级心理倾向分类
- 报告导出为 txt

## 环境要求
- Python 3.8+
- 依赖：snownlp

## 安装与运行
pip install snownlp -i https://pypi.tuna.tsinghua.edu.cn/simple
python main.py

## 项目结构
- main.py           主程序
- requirements.txt  依赖清单

## 技术栈
Python + Tkinter + SnowNLP
