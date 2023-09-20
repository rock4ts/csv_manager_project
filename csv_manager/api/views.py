
import json
import os

import pandas as pd
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from file_data.models import FileData
from file_data.utils import find_delimiter
from .messages import ResponseMessage
from .parsers import CSVUploadParser
from .serializers import FileInfoSerializer, FileUploadSerializer
from .utils import df_filtering_functions


class CSVManagerViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin,
                        ListModelMixin, RetrieveModelMixin):
    queryset = FileData.objects.all()
    parser_classes = (CSVUploadParser,)
    lookup_field = 'filename'
    lookup_value_regex = "[^/]+"
    filter_backends = (OrderingFilter, SearchFilter)
    ordering = ('filename',)
    search_fields = ('id', 'filename', 'data__0')

    def get_serializer_class(self):
        if self.action == 'create':
            return FileUploadSerializer
        elif self.action in ('list', 'retrieve'):
            return FileInfoSerializer

    def create(self, request, *args, **kwargs):
        try:
            request.data.update({'filename': request.data.get('file').name})
            return super().create(request, *args, **kwargs)
        except AttributeError:
            return Response(ResponseMessage.no_file_attached,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        file = self.get_object().file
        os.remove(os.path.join(settings.MEDIA_ROOT, file.name))
        return super().destroy(request, *args, **kwargs)

    @action(['PUT'],
            detail=True,
            url_path=r'mark_datetime/(?P<datetime_col>.+)')
    def mark_datetime_col(self, *args, **kwargs):
        db_file_object = self.get_object()
        csv_file = db_file_object.file
        datetime_col = self.kwargs.get('datetime_col')
        df = pd.read_csv(csv_file)
        if '(dt)' in datetime_col:
            return Response(ResponseMessage.datetime_mark_exists,
                            status=status.HTTP_302_FOUND)
        elif datetime_col in df:
            df.rename(columns={datetime_col: datetime_col + '(dt)'},
                      inplace=True)
            df.to_csv(csv_file.path, index=False)
            for entry in db_file_object.data:
                entry[datetime_col + '(dt)'] = entry.pop(datetime_col)
            db_file_object.save()
            return Response(ResponseMessage.datetime_col_marked,
                            status=status.HTTP_200_OK)
        else:
            return Response(ResponseMessage.col_not_found,
                            status=status.HTTP_404_NOT_FOUND)

    @action(['GET'], detail=True)
    def data(self, *args, **kwargs):
        file_data_object = self.get_object()
        df = pd.read_csv(file_data_object.file,
                         delimiter=find_delimiter(file_data_object.file),
                         skipinitialspace=True)
        cols_for_display = []
        sort_cols = []
        query_params = self.request.query_params.dict()
        # extracting columns for display and ordering to separate lists
        if query_params.get('columns'):
            cols_for_display = query_params.pop('columns').split(',')
        if query_params.get('order_by'):
            sort_cols = query_params.pop('order_by').split(',')
            # creating a list of ascending/descending order indicators
            asc_desc_indicators = list()
            for i, col in enumerate(sort_cols):
                if col[0] == '-':
                    sort_cols[i] = col[1:]
                    asc_desc_indicators.append(False)
                else:
                    asc_desc_indicators.append(True)
        # extracting filter parameters
        # as lists of column name, operator and value
        filter_elements = list()
        for col_and_operator, value in query_params.items():
            try:
                col_name, operator = col_and_operator.rsplit('__')
                filter_elements.append([col_name, operator, value])
            except ValueError:
                col_name = col_and_operator
                filter_elements.append([col_name, 'contains', value])
        # find datetime columns and convert strings to datetime
        datetime_cols = [
            col for col in df.columns if '(dt)' in col
        ]
        for col in datetime_cols:
            df[col] = pd.to_datetime(df[col].astype("string"), errors='coerce')
        # applying filters
        for col, operator, value in filter_elements:
            # checking and converting filter values to numeric type
            if '(dt)' not in col:
                try:
                    value = float(value)
                except ValueError:
                    pass
            df = df_filtering_functions.get(operator)(df, col, value)
        # ordering and filtering columns for display
        if sort_cols:
            df = df.sort_values(by=sort_cols, ascending=asc_desc_indicators)
        if cols_for_display:
            df = df[cols_for_display]
        # format timestamp representation to human readable format
        for col in datetime_cols:
            if not cols_for_display or col in cols_for_display:
                df[col] = df[col].dt.strftime('%Y-%m-%d %X')
        # convert dataframe to json
        json_data = json.loads(df.to_json(orient='records'))
        return Response(json_data, status=status.HTTP_200_OK)
