from django.db import models

from core.models import NullCharField


class CmLogLogin(models.Model):
    log_sno = models.AutoField(primary_key=True)
    log_date = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=20)
    login_date = models.DateTimeField(blank=True, null=True)
    http_user_agent = NullCharField(max_length=1000, blank=True, null=True)
    remote_addr = NullCharField(max_length=50, blank=True, null=True)
    remote_host = NullCharField(max_length=100, blank=True, null=True)
    remote_user = NullCharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cm_log_login'


class CmExecLog(models.Model):
    id = models.AutoField(primary_key=True)
    exec_time = models.DateTimeField()
    exec_pgm = NullCharField(max_length=100, blank=True, null=True)
    remark = NullCharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cm_exec_log'
