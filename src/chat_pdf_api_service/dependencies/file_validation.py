from fastapi import HTTPException, UploadFile


"""
A class to validate uploaded files in a FastAPI application.

Attributes:
    file (UploadFile): The uploaded file to be validated.

Methods:
    check_file_type() -> bool:
        Validates the file type against a list of allowed content types.
        Raises an HTTPException if the file type is invalid.

    check_file_size() -> bool:
        Validates the file size against a maximum allowed size of 5MB.
        Raises an HTTPException if the file size exceeds the limit.
"""
class FileValidator:
    def __init__(self, file: UploadFile):
        self.file = file

        self.check_file_type()
        self.check_file_size()

    def check_file_type(self) -> bool:
        allowed_content_types = ["application/pdf"]
        if self.file.content_type not in allowed_content_types:
            raise HTTPException(
                status_code=400, detail={"message": "Inavlid file type"}
            )
        else:
            True

    def check_file_size(self) -> bool:
        allowed_file_size = 15 * 1024 * 1024  # 15mb

        self.file.file.seek(0)
        if len(self.file.file.read()) > allowed_file_size:
            raise HTTPException(
                status_code=400, detail={"message": "File size exceded 5mb"}
            )
        else:
            return True
