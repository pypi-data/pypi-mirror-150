from trame_client.ui.core import AbstractLayout
from trame_client.widgets.html import Div
from trame_client.widgets.trame import ServerTemplate
from trame_router.widgets.router import register_route

CHAR_TO_CONVERT = "/-:*"


def path_to_name(path: str):
    name = path
    for specialChar in CHAR_TO_CONVERT:
        name = name.replace(specialChar, "_")
    return name


class RouterViewLayout(AbstractLayout):
    def __init__(self, _app, path, name="default", **kwargs):
        template_name = path_to_name(path)
        register_route(
            _app, name, path, ServerTemplate(trame_app=_app, name=template_name).html
        )
        super().__init__(
            _app,
            Div(**kwargs),
            template_name=template_name,
            **kwargs,
        )
