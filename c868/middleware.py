from django.core.exceptions import PermissionDenied

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        cbv = getattr(view_func, 'cbv', None)
        if cbv:
            if hasattr(cbv, 'allowed_roles'):
                allowed_roles = cbv.allowed_roles
                user = request.user
                if request.user.is_authenticated:
                    if not user.role.name in allowed_roles:
                        print(user)
                        print(user.role)
                        print(allowed_roles)
                        raise PermissionDenied()