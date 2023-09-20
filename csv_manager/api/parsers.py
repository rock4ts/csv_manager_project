from rest_framework.parsers import FileUploadParser


class CSVUploadParser(FileUploadParser):
    media_type = 'text/csv'
