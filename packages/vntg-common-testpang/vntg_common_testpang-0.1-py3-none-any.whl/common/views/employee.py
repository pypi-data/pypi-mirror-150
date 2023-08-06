import logging

from rest_framework import permissions
from rest_framework.decorators import action

from core.business import BusinessNode
from core.helper.request_helper import get_emp_no_by_current_user
from core.views.baseview import BaseModelApiView, BaseSqlApiView
from common.models.employee import CmEmployee, CmDepartment
from common.serializers.employee import CmEmployeeSerializer, CmDepartmentSerializer

LOGGER = logging.getLogger(__name__)


class CmEmployeeView(BaseModelApiView):
    """사원 목록

    [Parameters]
    - busi_place: 사업장, 필수
    - dept_code: 부서 코드, 생략가능
    - dept_name: 부서 명, 생략가능
    - emp_name : 사원 명, 생략가능
    """

    def define_nodes(self):
        # 노드 등록
        self._append_node(BusinessNode(node_name='employee', model=CmEmployee, serializer=CmEmployeeSerializer))
        self._append_node(BusinessNode(node_name='emp-detail', model=CmEmployee, serializer=CmEmployeeSerializer))

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        # 조회조건을 추가하기 위해 오버라이딩
        filter_data = {}
        if node.node_name == 'employee':
            filter_data = {
                'busi_place': request_data.get('busi_place', '%'),
                'dept_code': request_data.get('dept_code', '%'),
                # 'dept_name': request_data.get('dept_name', '%'),
                'emp_name': request_data.get('emp_name', '%'),
            }
            # 불필요한 파라미터 제거
            filter_data = {key: value for key, value in filter_data.items() if value is not None and value != '%'}
            # 하위 테이블 조건 유무 확인
            if len(filter_data) == 0:
                raise Exception('조회 조건이 누락되었습니다.')
            return filter_data
        elif node.node_name == 'emp-detail':
            # emp_no가 없으면 현재 사원 정보 사용
            if 'emp_no' in request_data:
                emp_no = request_data.get('emp_no')
            else:
                emp_no = get_emp_no_by_current_user()
            filter_data = {
                'emp_no': emp_no,
            }
            return filter_data

    def _set_query(self, node: BusinessNode, request_data: dict):
        if node.node_name == 'employee':
            filter_data = self._create_filter(node=node, parameter_list=None, request_data=request_data,
                                              include_all=False)

            # Group 이름을 extra()로 조인 조회 - 모델에 foreign key가 설정되어 있지 않은 경우.
            # extra()의 select/tables/where는 실제 query(select/from/where)에 반영된다.
            # URL에서 받은 법인 pk를 이용하여 해당 법인에 속한 사업장을 조회한다.
            node.queryset = node.model.objects.extra(
                select={'dept_name': 'cm_department.dept_name'},
                tables=['cm_department'],
                # where=['cm_department.dept_code=cm_employee.dept_code and cm_department.dept_name Like %s'],
                # params=[request_data.get('dept_name', '%')]
                where=["cm_department.dept_code=cm_employee.dept_code",
                       "( %s = '%%' or ( %s <> '%%' and cm_department.dept_name = %s))"],
                params=[request_data.get('dept_name', '%'),
                        request_data.get('dept_name', '%'),
                        request_data.get('dept_name', '%')],
            ).filter(**filter_data)
        else:
            return super()._set_query(node, request_data)

    @action(detail=False, methods=['post'])
    def get(self, request, *args, **kwargs):
        return self._exec_get(request)

    @action(detail=False, methods=['post'])
    def get_emp_detail(self, request):
        return self._exec_get(request)


class CmDepartmentView(BaseModelApiView):
    """부서 목록

    [Parameters]
    - busi_place: 사업장, 필수
    - parent_dept_code : 상위 부서 코드, 생략가능
    - dept_name : 부서 명, 생략가능
    """

    def define_nodes(self):
        # 노드 등록
        self._append_node(BusinessNode(node_name='dept', model=CmDepartment, serializer=CmDepartmentSerializer))

    def _create_filter(self, node: BusinessNode, parameter_list=None, request_data=None, include_all=False):
        # 조회조건을 추가하기 위해 오버라이딩
        if node.node_name == 'dept':
            filter_data = {
                'busi_place': request_data.get('busi_place', '%'),
                'parent_dept_code': request_data.get('parent_dept_code', '%'),
                'dept_name': request_data.get('dept_name', '%'),
            }
            # 불필요한 파라미터 제거
            filter_data = {key: value for key, value in filter_data.items() if value is not None and value != '%'}
            # 하위 테이블 조건 유무 확인
            if len(filter_data) == 0:
                raise Exception('조회 조건이 누락되었습니다.')
            return filter_data

    @action(detail=False, methods=['post'])
    def get(self, request, *args, **kwargs):
        return self._exec_get(request)
