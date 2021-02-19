# -*- coding: utf-8 -*-
from jenkins_job_wrecker.cli import get_xml_root
from jenkins_job_wrecker.modules.buildwrappers import (
    prebuildcleanup,
    secretbuildwrapper,
)
import os

fixtures_path = os.path.join(os.path.dirname(__file__), "fixtures", "buildwrappers")


class TestPreBuildCleanup(object):
    def test_basic(self):
        filename = os.path.join(fixtures_path, "prebuildcleanup.xml")
        root = get_xml_root(filename=filename)
        assert root is not None
        parent = []
        prebuildcleanup(root, parent)
        assert len(parent) == 1
        assert "workspace-cleanup" in parent[0]
        jjb_ws_cleanup = parent[0]["workspace-cleanup"]
        assert jjb_ws_cleanup["dirmatch"] is True
        assert jjb_ws_cleanup["disable-deferred-wipeout"] is True
        assert jjb_ws_cleanup["check-parameter"] == "DO_WS_CLEANUP"
        assert jjb_ws_cleanup["external-deletion-command"] == "shred -u %s"

    def test_empty_value(self):
        filename = os.path.join(fixtures_path, "prebuildcleanup_empty_value.xml")
        root = get_xml_root(filename=filename)
        assert root is not None
        parent = []
        prebuildcleanup(root, parent)
        assert len(parent) == 1
        assert "workspace-cleanup" in parent[0]
        jjb_ws_cleanup = parent[0]["workspace-cleanup"]
        assert jjb_ws_cleanup["dirmatch"] is True
        assert jjb_ws_cleanup["disable-deferred-wipeout"] is True
        assert "external-deletion-command" not in jjb_ws_cleanup
        assert "check-parameter" not in jjb_ws_cleanup


class TestAWSBindings(object):
    def test_aws(self):
        filename = os.path.join(fixtures_path, "awsbindings.xml")
        root = get_xml_root(filename=filename)
        assert root is not None
        parent = []
        secretbuildwrapper(root, parent)
        assert len(parent) == 1
        assert "credentials-binding" in parent[0]
        jjb_binding = parent[0]["credentials-binding"][0]["amazon-web-services"]
        assert jjb_binding["credential-id"] == "001"
        assert jjb_binding["access-key"] == "AWS_ACCESS_KEY"
        assert jjb_binding["secret-key"] == "AWS_SECRET_KEY"

class TestSSHKeyBindings(object):
    def test_no_user_passphrase(self):
        filename = os.path.join(fixtures_path, "sshkeybindings-no-user-passphrase.xml")
        root = get_xml_root(filename=filename)
        assert root is not None
        parent = []
        secretbuildwrapper(root, parent)
        assert len(parent) == 1
        assert "credentials-binding" in parent[0]
        jjb_binding = parent[0]["credentials-binding"][0]["ssh-user-private-key"]
        assert jjb_binding["credential-id"] == "ssh-key-backup"
        assert jjb_binding["key-file-variable"] == "BUILD_KEY"
        assert "username-variable" not in jjb_binding
        assert "passphrase-variable" not in jjb_binding

    def test_with_user_passphrase(self):
        filename = os.path.join(fixtures_path, "sshkeybindings-with-user-passphrase.xml")
        root = get_xml_root(filename=filename)
        assert root is not None
        parent = []
        secretbuildwrapper(root, parent)
        assert len(parent) == 1
        assert "credentials-binding" in parent[0]
        jjb_binding = parent[0]["credentials-binding"][0]["ssh-user-private-key"]
        assert jjb_binding["credential-id"] == "ssh-key-backup"
        assert jjb_binding["key-file-variable"] == "BUILD_KEY"
        assert jjb_binding["username-variable"] == "USERNAME"
        assert jjb_binding["passphrase-variable"] == "PASSPHRASE"
