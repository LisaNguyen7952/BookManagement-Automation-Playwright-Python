import pytest

from assertions.ui_assertions import assert_dict_match
from data.book_factory import BookFactory
from ui.pages.book_management import UIBookManagement
from utils.logger_helper import logger


def test_add_new_book(page):
    book_detail = BookFactory.create_book(random_fields=["name","price","description","pictures","categories","promotions"])
    print(f"New book detail is {book_detail}")
    book_management = UIBookManagement(page)
    book_name = book_detail["name"]
    book_management.view_book_management()
    assert book_management.is_book_management_page_visible(), f"Unable to view book management page, pls recheck"
    book_management.view_add_new_book_page()
    assert book_management.is_book_detail_page_visible(), f"Unable to view the add new book management page, pls recheck"
    book_management.add_new_book(book_detail)
    assert book_management.is_add_new_book_page_invisible(), f"Unable to close the new book page, pls recheck"
    logger.info(f"Added new book which name - {book_detail['name']}to book management page successfully")
    #View book after created
    for category in book_detail["categories"]:
        book_category = category
        book_management.view_book_management()
        assert book_management.is_book_management_page_visible(), f"Unable to view book management page, pls recheck"
        book_management.view_book_category_tab(book_category)
        book_management.view_specific_book_detail(book_name)
        assert book_management.is_book_detail_page_visible()
        current_book_detail = book_management.get_book_detail()
        print(f"Book detail is {current_book_detail}")
        assert_dict_match(current_book_detail,book_detail)
    logger.info(f"Book detail of {book_detail["name"]} shows correctly in category tabs")
def test_view_book_category(page):
    book_management = UIBookManagement(page)
    book_category = "Adventure"
    book_management.view_book_management()
    assert book_management.is_book_management_page_visible(), f"Unable to view book management page, pls recheck"
    book_management.view_book_category_tab(book_category)
    assert book_management.is_book_category_tab_selected(book_category),f"Unable to tap the book category tab, pls recheck"
    logger.info(f"Number of books in this category is {book_management.get_number_of_books_for_specific_category(book_category)}")


def test_view_specific_book_category(page):
    book_management = UIBookManagement(page)
    book_category = "Adventure"
    book_management.view_book_management()
    assert book_management.is_book_management_page_visible(), f"Unable to view book management page, pls recheck"
    book_category_list = book_management.get_category_tab_list()
    print(f"Category tab list is {book_category_list}")
    assert book_category in book_category_list,f"Book category {book_category} is not in the book category list, can not view it, pls recheck"
    book_management.view_book_category_tab(book_category)
    assert book_management.is_book_category_tab_selected(book_category),f"Unable to tap the book category tab, pls recheck"
    number_of_books = book_management.get_number_of_books_for_specific_category(book_category)
    # print(f"Number of books in this category - {book_category} is {number_of_books}")
    current_number_of_books = book_management.get_number_of_books_currently_showing()
    assert current_number_of_books == number_of_books, f"Number of books show incorrectly, actual show is {current_number_of_books} while number of books is {number_of_books}"
    logger.info(f"The list of book names of category {book_category} shows correctly and it is: {current_number_of_books}")
@pytest.mark.smoke
def test_view_specific_book(page):
    book_management = UIBookManagement(page)
    book_detail = {'name': 'dPRzujD aqIrDxLsYZ', 'price': 108816, 'description': 'uGgxnvcnNFsVDkU', 'pictures': ['VJ703_13-01-2026.png', 'download.jpeg'], 'promotions': [], 'categories': ['Đón tết nao cả nhà ưi']}
    assert book_detail["categories"],f"Book category can not blank"
    book_name = book_detail["name"]
    for category in book_detail["categories"]:
        book_category = category
        book_management.view_book_management()
        assert book_management.is_book_management_page_visible(), f"Unable to view book management page, pls recheck"
        book_category_list = book_management.get_category_tab_list()
        print(f"Category tab list is {book_category_list}")
        assert book_category in book_category_list,f"Book category {book_category} is not in the book category list, can not view it, pls recheck"
        book_management.view_book_category_tab(book_category)
        book_list = book_management.get_book_list_currently_showing()
        assert book_name in book_list,f"Book name {book_name} not in the book list, unable to its view detail"
        book_management.view_specific_book_detail(book_name)
        assert book_management.is_book_detail_page_visible()
        current_book_detail = book_management.get_book_detail()
        print(f"Book detail is {current_book_detail}")
        assert_dict_match(current_book_detail,book_detail)
    logger.info(f"Book detail of {book_detail["name"]} shows correctly in category tabs")


def test_adjust_book_info(page):
    book_management = UIBookManagement(page)
    book_detail={
        'name': 'KLSVDYEf AvaikzV', 'description': 'This book has been adjusted by Lisa',
     'promotions': ['COCHI241220250123456', 'COCHI2412202501234567']
    }
    book_category = "Đón tết thui cả nhà ưi"
    book_name = book_detail["name"]
    book_management.view_book_management()
    assert book_management.is_book_management_page_visible(), f"Unable to view book management page, pls recheck"
    book_management.view_book_category_tab(book_category)
    book_list = book_management.get_book_list_currently_showing()
    assert book_name in book_list, f"Book name {book_name} not in the book list, unable to its view detail"
    book_management.view_specific_book_detail(book_name)
    assert book_management.is_book_detail_page_visible()
    book_management.adjust_book_info(book_detail)
    #View to verify
    logger.info(f"Book detail has been adjusted successfully")

def test_delete_book_info(page):
    book_management = UIBookManagement(page)
    # book_detail={
    #     'name': 'Parallel Test Book 1 - Handcrafted Bronze Tuna 1767830295402-AXl1S', 'categories': ['Đón tết 2026']
    # }
    book_category = 'Đón'
    # book_name = book_detail["name"]
    book_management.view_book_management()
    assert book_management.is_book_management_page_visible(), f"Unable to view book management page, pls recheck"
    book_category_list = book_management.get_category_tab_list()
    print(f"Category tab list is {book_category_list}")
    book_management.view_book_category_tab(book_category)
    book_list = book_management.get_book_list_currently_showing()
    book_name = book_list[0]
    # assert book_name in book_list, f"Book name {book_name} not in the book list, unable to its view detail"
    book_management.view_specific_book_detail(book_name)
    assert book_management.is_book_detail_page_visible(),f"Unable to view book detail page, pls recheck"
    book_management.delete_book()
    assert book_management.is_delete_popup_invisible(),f"Unable to close the delete book popup, pls recheck"
    logger.info(f"Show proper notification after deleted book - {book_management.get_alert_text()}")
    #Verify after delete book
    book_management.refresh_page()
    book_list_after_delete = book_management.get_book_list_currently_showing()
    print(f"Book List after delete is {book_list_after_delete}")
    assert book_name is not book_list_after_delete,f"Book name {book_name} is still exist in the book list, delete book might fail, pls recheck"
    logger.info(f"Delete book which name is {book_name} in the book category - {book_category} successfully")








