from src.config.app_factory import create_app
from src.config.settings import Settings

app = create_app(Settings())
