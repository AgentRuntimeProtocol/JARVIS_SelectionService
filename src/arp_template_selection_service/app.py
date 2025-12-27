from __future__ import annotations

from .service import SelectionService
from .utils import auth_settings_from_env_or_dev_insecure


def create_app():
    return SelectionService().create_app(
        title="ARP Template Selection Service",
        auth_settings=auth_settings_from_env_or_dev_insecure(),
    )


app = create_app()

