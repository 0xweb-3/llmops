import sys

from injector import Injector

from demo.injector_demo.modules import AppModule
from demo.injector_demo.service import B


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "DefaultUser"

    injector = Injector([AppModule(name)])
    b = injector.get(B)
    b.prin()


if __name__ == '__main__':
    main()
