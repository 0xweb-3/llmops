import dotenv
from flask_sqlalchemy import SQLAlchemy
from injector import Injector

from config import Config
from internal.router import Router
from internal.server.http import Http
from .modules import ExtensionModule

# 将env加载到环境变量中
dotenv.load_dotenv()

# class ExtensionModule(Module):
#     def configure(self, binder: Binder) -> None:
#         binder.bind(SQLAlchemy, to=db)


# injector = Injector()
injector = Injector([ExtensionModule])

# app = Http(__name__, conf=Config(), db=db, router=injector.get(Router))
app = Http(__name__, conf=Config(), db=injector.get(SQLAlchemy), router=injector.get(Router))

if __name__ == '__main__':
    app.run(port=8080, debug=True)

# python -m app.http.app
