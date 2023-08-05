import logging
import traceback

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.views.baseview import BaseModelApiView
from common.utils import get_next_seq_value

LOGGER = logging.getLogger(__name__)


class SequenceView(BaseModelApiView):
    """"""

    def define_nodes(self):
        # Business node 없음
        pass

    @swagger_auto_schema(methods=['post'],
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 'sequence_name': openapi.Schema(type=openapi.TYPE_STRING,
                                                                 description='Sequence 이름'),
                                 'prefix': openapi.Schema(type=openapi.TYPE_STRING,
                                                          description='Sequence 접두사'),
                                 'padding': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                           default=4,
                                                           description='Sequence 자리수(0으로 채워짐)')
                             },
                             required=['sequence_name', 'prefix']
                         ),
                         operation_description='Sequence 생성')
    @action(detail=True, methods=['post'])
    def get_next_sequence(self, request, *args, **kwargs):
        try:
            # 조회시 반환할 데이터
            return_data = {'success': True, 'code': 1, 'message': 'OK', 'data': None}

            # Sequence 생성 조건이 있는지 확인
            if 'sequence_name' not in request.data.keys() \
                    or 'prefix' not in request.data.keys() \
                    or request.data['sequence_name'] is None \
                    or request.data['prefix'] is None:
                msg = 'Sequence 생성 조건이 누락되었습니다.'
                LOGGER.info(f'{type(self).__name__} _get - message: {msg}')
                return_data['success'] = False
                return_data['code'] = -1
                return_data['message'] = msg
                return Response(return_data, status.HTTP_400_BAD_REQUEST)

            sequence_name = request.data['sequence_name']
            prefix = request.data['prefix']
            padding = int(request.data.get('padding', 4))
            LOGGER.info(f'{type(self).__name__} _get - sequence_name: {sequence_name}, prefix: {prefix}')

            # Sequence 생성
            seq_value = get_next_seq_value(name=sequence_name, prefix=prefix, padding=padding)
            return_data['data'] = seq_value

            return Response(return_data, status.HTTP_200_OK)
        except Exception as ex:
            LOGGER.exception(ex)
            return_data['success'] = False
            return_data['code'] = -1
            return_data['message'] = '예외 발생'
            return_data['data'] = traceback.format_exc()
            return Response(return_data, status.HTTP_400_BAD_REQUEST)
