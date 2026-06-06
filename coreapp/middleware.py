from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# ✅ Decorator to check user_type
def check_user_type(allowed_types):
    """
    Decorator to check if user has required user_type

    Usage:
        @check_user_type(['volunteer'])           # Only volunteers
        @check_user_type(['volunteer', 'admin'])  # Volunteers or admins
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Get user_type from session
            user_type = request.session.get('user_type')
            username  = request.session.get('username')

            # Not authenticated → 401
            if not user_type or not username:
                return JsonResponse({
                    "success":  False,
                    "error":    "❌ Not authenticated. Please login first.",
                    "redirect": "/login"
                }, status=401)

            # Wrong user type → 403
            if user_type not in allowed_types:
                return JsonResponse({
                    "success":       False,
                    "error":         f"❌ Access Denied! {user_type.upper()} users cannot access this feature.",
                    "allowed_types": allowed_types,
                    "user_type":     user_type
                }, status=403)

            print(f"✅ Access granted to {user_type} user: {username}")
            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator


# ✅ Decorator for ANY logged-in user (student OR volunteer)
def check_authenticated(view_func):
    """Allow any logged-in user regardless of user_type."""
    def wrapper(request, *args, **kwargs):
        user_type = request.session.get('user_type')
        username  = request.session.get('username')

        if not user_type or not username:
            return JsonResponse({
                "success":  False,
                "error":    "❌ Not authenticated. Please login first.",
                "redirect": "/login"
            }, status=401)

        print(f"✅ Authenticated access: {user_type} user ({username})")
        return view_func(request, *args, **kwargs)

    return wrapper
