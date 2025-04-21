from _typeshed import Incomplete
from sys import exit as exit
from typing import NamedTuple

logger: Incomplete
VM_DIR: Incomplete

class Image(NamedTuple('Image', [('arch', Incomplete), ('os', Incomplete), ('prompt', Incomplete), ('cdrom', Incomplete), ('snapshot', Incomplete), ('url', Incomplete), ('alternate_urls', Incomplete), ('extra_files', Incomplete), ('qcow', Incomplete), ('default_mem', Incomplete), ('extra_args', Incomplete), ('hashes', Incomplete)])): ...

json_path: Incomplete
images: Incomplete
SUPPORTED_IMAGES: Incomplete
home_dir: Incomplete

class Qcows:
    @staticmethod
    def get_qcow_info(name: Incomplete | None = None): ...
    @staticmethod
    def get_qcow(name: Incomplete | None = None, download: bool = True, _is_tty: bool = True): ...
    @staticmethod
    def get_file(urls, output_path, sha1hash: Incomplete | None = None, do_retry: bool = True, _is_tty: bool = True) -> None: ...
    @staticmethod
    def download_qcow(image_data, output_path, _is_retry: bool = False, _is_tty: bool = True) -> None: ...
    @staticmethod
    def qcow_from_arg(idx: int = 1): ...
    @staticmethod
    def remove_image(target) -> None: ...
