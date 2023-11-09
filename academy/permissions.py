from rest_framework import permissions


class IsInstructorPermission(permissions.BasePermission):
    '''
    permissons for instructors
    '''

    # def has_permisson(self, request, view):
    #     if not request.user.is_instructor:
    #         return False
    #     return super().has_perm(request, view)

   
    def has_permisson(self, request, view):
         
         user = request.user
         print(user,"kkkk")
         if request.method == "POST":
             return  user.is_instructor
         return False
        #  if request.method == "PUT":
        #      if user.is_instructor :
        #          return True
        #      return False
        #  if request.method == "PATCH":
        #      if user.is_instructor :
        #          return True
        #      return False
        #  if request.method == "DELETE":
        #      if user.is_instructor :
        #          return True
        #      return False


    # def has_object_permisson(self, request, view, obj):
    #     return obj.instructor == request.user


    
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



