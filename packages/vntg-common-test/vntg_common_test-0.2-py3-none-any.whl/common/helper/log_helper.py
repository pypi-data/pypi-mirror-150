import logging
from datetime import datetime

from common.models.log import CmLogLogin, CmExecLog

LOGGER = logging.getLogger(__name__)


# region 로그인 로그

def create_login_log(user_id, request):
    try:
        login_data = {
            'user_id': user_id,
            'login_date': datetime.now().date(),
            'http_user_agent': request.META.get('HTTP_USER_AGENT', 'n/a'),
            'remote_addr': request.META.get('REMOTE_ADDR', 'n/a'),
            'remote_host': request.META.get('REMOTE_HOST', 'n/a'),
            'remote_user': request.META.get('REMOTE_USER', 'n/a'),
        }

        CmLogLogin.objects.create(**login_data)
    except Exception as ex:
        # 오류 무시
        LOGGER.exception(ex)

# endregion


# region 실행 로그

def create_exec_log(exec_pgm: str, desc: str):
    try:
        log_data = {
            'exec_time': datetime.now(),
            'exec_pgm': exec_pgm,
            'remark': desc,
        }

        CmExecLog.objects.create(**log_data)
    except Exception as ex:
        # 오류 무시
        LOGGER.exception(ex)

# endregion
