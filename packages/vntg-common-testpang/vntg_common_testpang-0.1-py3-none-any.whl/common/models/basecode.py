from django.db import models

from core.models import BaseTableModel


class CmCodeDetail(BaseTableModel):
    cm_code_type_id = models.CharField(max_length=10)
    detail_code_id = models.CharField(primary_key=True, max_length=10)
    detail_code_name = models.CharField(max_length=100)
    sort_seq = models.IntegerField(blank=True, null=True)
    use_yn = models.CharField(max_length=1)
    etc_ctnt1 = models.CharField(max_length=20, blank=True, null=True)
    etc_ctnt2 = models.CharField(max_length=20, blank=True, null=True)
    etc_ctnt3 = models.CharField(max_length=20, blank=True, null=True)
    etc_ctnt4 = models.CharField(max_length=20, blank=True, null=True)
    etc_ctnt5 = models.CharField(max_length=20, blank=True, null=True)
    etc_desc = models.CharField(max_length=1000, blank=True, null=True)
    valid_start_date = models.DateField(blank=True, null=True)
    valid_end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cm_code_detail'
        # unique_together = (('cm_code_type_id', 'detail_code_id'),)
        constraints = [
            models.UniqueConstraint(fields=['cm_code_type_id', 'detail_code_id'], name='code_master_detail')
        ]


class CmCodeMaster(BaseTableModel):
    # 모델 관리자
    # class CustomModelManager(models.Manager):
    #     def get_queryset(self):
    #         # 삭제처리한 행은 아예 Select되지 않도록 처리
    #         return super().get_qeuryset().filter(delete_yn='N')

    cm_code_type_id = models.CharField(primary_key=True, max_length=10)
    cm_code_type_name = models.CharField(max_length=100)
    parent_code_type_id = models.CharField(max_length=10, blank=True, null=True)
    cm_code_length = models.IntegerField(blank=True, null=True)
    system_yn = models.CharField(max_length=1, blank=True, null=True)
    remark = models.CharField(max_length=500, blank=True, null=True)
    delete_yn = models.CharField(max_length=1, blank=True, null=True)

    # objects = models.Manager()
    # objects = CustomModelManager()

    class Meta:
        managed = False
        db_table = 'cm_code_master'

