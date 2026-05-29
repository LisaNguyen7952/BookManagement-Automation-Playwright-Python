
from playwright.sync_api import expect

from utils.interactions import get_locator_text, get_locator_texts
from utils.logger_helper import logger


def expect_locator_have_text(locator, expected: str) -> bool:
    text = get_locator_text(locator)
    return text.strip().casefold() == expected.strip().casefold()

def expect_locator_contains_text(locator, expected: str):
    actual = get_locator_text(locator)
    assert expected.strip().casefold() in actual.strip().casefold(), f"Expected '{expected}' in '{actual}'"

def expect_url_contains(page, partial_url: str):
    assert partial_url.strip().casefold() in page.url.strip().casefold(), \
        f"URL '{page.url}' does not contain '{partial_url}'"
def expect_text_contains(actual_text,expected_partial_text: str):
    assert expected_partial_text.strip().casefold() in actual_text.strip().casefold(), \
        f"URL '{actual_text}' does not contain '{expected_partial_text}'"
def expected_text(actual_text,expect_text:str):
    # So sánh (strip + không phân biệt hoa/thường)
    assert actual_text.strip().casefold() == expect_text.strip().casefold(), \
        f"Expected text '{expect_text}' but got '{actual_text}'"
    #Need to return fails once the element is not visible
def verify_visible_locator(locator):
    try:
        expect(locator).to_be_visible()
    except AssertionError:
        raise AssertionError(f"Expected locator {locator} is not visible")
    #want to return a True or False to process

def is_locator_visible(locator, timeout: int = 3000) -> bool:
    try:
        # Smart wait: chờ cho đến khi locator hiện ra trong khoảng timeout
        expect(locator).to_be_visible(timeout=timeout)
        return True
    except (AssertionError, TimeoutError):
        # Nếu chờ không thấy, fallback: check tức thì
        return locator.is_visible()

def is_locator_invisible(locator, timeout=3000):
    try:
        expect(locator).to_be_hidden(timeout=timeout)
        return True
    except:
        return not locator.is_visible()

def is_locator_enable(locator, timeout: int = 5000) -> bool:
    """
    Kiểm tra locator có enable không.
    Hỗ trợ:
      - disabled attribute
      - aria-disabled
      - class='disabled' (ở chính locator hoặc thẻ cha)
    Trả về True nếu enable, False nếu disable.
    """
    try:
        locator.wait_for(state="visible", timeout=timeout)

        # 1. Check attribute disabled
        disabled_attr = locator.get_attribute("disabled")
        if disabled_attr is not None:
            return False

        # 2. Check aria-disabled
        aria_disabled = locator.get_attribute("aria-disabled")
        if aria_disabled and aria_disabled.lower() == "true":
            return False

        # 3. Check class='disabled' ở chính locator
        class_attr = locator.get_attribute("class") or ""
        if "disabled" in class_attr.split():
            return False

        # 4. Check mở rộng — nếu cha có class disabled
        try:
            parent_class = locator.evaluate(
                "el => el.parentElement && el.parentElement.classList ? Array.from(el.parentElement.classList).join(' ') : ''"
            )
            if "disabled" in parent_class:
                return False
        except Exception:
            pass  # nếu element không có cha thì bỏ qua

        return True
    except Exception:
        return False
def is_locator_checked(locator, value=None):
    count = locator.count()

    if count == 0:
        logger.info("No elements found")
        return False

    # Nếu không truyền value → check phần tử đầu tiên
    if value is None:
        return locator.first.is_checked()

    expected = value.strip().casefold()

    for i in range(count):
        el = locator.nth(i)

        attr_value = (el.get_attribute("value") or "").strip().casefold()

        label_text = (
            el.evaluate("""
                el => {
                    const label =
                        el.nextElementSibling?.innerText ||
                        el.parentElement?.innerText ||
                        "";
                    return label.trim().toLowerCase();
                }
            """)
            or ""
        )

        if expected in [attr_value, label_text]:
            return el.is_checked()

    return False

def does_locator_have_texts(locator, expected_list: list[str]):
    """
        So sánh dữ liệu từ field với expected list.

        :param locator: Locator cần lấy dữ liệu.
        :param expected_list: Danh sách giá trị mong đợi.
        """
    actual = get_locator_texts(locator)

    if not actual:
        print(f"There is no value on the locator to verify")
        return False
    missing_items=[item for item in expected_list
                   if item not in expected_list]
    if missing_items:
        print(f"Missing items: {missing_items} while actual: {actual} ")
        return False


    print(f"✅ All expected items found: {expected_list}")
    return True
def assert_dict_match(actual: dict, expected: dict, ignore_keys:list[str]|None = None):
    ignore_keys = ignore_keys or []
    mismatches = []

    for key, expected_value in expected.items():
        if key in ignore_keys:
            continue
        actual_value = actual.get(key)

        if actual_value != expected_value:
            mismatches.append(
                f"[{key}] actual: {actual_value} | expected: {expected_value}"
            )

    if mismatches:
        raise AssertionError(
            "Data mismatch:\n" + "\n".join(mismatches)
        )
def assert_list_dict_match(
    actual: list[dict],
    expected: list[dict],
    ignore_keys: list[str] | None = None,
):
    ignore_keys = ignore_keys or []
    mismatches = []

    if len(actual) != len(expected):
        raise AssertionError(
            f"Length mismatch: actual {len(actual)} | expected {len(expected)}"
        )

    for index, expected_item in enumerate(expected):
        actual_item = actual[index]

        for key, expected_value in expected_item.items():
            if key in ignore_keys:
                continue

            actual_value = actual_item.get(key)

            if actual_value != expected_value:
                mismatches.append(
                    f"[item {index}][{key}] actual: {actual_value} | expected: {expected_value}"
                )

    if mismatches:
        raise AssertionError(
            "Data mismatch:\n" + "\n".join(mismatches)
        )