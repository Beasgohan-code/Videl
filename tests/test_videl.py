import pytest

from videl import Button, ButtonStyle, RichMessage, button, inline


def test_button_style_is_adapter_only_by_default():
    item = button("Play", callback="play:42", style=ButtonStyle.PRIMARY)
    assert item.to_dict() == {"text": "Play", "callback_data": "play:42"}
    assert item.to_dict(include_style=True)["style"] == "primary"


def test_keyboard_and_rich_message_payload():
    keyboard = inline([button("Play", callback="play"), button("Docs", url="https://example.com")])
    message = RichMessage("<b>Hello</b>").buttons(keyboard)
    payload = message.to_payload(123)
    assert payload["chat_id"] == 123
    assert payload["reply_markup"]["inline_keyboard"][0][0]["callback_data"] == "play"


def test_exclusive_button_actions():
    with pytest.raises(ValueError):
        Button("bad", callback_data="a", url="https://example.com")


def test_callback_limit():
    with pytest.raises(ValueError):
        Button("bad", callback_data="x" * 65)
