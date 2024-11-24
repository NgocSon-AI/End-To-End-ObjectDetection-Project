# import sys

# def error_message_detail(error, error_detail: sys):
#     _, _, exc_tb = error_detail.exc_info()  # error_detail.exc_info() sẽ trả về một tuple [type(loại lỗi), value(giá trị lỗi), traceback(exc_tb)(thông tin về ngữ cảnh nơi xảy ra lỗi)]
#     # chỉ giữ lại giá trị exc_tb, bỏ _, _,

#     file_name = exc_tb.tb_frame.f_code.co_filename  # Lấy ra tên tệp và vị trí lỗi (vị trí ở đây là số dòng)

#     # Tạo thông điệp lỗi
#     error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
#         file_name, exc_tb.tb_lineno, str(error) #Tên tệp lỗi, số dòng-nơi xảy ra lỗi, thông điệp lỗi.
#     )

#     return error_message    # Chứa thông tin chi tiết về lỗi xảy ra.

# class SignException(Exception):
#     def __init__(self, error_message, error_detail):
#         """
#         :param error_message: error message in string format
        
#         """
#         super().__init__(error_message)     # Gọi hàm khởi tạo của lớp cha (Exception)
#         self.error_message = error_message_detail(
#             error_message, error_detail=error_detail    # Lưu trữ thông điệp lỗi chi tiết   error_message_detail được gọi để tạo ra thông điệp lỗi chi tiết gồm thông tin về tệp và dòng nơi lỗi xảy ra.
#         )
#     def __str__(self):
#         return self.error_message
