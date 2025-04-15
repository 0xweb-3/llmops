from langchain_core.prompts import PromptTemplate

if __name__ == '__main__':
    prompt = (
            PromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
            + "，让我开心一下"  # +号只能用在提示模版之后
            + "\n使用{language}语言")
    print(prompt.invoke({
        "subject": "程序员",
        "language": "英文"
    }).to_string())
