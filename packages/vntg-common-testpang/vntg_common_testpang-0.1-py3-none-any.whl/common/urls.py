from django.urls import path

from .views.authentication import UserGroupView, GroupUsersView, UserRoleView, UserGroupRoleCheckView, \
    UserMenuAuthCreateView
from .views.dashboard import CmDashboardView
from .views.user_group import UserListView, UserView, GroupView, RoleView, UserDetailView
from .views.corporation import CmCorporationView, CmBusiplaceView
from .views.employee import CmEmployeeView, CmDepartmentView
from .views.basecode import CodeMasterView, CodeDetailView, CodeListView
from .views.program_menu import UserMainMenuView, ProgramView, UserMyMenuView
from .views.sequence import SequenceView
from .views.test_views import TemplateDummyListView,  MetaInfoView

# from .views.test_views import TemplateDummyFileView

default_get_action = {'post': 'get'}
default_post_action = {'post': 'save'}

"""공통 api endpoint 설정
- /api/common/로 시작
- 조회의 경우, View클래스.as_view({'post':'메서드이름'}) 으로 작성
- 저장의 경우, View클래스.as_view({'post':'save'}) 으로 작성
"""
urlpatterns = [
    # path('common/', include('rest_framework.urls', namespace='rest_framework')),
    # 사용자 정보
    path('user/', UserListView.as_view(default_get_action)),
    path('user/<str:user_id>', UserView.as_view(default_get_action)),
    path('user-detail/', UserDetailView.as_view(default_get_action)),
    path('user-info/', UserDetailView.as_view(default_post_action)),
    # 그룹/Role 정보
    path('group/', GroupView.as_view(default_get_action)),
    path('role/', RoleView.as_view(default_get_action)),
    # 권한 관련
    path('group/<int:group_sno>/users/', GroupUsersView.as_view(default_get_action)),
    path('auth/group/', UserGroupView.as_view(default_get_action)),
    # path('auth/<str:user_id>/group/<int:group_sno>', UserGroupRoleCheckView.as_view({'post': 'check_group'})),
    path('auth/role/', UserRoleView.as_view(default_get_action)),
    # path('auth/<str:user_id>/role/<str:role_no>', UserGroupRoleCheckView.as_view({'post': 'check_role'})),
    path('auth/create/', UserMenuAuthCreateView.as_view(default_post_action)),
    # 법인/사업장 정보
    path('corporation/', CmCorporationView.as_view(default_get_action)),
    path('busi-place/', CmBusiplaceView.as_view(default_get_action)),
    # 사원/부서 정보
    path('employee/', CmEmployeeView.as_view(default_get_action)),
    path('emp-detail/', CmEmployeeView.as_view({'post': 'get_emp_detail'})),
    path('dept/', CmDepartmentView.as_view(default_get_action)),
    # 공통코드 - 코드정의 정보, 코드 리스트, 코드 정보
    path('code/<str:cm_code_type_id>', CodeMasterView.as_view(default_get_action)),
    path('code/<str:cm_code_type_id>/list/', CodeDetailView.as_view({'post': 'get_list'})),
    path('code/<str:cm_code_type_id>/detail/<str:detail_code_id>', CodeDetailView.as_view({'post': 'get_detail'})),
    # 공통코드 전체 리스트
    path('codelist/', CodeListView.as_view({'post': 'get_list'})),
    # 프로그램/메뉴
    path('program/', ProgramView.as_view(default_get_action)),
    # 사용자 메인메뉴
    path('user/main-menu/', UserMainMenuView.as_view(default_get_action)),
    path('user-menu/', UserMyMenuView.as_view({'post': 'get_user_my_menu'})),
    # 채번
    path('sequence/', SequenceView.as_view({'post': 'get_next_sequence'})),
    # 대시보드 차트 #1
    path('dashboard/chart1/', CmDashboardView.as_view({'post': 'get_chart1'})),
    # 대시보드 차트 #3
    path('dashboard/chart3/', CmDashboardView.as_view({'post': 'get_chart3'})),
]

urlpatterns += [
    path('template', TemplateDummyListView, name='template'),
    # path('templatefile', TemplateDummyFileView, name='templatefile'),
    path('meta-info', MetaInfoView.as_view(default_get_action)),
]
