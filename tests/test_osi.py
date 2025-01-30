import os
from exert.usermode import osi

def test_file_print():
    header_line = osi.HeaderLine()
    osi_name = osi.Name()
    osi_version = osi.Version()
    task = osi.Task()
    cred = osi.Cred()
    mm = osi.MM()
    vma = osi.VMA()
    fs = osi.FS()
    qstr = osi.QSTR()
    osi_path = osi.Path()
    demo_path = "demo_osi.osi"
    osi.main(header_line, osi_name, osi_version, task, cred, mm, vma, fs, qstr, osi_path, demo_path)

    assert os.path.exists(demo_path)
