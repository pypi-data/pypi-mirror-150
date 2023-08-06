from core.helper import model_helper

from common.models.basecode import CmCodeMaster, CmCodeDetail

"""
    공통코드 조회 Helper

    Usage:
        from common.helper import basecodehelper

        basecodehelper.get_basecode_list('CM10', ['corp_code', 'busi_place'])
"""


def get_basecode_list(code_type: str, use_yn: str = 'Y', columns: list = None, order_by: list = None) -> list:
    """공통코드유형의 공통코드 목록을 조회합니다.

    사용여부의 기본값은 'Y'입니다.
    정렬 조건은 다음과 같이 작성합니다.

    - sort_seq 내림차순 정렬, etc_ctnt1 오른차순 정렬 ['-sort_seq', 'etc_ctnt1']

    :param code_type: 공통코드유형
    :param use_yn: 사용여부 - 기본 : 'Y'
    :param columns: 조회하고자 하는 컬럼들
    :param order_by: 정렬 조건
    """
    # 조회조건
    filter_data = {
        'cm_code_type_id': code_type,
        'use_yn': use_yn,
    }
    # 조회
    result_list = model_helper.get_list(model=CmCodeDetail, filter_data=filter_data, columns=columns, order_by=order_by)

    return result_list


def get_basecode_row(code_type: str, code: str, columns: list = None) -> dict:
    """공통코드유형의 공통코드에 해당하는 단일행을 조회합니다.

    :param code_type: 공통코드유형
    :param code: 공통코드
    :param columns: 조회하고자 하는 컬럼들
    """
    # 조회조건
    filter_data = {
        'cm_code_type_id': code_type,
        'detail_code_id': code,
    }
    # 조회
    result_row = model_helper.get_row(model=CmCodeDetail, filter_data=filter_data, columns=columns)

    return result_row


def get_basecode_name(code_type: str, code: str) -> str:
    """공통코드유형의 공통코드에 해당하는 코드명을 조회합니다.

    :param code_type: 공통코드유형
    :param code: 공통코드
    """
    # 조회조건
    filter_data = {
        'cm_code_type_id': code_type,
        'detail_code_id': code,
    }
    # 조회
    result_value = model_helper.get_value(model=CmCodeDetail, filter_data=filter_data, column='detail_code_name')

    return result_value
