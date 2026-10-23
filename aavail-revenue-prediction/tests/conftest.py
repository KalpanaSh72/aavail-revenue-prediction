import pytest
@pytest.fixture
def client():
    import app as app_module
    app_module.app.config.update(TESTING=True)
    return app_module.app.test_client()
