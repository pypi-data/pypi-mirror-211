# Copyright 2023 TileDB Inc.
# Licensed under the MIT License.

"""Class to render the BioImageViewer."""
import os
from IPython.display import display
from ipywidgets import DOMWidget, register
from typing import Optional
from traitlets import Dict, Unicode
from ._frontend import module_name, module_version

@register
class BioImageViewer(DOMWidget):
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _model_name = Unicode("BioImageViewerModel").tag(sync=True)
    _view_name = Unicode("BioImageViewerView").tag(sync=True)
    value = Dict().tag(sync=True)

class Render:
    def __init__(self, namespace, groupId, token: Optional[str] = None):
        self._value = None

        if token == None:
            token = os.getenv("TILEDB_REST_TOKEN")

        data = {
            "namespace": namespace,
            "groupID": groupId,
            "token": token,
        }

        viewer = BioImageViewer()
        viewer.value = data
        display(viewer)
