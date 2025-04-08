import openai

# 这里填写您在https://yibuapi.com上创建的apikey
api_key = "sk-mh6Bv2MgWgN0g56Hc3wAwzAT54zbd0X7jtBkWoK5muW7XULY"
# 这里填写https://yibuapi.com/v1
base_url = "https://yibuapi.com/v1"
# 这是问题
questions = f"""
生成三个虚构的中文书名及其作者和类型的清单。 
使用以下键以 JSON 格式提供它们：book_id, title, author, genre.
"""


def get_openai_response(question, api_key, base_url):
    try:
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"请求失败: {str(e)}"


if __name__ == "__main__":
    response = get_openai_response(questions, api_key, base_url)
    print(f"回答: {response}\n")
