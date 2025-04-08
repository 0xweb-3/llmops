import dotenv
from injector import Injector

from config import Config
from internal.router import Router
from internal.server.http import Http

injector = Injector()
# 将env加载到环境变量中
dotenv.load_dotenv()

app = Http(__name__, conf=Config(), router=injector.get(Router))

if __name__ == '__main__':
    app.run(port=8080, debug=True)
