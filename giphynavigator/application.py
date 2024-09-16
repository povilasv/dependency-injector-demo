
from fastapi import FastAPI

from .containers import Container, ConfigurationContainer
from .services import SearchService
from . import containers
from . import handlers
import uvicorn



def create_app() -> FastAPI:
    cfg = ConfigurationContainer()
    container = Container(config=cfg)

    print("Overriding...")
    container.wire(modules=[__name__, containers])

    print("Checking dependencies...")
    container.check_dependencies()
    print("Done")

    app = FastAPI()

    app.container = container

    return app

if __name__ == "__main__":
    app = create_app()
    app.get("/")(handlers.index)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
