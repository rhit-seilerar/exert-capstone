from exert.utilities import version as ver

def test_version_from_string():
    version = ver.version_from_string("4.4.100")
    version.x = 4
    version.y = 4
    version.z = 100

def test_version_comparison():
    version1 = ver.Version(4, 4, 100)
    version2 = ver.Version(4, 4, 101)
    version3 = ver.Version(4, 4, 99)
    version4 = ver.Version(4, 3, 101)
    version5 = ver.Version(3, 5, 100)

    assert not ver.compare_version(version1, version2)
    assert ver.compare_version(version1, version3)
    assert ver.compare_version(version1, version4)
    assert ver.compare_version(version1, version5)
