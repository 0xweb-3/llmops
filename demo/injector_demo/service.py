from injector import inject

from demo.injector_demo.interfaces import A


class B:
    @inject
    def __init__(self, a: A):
        self.a = a

    def prin(self):
        print(self.a.name)
