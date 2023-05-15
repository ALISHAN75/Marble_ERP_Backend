from rest_framework import permissions


class IsUserAllowed(permissions.BasePermission):
    permission_codename = []

    def __init__(self, permission_codename):
        super().__init__()
        self.permission_codename = permission_codename

    def __call__(self):
        return self

    def has_permission(self, request, view):
        permissionList = list(request.user.get_group_permissions())

        if request.method == 'POST':
            return_value = self.permission_codename['POST'] in permissionList or request.user.is_staff
        elif request.method == 'PUT':
            return_value = self.permission_codename['PUT'] in permissionList or request.user.is_staff
        elif request.method == 'DELETE':
            return_value = self.permission_codename['DELETE'] in permissionList or request.user.is_staff
        elif request.method == 'GET':
            return_value = self.permission_codename['GET'] in permissionList or request.user.is_staff

        # return_value = self.permission_codename in permissionList or request.user.is_staff
        return return_value


# # second way
# class IsUserAllowed(permissions.BasePermission):
#     permission_codename = ""

#     def has_permission(self, request, view):
#         # return request.user.has_permission(self.permission_codename)
#         if request.user and request.user.groups.filter(name="Customer") or request.user.is_staff:
#             return True
#         return False

# def UserHasPermission(permission_codename):
#     return type('IsUserAllowed', (IsUserAllowed, ), {'permission_codename': permission_codename})
