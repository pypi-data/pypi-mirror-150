from datetime import datetime

from django.db import router, transaction

from common.models.sequence import CmSequence


def get_next_seq_value(name: str = 'default', prefix: str = 'default', padding: int = 4):
    """sequence name + prefix에 대한 다음 일련번호를 생성하여 반환합니다.
    padding 값이 음수이면, next_value(int)만 리턴합니다.

    ex) 계약번호 채번
        - sequence name: contract
        - prefix: co2109
        - seq: 5자리 일련번호
        - 호출 get_next_seq_value(name='contract', prefix='co2109', padding=5)
        - return: co210912345

    :param name: Sequence 명
    :param prefix: Sequence 접두사
    :param padding: 일련번호를 0으로 채울 자리수
    :return: prefix + next_seq
    """
    using = router.db_for_write(CmSequence)

    with transaction.atomic(using=using, savepoint=False):
        # key 칼럼이 2개인 경우, get_or_create()는 key duplicate 오류 발생 -> select 확인 / create로 변경
        # sequence_row, created = CmSequence.objects.select_for_update(
        #     nowait=False
        # ).get_or_create(
        #     seq_name=name,
        #     prefix=prefix,
        #     defaults={
        #         'padding': padding,
        #         'last_value': 1
        #     }
        # )

        # sequence row 검색, 없으면 생성
        sequence_row = CmSequence.objects.select_for_update(
            nowait=False
        ).filter(seq_name=name, prefix=prefix).first()

        apply_seq = 0

        if sequence_row is None:
            # sequence row 없음 -> create
            sequence_row = CmSequence.objects.select_for_update(
                nowait=False
            ).create(
                seq_name=name,
                prefix=prefix,
                padding=padding,
                last_value=1
            )
            apply_seq = 1
        else:
            # sequence row 있음 -> update
            # sequence_row.last_value += 1
            # sequence_row.save()
            apply_seq = sequence_row.last_value + 1
            CmSequence.objects.filter(seq_name=name, prefix=prefix).update(last_value=apply_seq)

        if padding >= 0:
            # prefix + seq 로 리턴
            return f'{prefix}{str(apply_seq).zfill(padding)}'
        else:
            # seq 리턴
            return apply_seq
