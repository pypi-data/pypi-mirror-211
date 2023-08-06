from __future__ import annotations

from dataclasses import dataclass

from atoti_core import BaseSessionBound, keyword_only_dataclass

from ._mime_types import LINK_MIME_TYPE


@keyword_only_dataclass
@dataclass(frozen=True)
class Link:
    path: str
    session: BaseSessionBound

    def _repr_mimebundle_(
        self,
        include: object,  # noqa: ARG002
        exclude: object,  # noqa: ARG002
    ) -> dict[str, object]:
        return {
            "text/plain": """Open the notebook in JupyterLab with the Atoti extension enabled to see this link.""",
            LINK_MIME_TYPE: {
                "path": self.path,
                "sessionLocation": self.session._location,
            },
        }


def link(session: BaseSessionBound, /, *, path: str) -> object:
    return Link(path=path.lstrip("/"), session=session)
