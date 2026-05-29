from configs.other_config import DIALOG_ACTIONS


def accept_dialog_once(page, expected_part_message):
    def handler(dialog):
        assert expected_part_message in dialog.message
        dialog.accept()
    page.once("dialog",handler)
def prompt_dialog_once(page,expected_part_message,text):
    if text is None:
        raise ValueError("Prompt requires text")
    def handler(dialog):
        assert expected_part_message in dialog.message
        dialog.accept(text)
    page.once("dialog",handler)
def dismiss_dialog_once(page,expected_part_message):
    def handler(dialog):
        assert expected_part_message in dialog.message
        dialog.dismiss()
    page.once("dialog",handler)

def handle_dialog_on(
    dialog,
    expected_part_message: str,
    action: str,
    text: str | None = None
):
    if expected_part_message not in dialog.message:
        raise AssertionError(f"Unexpected dialog: {dialog.message}")

    action = action.lower()

    if action not in DIALOG_ACTIONS:
        raise ValueError(f"Unsupported action: {action}")

    if action == "accept":
        dialog.accept()

    elif action == "dismiss":
        dialog.dismiss()

    elif action == "prompt":
        if text is None:
            raise ValueError("Prompt action requires text")
        dialog.accept(text)

    else:
        raise ValueError(f"Unhandled dialog action: {action}")

