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
