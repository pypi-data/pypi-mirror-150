from django.db import models

from core.models import BaseTableModel
from common.utils import get_next_seq_value

# 사용자 레벨
USER_LEVEL_CHOICES = [
    (0, 'admin'),
    (1, 'staff'),
    (5, 'user'),
]


class CmUser(BaseTableModel):
    user_id = models.CharField(primary_key=True, max_length=20)
    user_name = models.CharField(max_length=100)
    # 비밀번호는 생성시 기본 비밀번호로 설정 - 비밀번호 칼럼을 조회 금지
    pwd = models.CharField(max_length=200)
    system_type = models.CharField(max_length=10)
    user_level = models.IntegerField(default=5, choices=USER_LEVEL_CHOICES)
    use_yn = models.CharField(max_length=1, blank=True, null=True, default='N')
    emp_no = models.CharField(max_length=20, blank=True, null=True)
    tel_no = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    remark = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cm_user'


class CmGroup(BaseTableModel):
    group_sno = models.IntegerField(primary_key=True)
    # group_sno = models.AutoField(primary_key=True,
    #                              default=get_next_seq_value(name='cm_group', prefix='none', padding=-1))
    group_name = models.CharField(max_length=100)
    system_type = models.CharField(max_length=10)
    use_yn = models.CharField(max_length=1, blank=True, null=True, default='N')
    remark = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cm_group'

    def save(self, *args, **kwargs):
        super(CmGroup, self).save(*args, **kwargs)


class CmRole(BaseTableModel):
    role_no = models.CharField(primary_key=True, max_length=20)
    role_type = models.CharField(max_length=20)
    role_name = models.CharField(max_length=100)
    system_yn = models.CharField(max_length=1, blank=True, null=True)
    use_yn = models.CharField(max_length=1, blank=True, null=True)
    remark = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cm_role'
