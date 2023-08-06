from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from common.views.authentication import UserGroupView, UserRoleView, UserMenuView
from common.views.login import LoginView, CustLoginView
from common.views.search_account import FindIdView, FindPasswordView, ResetPasswordView

default_get_action = {'post': 'get'}


urlpatterns = [
    # Login (token 발행)을 위한 별도 urls (core 에서 여기로 이동함)
    path('login', LoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # Login 아이디 / 비밀번호 찾기, 초기화
    path('find-id/', FindIdView.as_view({'post': 'get_find_id'})),
    path('find-pw/', FindPasswordView.as_view({'post': 'get_find_pw'})),
    path('init-pw/', ResetPasswordView.as_view({'post': 'reset_pw'})),
    # 공사업체 로그인
    path('cust-login', CustLoginView.as_view(), name='token_obtain_pair'),
    # 권한 관련
    path('auth/group/', UserGroupView.as_view(default_get_action)),
    path('auth/role/', UserRoleView.as_view(default_get_action)),
    path('auth/role/<str:role_no>', UserRoleView.as_view({'post': 'get_auth_role'})),
    path('auth/menu/', UserMenuView.as_view(default_get_action)),
    path('auth/menu/<int:run_sno>', UserMenuView.as_view({'post': 'get_auth_menu'})),
]
