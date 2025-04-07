from injector import Binder, Module

from demo.injector_demo.interfaces import A


class AppModule(Module):
    def __init__(self, name: str):
        self.name = name

    def configure(self, binder: Binder) -> None:
        # 创建带参数带A实例，并绑定
        binder.bind(A, to=A(name="Injected LLMOPS"))
