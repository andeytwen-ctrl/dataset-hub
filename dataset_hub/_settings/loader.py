from .default_settings import DEFAULT_SETTINGS
from .user_settings import RUNTIME_SETTINGS

def load_settings():
    return {**DEFAULT_SETTINGS, **RUNTIME_SETTINGS}