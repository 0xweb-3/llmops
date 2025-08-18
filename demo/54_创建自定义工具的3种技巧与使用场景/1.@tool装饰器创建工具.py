from langchain_core.tools import tool
from pydantic import BaseModel, Field


class MultiplyInput(BaseModel):
    a: int = Field(description="第一个数字")
    b: int = Field(description="第二个数字")


# 传递参数的方式
@tool("multiply_tool", return_direct=True, args_schema=MultiplyInput)
def multiply2(a: int, b: int) -> int:
    """将传递的两个数字相乘"""
    return a * b


@tool
def multiply(a: int, b: int) -> int:
    """将传递的两个数字相乘"""
    return a * b


if __name__ == '__main__':
    # 打印下该工具的相关信息
    print("名称: ", multiply2.name)
    print("描述: ", multiply2.description)
    print("参数: ", multiply2.args)
    print("直接返回: ", multiply2.return_direct)
