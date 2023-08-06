from __future__ import annotations

from typing import Optional

from atoti_core import BaseSessionBound

from ._widget_manager import WIDGET_MANAGER_ATTRIBUTE_NAME, WidgetManager


def visualize(session: BaseSessionBound, /, *, name: Optional[str] = None) -> None:
    widget_manager = getattr(session, WIDGET_MANAGER_ATTRIBUTE_NAME)
    assert isinstance(widget_manager, WidgetManager)
    widget_manager.display_widget(session, name=name)
