from kubeshift.utils import Utils


def test_sanitizeName():
    assert Utils.sanitizeName("foo/bar") == "foo-bar"
