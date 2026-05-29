

from configs.env_config import PICTURE_TEST_DATA_DIR


def get_uploaded_items(self,uploaded_file_items):
    count = uploaded_file_items.count()
    if count ==0:
        raise Exception("No uploaded items found")

    return [
        {
            "name": item.locator("p").inner_text().strip(),
            "size": item.locator("span").inner_text().strip()
        }
        for item in [
            self.uploaded_file_items.nth(i)
            for i in range(count)
        ]
    ]

from playwright.sync_api import expect

def wait_for_uploaded_file(
        uploaded_items_locator,
        expected_count: int,
        timeout: int = 10000
):

    expect(uploaded_items_locator).to_have_count(
        expected_count,
        timeout=timeout
    )

def upload_multiple_files_in_once(locator, files: list[str]):

    file_paths = []

    for file_name in files:

        file_path = PICTURE_TEST_DATA_DIR / file_name

        if not file_path.exists():
            raise FileNotFoundError(
                f"Upload file does not exist: {file_path}"
            )

        file_paths.append(str(file_path))
        # upload_file_by_area(locator,file_name)

    locator.set_input_files(file_paths)
def upload_multiple_files_one_by_one(page, upload_area_locator, files: list[str], timeout: int = 3000):

    print(f"Refer to the number of uploaded files is: {len(files)}")
    if not isinstance(files, list):
        raise TypeError(f"Expected list but got {type(files).__name__}")
    if not files:
        raise ValueError("No uploaded files found")
    for file_name in files:

        file_path = PICTURE_TEST_DATA_DIR / file_name

        if not file_path.exists():
            raise FileNotFoundError(
                f"Upload file does not exist: {file_path}"
            )

        # ========= WAY 1 =========
        # try normal input[type=file]
        try:

            file_input = page.locator("input[type='file']")

            if file_input.count() > 0:
                file_input.first.set_input_files(
                    str(file_path),
                    timeout=timeout
                )
                continue

        except Exception as e:
            print(f"Direct upload failed: {e}")

        # ========= WAY 2 =========
        # fallback file chooser
        try:

            with page.expect_file_chooser() as fc_info:
                upload_area_locator.click()

            fc_info.value.set_files(str(file_path))
            continue

        except TimeoutError:
            raise AssertionError(
                "Unable to upload file by both methods")


def upload_file_by_area(page, upload_area_locator, file_name: str):
    file_path = PICTURE_TEST_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Upload file does not exist: {file_path}")

    with page.expect_file_chooser() as fc_info:
        upload_area_locator.click()

    fc_info.value.set_files(str(file_path))

def get_dict_value(data: dict, key: str, default=None):
    if not isinstance(data, dict):
        raise TypeError(f"Expected dict but got {type(data).__name__}")

    return data.get(key, default)


def get_values_from_list_dict(data: list[dict], key: str) -> list:
    if not isinstance(data, list):
        raise TypeError(f"Expected list but got {type(data).__name__}")

    return [item.get(key) for item in data]