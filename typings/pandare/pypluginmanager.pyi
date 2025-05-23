from pandare import PyPlugin as PyPlugin
from typing import Any

class PyPluginManager:
    def enable_flask(self, host: str = '127.0.0.1', port: int = 8080) -> None: ...
    def serve(self) -> None: ...
    def load(self, pluginclasses: type[PyPlugin], args: (dict[str, Any] | None) = None, template_dir: (str | None) = None) -> None: ...
