from functools import lru_cache

from atoti_core import BaseSessionBound, Plugin

from ._link import link
from ._visualize import visualize
from ._widget_manager import WIDGET_MANAGER_ATTRIBUTE_NAME, WidgetManager


@lru_cache
def _get_widget_manager() -> WidgetManager:
    return WidgetManager()


class JupyterLab3Plugin(Plugin):
    def init_session(self, session: BaseSessionBound, /) -> None:
        session._link = link
        session._visualize = visualize

        setattr(session, WIDGET_MANAGER_ATTRIBUTE_NAME, _get_widget_manager())
