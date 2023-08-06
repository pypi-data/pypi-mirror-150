from django.contrib import admin

from common.models.basecode import CmCodeMaster, CmCodeDetail


# Register your models here.
@admin.register(CmCodeMaster)
class CmCodeMasterAdmin(admin.ModelAdmin):
    list_display = ['cm_code_type_id', 'cm_code_type_name', 'system_yn', 'remark']
    # list_display_links = ['cm_code_type_id']
    # list_editable = ['cm_code_type_name', 'system_yn', 'remark']
    # list_filter = ['cm_code_type_id', 'cm_code_type_name']
    search_fields = ['cm_code_type_id', 'cm_code_type_name']


@admin.register(CmCodeDetail)
class CmCodeDetailAdmin(admin.ModelAdmin):
    # 목록에 표시할 칼럼
    list_display = ['cm_code_type_id', 'detail_code_id', 'detail_code_name', 'sort_seq', 'use_yn',
                    'etc_ctnt1', 'etc_ctnt2', 'etc_ctnt3', 'etc_ctnt4', 'etc_ctnt5', 'etc_desc']
    # 상세 페이지로 이동할 링크를 설정할 칼럼
    list_display_links = ['cm_code_type_id', 'detail_code_id', 'detail_code_name']
    # 리스트에서 편집 가능한 칼럼
    # list_editable = ['detail_code_name', 'sort_seq', 'use_yn',
    #                  'etc_ctnt1', 'etc_ctnt2', 'etc_ctnt3', 'etc_ctnt4', 'etc_ctnt5', 'etc_desc']
    # 검색 적용할 칼럼
    search_fields = ['cm_code_type_id', 'detail_code_id', 'detail_code_name']

