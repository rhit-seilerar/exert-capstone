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
    osi.main(header_line=header_line,
             osi_name=osi_name,
             osi_version=osi_version,
             task=task,
             cred=cred,
             mm=mm,
             vma=vma,
             fs=fs,
             qstr=qstr,
             osi_path=osi_path,
             demo_path=demo_path)

    assert os.path.exists(demo_path)
