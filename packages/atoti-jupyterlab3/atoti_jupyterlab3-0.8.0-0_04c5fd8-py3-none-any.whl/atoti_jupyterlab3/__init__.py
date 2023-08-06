"""Plugin to interactively visualize Atoti sessions in JupyterLab.

This package is required to use :meth:`atoti.Session.visualize` and :meth:`atoti_query.QuerySession.visualize`.
"""


def _jupyter_labextension_paths() -> (  # pyright: ignore[reportUnusedFunction]
    list[dict[str, str]]
):
    """Return the paths used by JupyterLab to load the extension assets."""
    return [{"src": "labextension", "dest": "atoti-jupyterlab3"}]
