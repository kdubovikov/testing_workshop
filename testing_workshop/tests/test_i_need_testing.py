import pytest
from ..i_need_testing import get_random_quote, construct_meme_url, generate_meme, save_meme, create_meme

@pytest.mark.meme_tests
def test_get_random_qote(quote, mocker):
    # setup data
    requests_get_path = mocker.patch("testing_workshop.i_need_testing.requests")
    requests_get_path.get.return_value.json.return_value = quote

    # run code
    result = get_random_quote()

    # assert result
    requests_get_path.get.assert_called_once()
    assert result == quote[0]["q"]


@pytest.mark.meme_tests
def test_construct_meme_url():
    url = construct_meme_url("10-Guy", "top", "bottom")
    assert url == "https://apimeme.com/meme?meme=10-Guy&top=top&bottom=bottom"

@pytest.mark.meme_tests
def test_generate_meme(mocker):
    requests_get_path = mocker.patch("testing_workshop.i_need_testing.requests")
    requests_get_path.get.return_value.content = b"meme"

    result = generate_meme("top", "bottom")

    requests_get_path.get.assert_called_once()
    assert result == b"meme"

@pytest.mark.meme_tests
def test_save_meme(mocker):
    mock_open = mocker.patch("builtins.open")
    save_meme(b"meme")

    mock_open.assert_called_once_with("meme.jpg", "wb")
    mock_open.return_value.write.assert_called_once_with(b"meme")

@pytest.mark.meme_tests
def test_create_meme(mocker):
    get_random_quote_path = mocker.patch("testing_workshop.i_need_testing.get_random_quote")
    generate_meme_headings_path = mocker.patch("testing_workshop.i_need_testing.generate_meme_headings")
    generate_meme_path = mocker.patch("testing_workshop.i_need_testing.generate_meme")
    save_meme_path = mocker.patch("testing_workshop.i_need_testing.save_meme")

    get_random_quote_path.return_value = "quote"
    generate_meme_headings_path.return_value = "top", "bottom"
    generate_meme_path.return_value = b"meme"

    create_meme()

    get_random_quote_path.assert_called_once()
    generate_meme_headings_path.assert_called_once_with("quote")
    generate_meme_path.assert_called_once_with("top", "bottom")
    save_meme_path.assert_called_once_with(b"meme")


    
