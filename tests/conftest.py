import pytest

MOCK_ORIGINAL_URL = "https://probando.com/121323"
MOCK_SHORT_URL = "6b86b273"


@pytest.fixture
def mock_create_short_url_use_case(mocker):
    mocker.patch("src.application.create_short_url.CreateShortUrlUseCase.execute", return_value=MOCK_SHORT_URL)
    return MOCK_SHORT_URL


@pytest.fixture
def mock_get_original_url_use_case(mocker):
    mocker.patch("src.application.get_original_url.GetOriginalUrlUseCase.execute", return_value=MOCK_ORIGINAL_URL)
    return MOCK_ORIGINAL_URL