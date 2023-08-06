from django.db import models

from core.models import BaseTableModel


class CmGroupUsers(BaseTableModel):
    group_sno = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'cm_group_users'
        # PK 칼럼 그룹 설정
        constraints = [
            models.UniqueConstraint(fields=['group_sno', 'user_id'], name='group_users')
        ]


class CmUserRole(BaseTableModel):
    user_id = models.CharField(primary_key=True, max_length=20)
    role_no = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'cm_user_role'
        # PK 칼럼 그룹 설정
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'role_no'], name='user_role')
        ]


class CmGroupAuth(BaseTableModel):
    group_sno = models.IntegerField(primary_key=True)
    run_sno = models.IntegerField()
    use_yn = models.CharField(max_length=1, blank=True, null=True, default='N')
    select_yn = models.CharField(max_length=1, blank=True, null=True, default='N')
    save_yn = models.CharField(max_length=1, blank=True, null=True, default='N')
    print_yn = models.CharField(max_length=1, blank=True, null=True, default='N')
    custom_yn = models.CharField(max_length=1, blank=True, null=True, default='N')

    class Meta:
        managed = False
        db_table = 'cm_group_auth'
        # unique_together = (('group_sno', 'run_sno'),)
        constraints = [
            models.UniqueConstraint(fields=['group_sno', 'run_sno'], name='pk_cm_group_auth')
        ]


class CmUserAuth(BaseTableModel):
    user_id = models.CharField(primary_key=True, max_length=20)
    run_sno = models.IntegerField()
    use_yn = models.CharField(max_length=1, blank=True, null=True, default='N')
    select_yn = models.CharField(max_length=1, blank=True, null=True, default='N')
    save_yn = models.CharField(max_length=1, blank=True, null=True, default='N')
    print_yn = models.CharField(max_length=1, blank=True, null=True, default='N')
    custom_yn = models.CharField(max_length=1, blank=True, null=True, default='N')

    class Meta:
        managed = False
        db_table = 'cm_user_auth'
        # unique_together = (('user_id', 'run_sno'),)
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'run_sno'], name='pk_cm_user_auth')
        ]


class CmUserMenuAuth(models.Model):
    """공사업체 권한 생성을 위해 BaseTableModel 대신 models.Model을 상속 받습니다.
    """
    user_id = models.CharField(primary_key=True, max_length=20)
    menu_tree_sno = models.CharField(max_length=10)
    parent_menu_tree_sno = models.CharField(max_length=10)
    menu_sno = models.IntegerField()
    run_sno = models.IntegerField()
    menu_path = models.CharField(max_length=100)
    menu_name = models.CharField(max_length=100)
    system_type = models.CharField(max_length=10)
    system_code = models.CharField(max_length=10, blank=True, null=True)
    pgm_id = models.CharField(max_length=20, blank=True, null=True)
    pgm_type = models.CharField(max_length=10, blank=True, null=True)
    pgm_url = models.CharField(max_length=200, blank=True, null=True)
    pgm_param = models.CharField(max_length=500, blank=True, null=True)
    sort_seq = models.IntegerField(blank=True, null=True)
    tree_level = models.IntegerField(blank=True, null=True)
    use_yn = models.CharField(max_length=1, blank=True, null=True)
    select_yn = models.CharField(max_length=1, blank=True, null=True)
    save_yn = models.CharField(max_length=1, blank=True, null=True)
    print_yn = models.CharField(max_length=1, blank=True, null=True)
    custom_yn = models.CharField(max_length=1, blank=True, null=True)
    auth_kind = models.CharField(max_length=10, blank=True, null=True)
    menu_type = models.CharField(max_length=10, blank=True, null=True)
    first_rg_yms = models.DateTimeField(blank=True, null=True)
    first_rg_idf = models.CharField(max_length=20, blank=True, null=True)
    last_update_yms = models.DateTimeField(blank=True, null=True)
    last_update_idf = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cm_user_menu_auth'
        # unique_together = (('user_id', 'menu_tree_sno'),)
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'menu_tree_sno'], name='pk_cm_user_menu_auth')
        ]
