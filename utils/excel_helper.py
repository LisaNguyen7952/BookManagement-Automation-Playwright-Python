from datetime import datetime
import openpyxl

from utils.interactions import get_locator_text


def read_excel_file(file_path, sheet_name: str):
    """
    Đọc dữ liệu từ Excel và trả về:
      - data: list[tuple], mỗi row là 1 tuple
      - headers: list[str]
    """
    workbook = openpyxl.load_workbook(file_path, data_only=True)
    sheet = workbook[sheet_name]

    # Lấy headers ở dòng đầu tiên
    headers = [cell.value for cell in sheet[1]]

    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = []
        for key, value in zip(headers, row):
            if isinstance(value, datetime):
                row_data.append(value.strftime("%Y-%m-%d"))
            elif isinstance(value, (int, float)):
                row_data.append(str(value).rstrip(".0"))
            elif value is None:
                row_data.append("")
            else:
                row_data.append(str(value).strip())
        data.append(tuple(row_data))  # ✅ tuple phẳng
    return data, headers


def read_excel_with_multivalue(file_path, sheet_name: str, multivalue_columns=None, delimiter=","):
    """
    Đọc Excel, xử lý cột multi-value thành list (tự động split).
    :param file_path: đường dẫn Excel
    :param sheet_name: tên sheet
    :param multivalue_columns: list tên cột cần split
    :param delimiter: ký tự phân tách (mặc định ",")
    """
    raw_data, headers = read_excel_file(file_path, sheet_name)

    if not multivalue_columns:
        return raw_data  # ✅ giữ nguyên tuple list

    col_indexes = [headers.index(col) for col in multivalue_columns if col in headers]

    processed_data = []
    for row in raw_data:
        row_as_list = list(row)
        for idx in col_indexes:
            value = row_as_list[idx]
            if value:
                row_as_list[idx] = [v.strip() for v in value.split(delimiter)]
            else:
                row_as_list[idx] = []
        processed_data.append(tuple(row_as_list))  # ✅ tuple phẳng
    return processed_data
def read_excel_selected_columns(file_path, sheet_name: str, selected_columns: list[str]):
    """
    Đọc Excel nhưng chỉ lấy các cột được chỉ định.
    :param file_path: đường dẫn file Excel
    :param sheet_name: tên sheet
    :param selected_columns: danh sách tên cột cần lấy (theo header)
    :return: list[tuple] chứa dữ liệu của các cột cần thiết
    """
    all_data, headers = read_excel_file(file_path, sheet_name)

    # Xác định index của các cột cần lấy
    col_indexes = [headers.index(col) for col in selected_columns if col in headers]

    # Chỉ trích ra các giá trị cần thiết từ từng row
    filtered_data = [
        tuple(row[i] for i in col_indexes)
        for row in all_data
    ]

    return filtered_data

