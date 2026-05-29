import asyncio
import re
from utils.logger_helper import logger
from utils.string_helper import _normalize_option_texts
def wait_for_locator_visible(locator, timeout=10000):
     locator.wait_for(state="visible", timeout=timeout)
     return locator

# async def safe_click(locator, timeout=5000):
#     await locator.wait_for(state="visible", timeout=timeout)
#     await locator.click()
def safe_click(locator, timeout=5000):
    """
    Wait for element visible, scroll into view, then click safely.
    Retry once if intercepted.
    """
    locator.wait_for(state="visible", timeout=timeout)
    locator.scroll_into_view_if_needed()

    try:
        locator.click(timeout=timeout)
    except Exception as e:
        if "intercepts pointer events" in str(e):
            asyncio.sleep(0.5)
            locator.scroll_into_view_if_needed()
            locator.click(timeout=timeout)
        else:
            raise
def safe_double_clicks(locator, timeout = 5000):
    locator.wait_for(state="visible",timeout=timeout)
    locator.scroll_into_view_if_needed()
    try:
        locator.dblclick(timeout=timeout)
    except Exception as e:
        if "intercepts pointer events" in str(e):
            asyncio.sleep(0.5)
            locator.scroll_into_view_if_needed()
            locator.dblclick(timeout=timeout)
        else:
            raise

def safe_fill(locator, value, timeout=5000):
    if value is None:
        return  # intentionally do nothing

    if isinstance(value, (int, float)):
        value = str(value)

    if not isinstance(value, str):
        raise TypeError(
            f"safe_fill expects str/int/float, got {type(value)}"
        )

    locator.wait_for(state="visible", timeout=timeout)
    # locator.wait_for(state="editable", timeout=timeout)
    locator.scroll_into_view_if_needed()
    locator.fill(value)



def select_dropdown(dropdown_trigger, option_text_or_value: str, timeout: int = 5000):
    """
    Chọn option từ dropdown:
    - dropdown_trigger: Locator của trigger (<select> hoặc div)
    - option_text_or_value: text hoặc value cần chọn
    - timeout: thời gian chờ, default 5s
    """
    dropdown_trigger.wait_for(state="visible", timeout=timeout)
    tag_name = dropdown_trigger.evaluate("el => el.tagName.toLowerCase()")

    if tag_name == "select":
        # Native <select>
        try:
            dropdown_trigger.select_option(option_text_or_value)
        except Exception as e:
            dropdown_trigger.select_option(label=option_text_or_value)
    else:
        # Custom dropdown (VD: Select2)
        dropdown_trigger.click()
        page = dropdown_trigger.page

        # Chọn option trực tiếp
        option_locator = page.locator(
            f"//ul[contains(@class,'select2-results')]//div[@role='option' and "
            f"(normalize-space(text())='{option_text_or_value}' "
            f"or @value='{option_text_or_value}' "
            f"or @data-value='{option_text_or_value}')]"
        )

        option_locator.wait_for(state="visible", timeout=timeout)
        option_locator.scroll_into_view_if_needed()
        option_locator.click()

def select_dropdown_value(
    dropdown_trigger,
    option_text_or_value: str,
    timeout: int = 5000,
    current_value: str | None = None
):
    if current_value:
        if current_value.strip().casefold() == option_text_or_value.strip().casefold():
            logger.info(f"✅ Dropdown already has value: {option_text_or_value}")
            return

    dropdown_trigger.wait_for(state="visible", timeout=timeout)

    tag_name = dropdown_trigger.evaluate(
        "el => el.tagName.toLowerCase()"
    )

    if tag_name == "select":
        dropdown_trigger.select_option(value=option_text_or_value)
    else:
        dropdown_trigger.click()

        # 🔥 KEY FIX: phải nhập text để load option
        dropdown_trigger.fill(option_text_or_value)

        page = dropdown_trigger.page

        # option_locator = page.get_by_role(   # Text Matching 100%
        #     "option",
        #     name=option_text_or_value
        # )
        option_locator = page.get_by_role("option").filter(
            has_text=re.compile(option_text_or_value, re.IGNORECASE)
        )

        option_locator.first.wait_for(state="visible", timeout=timeout)
        option_locator.first.click()


def select_radio_button(radio_group_locator, raw_value):
    value= raw_value.strip().casefold()
    radio_group_locator.first.wait_for(state="attached")
    count = radio_group_locator.count()

    if count == 0:
        raise Exception("No radio buttons found")

    for i in range(count):
        el = radio_group_locator.nth(i)
        attr_value=(el.get_attribute("value") or "").strip().casefold()
        label_text= el.evaluate("el=> el.nextElementSibling?.innerText?.trim().toLowerCase()")
        if value in [attr_value,label_text]:
            el.check()
            return
    raise Exception(f"Radio button with value '{value}' not found")


def get_locator_text(locator) -> str:
    if locator.count() == 0:
        return ""

    first = locator.first

    tag_name = first.evaluate(
        "el => el.tagName.toLowerCase()"
    )

    if tag_name in ["input", "textarea"]:
        return first.input_value().strip()

    if tag_name == "select":
        return (
            first.locator("option:checked")
            .inner_text()
            .strip()
        )

    return first.inner_text().strip()

# def get_locator_texts(locator) -> list[str]:
#     """
#     Trả về danh sách giá trị từ field (select/input/textarea/div...).
#     Luôn trả về list[str], có thể rỗng nếu không có element.
#     """
#
#     count = locator.count()
#     if count == 0:
#         return []
#
#     tag_name = locator.first.evaluate("el => el.tagName.toLowerCase()")
#
#     if tag_name == "select":
#         return locator.evaluate_all(
#             "els => els.filter(o => o.selected).map(o => o.value)",
#             locator.locator("option")
#         )
#
#     if tag_name in ["input", "textarea"]:
#         value =  locator.first.input_value()
#         return [value] if value else []
#
#     texts = locator.all_inner_texts()
#     return [t.strip() for t in texts if t.strip()]
def get_locator_texts(locator) -> list[str]:
    """
    Return text/value list from multiple locators.
    """

    if locator.count() == 0:
        return []

    first = locator.first

    tag_name = first.evaluate(
        "el => el.tagName.toLowerCase()"
    )

    if tag_name in ["input", "textarea"]:
        return locator.evaluate_all(
            """
            els => els
                .map(el => el.value?.trim())
                .filter(Boolean)
            """
        )

    if tag_name == "select":
        return locator.evaluate_all(
            """
            els => els.map(
                el => el.options[el.selectedIndex]?.text?.trim()
            ).filter(Boolean)
            """
        )

    return locator.evaluate_all(
        """
        els => els
            .map(el => el.textContent?.trim())
            .filter(Boolean)
        """
    )
def get_locator_attribute_text(
    locator,
    attr_name: str
) -> str:

    if locator.count() == 0:
        return ""

    value = locator.first.get_attribute(attr_name)

    return value.strip() if value else ""
def get_locator_attribute_texts(locator, attr_name: str) -> list[str]:
    count = locator.count()
    if count == 0:
        return []

    return locator.evaluate_all(
        f"els => els.map(el => el.getAttribute('{attr_name}'))"
    )
def select_multiple_dropdown_values(
    dropdown_field,
    option_texts: list[str],
    dropdown_options_locator=None,
    selected_values_locator=None,
    skip_selected: bool = True,
    timeout: int = 5000,
):
    """
    Select multiple values from dropdown.
    """

    option_texts = _normalize_option_texts(option_texts)

    # Auto derive option locator if not passed
    if dropdown_options_locator is None:
        dropdown_options_locator = dropdown_field.page.locator(
            '[role="option"]'
        )

    current_values = []

    if skip_selected and selected_values_locator:
        raw = get_locator_texts(selected_values_locator)
        current_values = [
            t.replace("×", "").strip()
            for t in raw
        ]

    for value in option_texts:

        if skip_selected and value in current_values:
            print(f"⏭️ Skip selected value: {value}")
            continue

        dropdown_field.scroll_into_view_if_needed()
        dropdown_field.click()

        option = dropdown_options_locator.filter(has_text=value).first

        option.wait_for(state="visible", timeout=timeout)

        try:
            option.click()
        except Exception:
            option.click(force=True)

        print(f"✅ Selected: {value}")


def get_alert_message(
    locator,
    timeout: int = 3000
) -> str | None:
    try:
        locator.wait_for(state="visible", timeout=timeout)
        text = locator.inner_text()
        return text.strip()
    except TimeoutError:
        return None

async def scroll_to_the_last_element(element_locator, delay=300):
    """
    :param element_locator: locator of items which is interacting
    :param delay: time to load/render before count
    :return:
    """
    previous_count = 0
    page = element_locator.page  # lấy page từ locator

    while True:
        last_item = element_locator.last
        await last_item.scroll_into_view_if_needed()
        await wait_for_locator_visible(last_item)
        await page.wait_for_timeout(delay)
        current_count = await element_locator.count()
        if current_count == previous_count:
            break
        previous_count= current_count


def set_is_active(page, expected: bool):
    checkbox = page.locator("input[name='isActive']")
    switch = page.locator("span.MuiSwitch-switchBase")

    checkbox.wait_for()

    current = checkbox.is_checked()
    # print("Before:", current)

    if current != expected:
        switch.click(force=True)

        # 🔥 trigger form update
        page.click("body")

        page.wait_for_timeout(300)

    # print("After:", checkbox.is_checked())

def is_tab_selected(tab_locator) -> bool:
    return tab_locator.get_attribute("aria-selected") == "true"