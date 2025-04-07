from injector import Injector

from internal.router import Router
from internal.server.http import Http

injector = Injector()

app = Http(__name__, router=injector.get(Router))

if __name__ == '__main__':
    app.run(port=8080, debug=True)
