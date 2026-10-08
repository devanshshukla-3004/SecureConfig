from secureconfig.checks.linux import ssh_root_login


def test_ssh_root_login_secure(tmp_path, monkeypatch):
    path=tmp_path/"sshd_config"
    path.write_text("PermitRootLogin no\n")
    import secureconfig.checks.linux as linux
    monkeypatch.setattr(linux, "_read", lambda _: (path.read_text(), None))
    assert ssh_root_login().status.value=="PASS"


def test_ssh_root_login_insecure(tmp_path, monkeypatch):
    path=tmp_path/"sshd_config"
    path.write_text("PermitRootLogin yes\n")
    import secureconfig.checks.linux as linux
    monkeypatch.setattr(linux, "_read", lambda _: (path.read_text(), None))
    assert ssh_root_login().status.value=="FAIL"
