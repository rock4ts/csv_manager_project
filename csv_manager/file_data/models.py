import csv

from django.db import models

from .utils import find_delimiter, parse_file_bytes


class FileData(models.Model):
    file = models.FileField(upload_to='uploaded_files/',
                            verbose_name='Файл')
    filename = models.CharField(max_length=123,
                                blank=True,
                                unique=True,
                                verbose_name='Имя файла')
    data = models.JSONField(blank=True, default=list)

    class Meta:
        verbose_name_plural = 'FileData'

    def save(self, *args, **kwargs):
        if not self.filename:
            self.filename = self.file.name
        if not self.data:
            delimiter = find_delimiter(self.file)
            decoding_generator = parse_file_bytes(self.file)
            reader = csv.DictReader(decoding_generator,
                                    delimiter=delimiter,
                                    skipinitialspace=True)
            self.data = list()
            for row in reader:
                self.data.append(row)
        super().save(*args, **kwargs)
