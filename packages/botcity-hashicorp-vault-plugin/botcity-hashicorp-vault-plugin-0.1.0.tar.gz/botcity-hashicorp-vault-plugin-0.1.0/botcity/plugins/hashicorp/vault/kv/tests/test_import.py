def test_package_import():
    import botcity.plugins.hashicorp.vault.kv as plugin
    assert plugin.__file__ != ""
