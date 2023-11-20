from rest_framework import permissions


class IsInstructorPermission(permissions.BasePermission):
    
    '''
    permissons for instructors
    '''

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or \
            (request.user.is_authenticated and request.user.is_instructor)

    def has_object_permisson(self, request, view, obj):
        return obj.instructor == request.user
 

    
class IsStudentPermisson(permissions.DjangoModelPermissions):
    '''
    permissons for students
    ''' 

    def has_permisson(self, request, view):
        return bool(
            request.method not in permissions.SAFE_METHODS and
            request.user and
            request.user.is_student
        )



