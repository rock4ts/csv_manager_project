from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from file_data.models import FileData
from .messages import ResponseMessage


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True)
    filename = serializers.CharField(
        max_length=123,
        validators=[
            UniqueValidator(queryset=FileData.objects.all(),
                            message=ResponseMessage.file_exists)
        ]
    )

    class Meta:
        model = FileData
        fields = ('id', 'file', 'filename')


class FileInfoSerializer(serializers.ModelSerializer):
    column_names = serializers.SerializerMethodField()
    number_of_entries = serializers.SerializerMethodField()

    class Meta:
        model = FileData
        fields = ('id', 'filename', 'column_names', 'number_of_entries')

    def get_column_names(self, obj):
        return obj.data[0].keys()

    def get_number_of_entries(self, obj):
        return len(obj.data)
