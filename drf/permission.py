from rest_framework.permissions import BasePermission


class SuperPermission(BasePermission):
    # 重写里面的has_permission函数
    def has_permission(self, request, view):
        # 判断当前用户是不是超管
        return request.user.is_superuser


class StaffPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff
