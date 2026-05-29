from playwright.sync_api import expect

from assertions.ui_assertions import is_locator_checked
from utils.interactions import get_alert_message, get_locator_text, safe_fill
from utils.logger_helper import logger
from utils.wait_helper import wait_for_table_update_and_ready, wait_for_table_stable


class BasePage:
    def __init__(self, page):
        self.page = page
        self.alert = self.page.locator("//p[@class='MuiTypography-root MuiTypography-body2 css-vjx6hx']")
        self.table_rows = self.page.locator("tbody tr:not(.no-data)")
        self.table_header_columns = self.page.locator("//th[@scope='col']")

        self.next_page_button = self.page.locator("//button[@aria-label='Go to next page']")
        self.previous_page_button = self.page.locator("//button[@aria-label='Go to previous page']")
        self.pagination_area = self.page.locator("//nav[@aria-label='pagination navigation']")

        self.search_textbox = self.page.locator("//input[@autocomplete='new-password']")

    def refresh_page(self):
        self.page.reload(wait_until="networkidle")

    def search_data(self, key_search):
        safe_fill(self.search_textbox, key_search)
        wait_for_table_stable(self.table_rows)
    def get_alert_text(self):
        return get_alert_message(self.alert)
    def get_table_columns(self):
        return self.table_header_columns.count()
    def get_table_rows(self):
        return self.table_rows.count()

    def get_number_of_records(self):
        wait_for_table_stable(self.table_rows)
        number_of_records:int =0
        number_records_on_page= self.get_table_rows()
        page:int =1
        if number_records_on_page == 0:
            logger.warning("No records found")
            return 0
        while True:
            number_of_records += number_records_on_page
            # print(f"Number of records : {number_records_on_page}")
            #if no pagination
            if self.next_page_button.count()==0:
                break
            #Incase the next page is exist, but noot enable
            if not self.next_page_button.is_enabled():
                break
            expect(self.next_page_button).to_be_enabled()
            self.next_page_button.click()
            page += 1
            wait_for_table_stable(self.table_rows)
            number_records_on_page = self.get_table_rows()
        print(f"total pages: {page} has {number_of_records} records")
        return number_of_records
    def get_list_of_records(self,column_name)->list:
        wait_for_table_stable(self.table_rows)
        number_of_records:int =0
        records_list = []
        column_name_index = self.get_column_index(column_name)
        number_records_on_page= self.get_table_rows()
        page:int =1
        if number_records_on_page == 0:
            logger.warning("No records found")
            return 0
        while True:
            number_of_records += number_records_on_page
            for i in range (number_records_on_page):
                row = self.table_rows.nth(i)
                cell_locators = row.locator("td")
                cell_text = get_locator_text(cell_locators.nth(column_name_index))
                records_list.append(cell_text)
            # print(f"Number of records : {number_records_on_page}")
            #if no pagination
            if self.next_page_button.count()==0:
                break
            #Incase the next page is exist, but noot enable
            if not self.next_page_button.is_enabled():
                break
            expect(self.next_page_button).to_be_enabled()
            self.next_page_button.click()
            page += 1
            wait_for_table_stable(self.table_rows)
            number_records_on_page = self.get_table_rows()
        print(f"total pages: {page} has {number_of_records} records")
        print(f"List of records shows currently: {records_list}")
        return records_list
    def get_number_record_and_verify_search_results(self,key_search,search_by_column: list) -> bool:
        columns =len(search_by_column)
        key_search = key_search.lower()
        wait_for_table_stable( self.table_rows)
        number_of_records: int = 0
        number_records_on_page = self.get_table_rows()
        page: int = 1
        if number_records_on_page == 0:
            logger.warning("No records found")
            return 0
        mis_match_rows = []
        row_match = False
        while True:
            number_of_records += number_records_on_page
            print(f"Number of records : {number_records_on_page} on page {page}")
            #Verify data
            for i in range (number_of_records):
                row = self.table_rows.nth(i)
                cells = row.locator("td")
                for col_idx in range(columns):
                    cell_text = (get_locator_text(cells.nth(col_idx)) or "").lower()
                    if key_search in cell_text:
                        row_match = True
                        break
                if not row_match:
                    row_data = get_locator_text(cells)
                    logger.debug(f"Row {i} mismatch. Data: {row_data}")
                    mis_match_rows.append(i)

            if not self.next_page_button.is_enabled():
                break
            expect(self.next_page_button).to_be_enabled()
            self.next_page_button.click()
            page += 1
            wait_for_table_update_and_ready(self.table_rows)
            number_records_on_page = self.get_table_rows()
        if mis_match_rows:
            logger.warning(f"Rows mismatch with key '{key_search}': {mis_match_rows}")
        logger.info(f"total pages: {page} has {number_of_records} records")
        return number_of_records
    def verify_search_results(self,key_search,search_by_column: list, records:int) -> bool:
        # columns =len(search_by_column)
        key_search = key_search.lower()
        if records == 0:
            logger.warning("No records found")
            return 0
        mis_match_rows = []

        #Verify data
        for i in range (records):
            row_match = False
            row = self.table_rows.nth(i)
            cells = row.locator("td")
            for col_idx in search_by_column:
                cell_text = (get_locator_text(cells.nth(col_idx)) or "").lower()
                if key_search in cell_text:
                    row_match = True
                    break
            if not row_match:
                row_data = cells.all_inner_text()
                logger.debug(f"Row {i} mismatch. Data: {row_data}")
                mis_match_rows.append(i)
        if mis_match_rows:
            logger.warning(f"Rows mismatch on current page with key '{key_search}': {mis_match_rows}")
            return False
        return True
    def verify_search_data_after_search(self,key_search,search_by_column: list) -> bool:

        wait_for_table_update_and_ready( self.table_rows)
        number_of_records: int = 0
        number_records_on_page = self.get_table_rows()
        page: int = 1
        if number_records_on_page == 0:
            logger.warning("No records to verify")
            return False
        all_match= True
        while True:
            number_of_records += number_records_on_page
            print(f"Number of records : {number_records_on_page}")
            if not self.verify_search_results(key_search,search_by_column,number_records_on_page):
                all_match = False
            if not self.next_page_button.is_enabled():
                break
            self.next_page_button.click()
            page += 1
            wait_for_table_update_and_ready(self.table_rows)
            number_records_on_page = self.get_table_rows()
        logger.info(f"total pages: {page} has {number_of_records} records")
        return all_match

    def get_column_index(self, column_name: str) -> int:
        """
        Return column index by column name.
        """

        if not isinstance(column_name, str):
            raise TypeError(
                f"Expected column_name as str "
                f"but got {type(column_name).__name__}"
            )

        headers = [
            text.strip().lower()
            for text in self.table_header_columns.all_text_contents()
        ]

        normalized_column = column_name.strip().lower()

        if normalized_column not in headers:
            raise ValueError(
                f"Column '{column_name}' not found. "
                f"Available columns: {headers}"
            )

        return headers.index(normalized_column)

    def get_cell_text(
            self,
            row_locator,
            column_name: str,
    ) -> str:
        """
        Get cell text from row by column name.
        """


        col_index = self.get_column_index(
            column_name
        )

        return (
            row_locator.locator("td")
            .nth(col_index)
            .text_content()
            .strip()
        )

    def get_column_texts_for_checked_rows(
            self,
            column_name: str,
    ) -> list[str]:

        texts = []

        total_records = 0
        page = 1

        while True:

            row_count = self.table_rows.count()

            print(
                f"Page {page}: {row_count} records"
            )

            total_records += row_count

            for i in range(row_count):

                row = self.table_rows.nth(i)

                checkbox = row.get_by_role(
                    "checkbox"
                ).first

                if is_locator_checked(checkbox):
                    texts.append(
                        self.get_cell_text(
                            row,
                            column_name,
                        )
                    )

            if not self.next_page_button.is_visible():
                break

            if not self.next_page_button.is_enabled():
                break

            self.next_page_button.click()

            page += 1

            wait_for_table_update_and_ready(
                self.table_rows
            )

        logger.info(
            f"Total pages: {page}, "
            f"total records: {total_records}, "
            f"selected data: {texts}"
        )

        return texts
    def select_checkbox_matching_key_search(
            self,
            key_search: str,
            column_name: str,
    ):
        selected_checkbox = False
        while True:

            row_count = self.table_rows.count()
            for i in range(row_count):

                row = self.table_rows.nth(i)
                checkbox = row.get_by_role(
                    "checkbox"
                )

                if self.get_cell_text(
                            row,
                            column_name,
                        ) == key_search:
                    checkbox.click()
                    selected_checkbox = True
                    break
            if not self.next_page_button.is_visible():
                break

            if not self.next_page_button.is_enabled():
                break

            self.next_page_button.click()

            wait_for_table_update_and_ready(
                self.table_rows
            )
        if selected_checkbox:
            print(f"Selected row checkbox which data of column {column_name} matching key search: {key_search}")
        else:
            print(f"Unable to find matching key search: {key_search} in the column {column_name}, can not select proper checkbox")
    def get_row_index_matching_condition(self, column_name, key_search):
        number_of_rows = self.get_number_of_records()
        specific_row= 0
        if number_of_rows==0:
            return specific_row
        for i in range(number_of_rows):
            row = self.table_rows.nth(i)
            if key_search in self.get_cell_text(row, column_name):
                specific_row = i
                break
        return specific_row
    def get_cell_locator(self, column_name, key_search):
        number_of_rows = self.get_number_of_records()
        column_index = self.get_column_index(column_name)
        specific_cell_locator = None
        if number_of_rows==0:
            raise Exception ("No row in the grid table")
        for i in range(number_of_rows):
            row = self.table_rows.nth(i)
            row_text = get_locator_text(row)
            if key_search in row_text:
                specific_cell_locator = row.locator("td").nth(column_index)
                break
        return specific_cell_locator



























