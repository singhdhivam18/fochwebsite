"""
Role-Based Access Middleware  —  JWT Version
=============================================
No Django ORM / django_session table required.
Works entirely with a signed JWT stored as an HttpOnly cookie.

How it works:
  1. User logs in  ->  server creates a JWT, sets it as cookie 'foch_token'
  2. Every request  ->  middleware reads the cookie, verifies the signature
  3. If valid       ->  user_type extracted from token payload, access checked
  4. If invalid/missing -> redirect to /login (or 401 for API calls)

Student  -> only /dashboard and /logout_user
Volunteer -> everything
"""

import jwt
from django.http import JsonResponse
from django.shortcuts import redirect
from django.conf import settings

# -- Public paths (no token required) --
PUBLIC_PATHS = {
    '/login',
    '/register',
    '/login_user',
    '/register_user',
}

# -- Paths a STUDENT is allowed to reach --
STUDENT_ALLOWED_PATHS = {
    '/dashboard',
    '/logout_user',
    '/api',          # dashboard summary API - students need this for the page
}


def _is_api_request(request):
    """True for AJAX / fetch / /api/* calls that expect JSON back."""
    accept       = request.META.get('HTTP_ACCEPT', '')
    content_type = request.META.get('CONTENT_TYPE', '')
    is_ajax      = request.META.get('HTTP_X_REQUESTED_WITH', '') == 'XMLHttpRequest'
    return (
        is_ajax
        or 'application/json' in accept
        or 'application/json' in content_type
        or request.path.startswith('/api')
    )


class RoleBasedAccessMiddleware:
    """
    JWT-based middleware - no database needed, no ORM dependency.

    Flow:
        1. Allow static / media files through.
        2. Allow public paths (login page, register, etc.) through.
        3. Read JWT from the 'foch_token' HttpOnly cookie.
        4. Verify signature with settings.JWT_SECRET_KEY.
        5. Apply role rules: student -> limited access, volunteer -> full access.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.rstrip('/')  # strip trailing slash for clean matching
        if path == '':
            path = '/'

        # -- 1. Static / media always pass --
        if path.startswith('/static') or path.startswith('/media'):
            return self.get_response(request)

        # -- 2. Public paths always pass --
        if path in PUBLIC_PATHS:
            return self.get_response(request)

        # -- 3. Read and verify JWT from cookie --
        token = request.COOKIES.get('foch_token')

        if not token:
            return self._unauthenticated(request)

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            return self._unauthenticated(request, reason='Session expired. Please log in again.')
        except jwt.InvalidTokenError:
            return self._unauthenticated(request, reason='Invalid session. Please log in again.')

        # -- 4. Attach decoded payload to request for views to use --
        request.jwt_payload = payload          # e.g. payload['username'], payload['user_type']
        user_type = payload.get('user_type', 'student')

        # -- 5. Role-based access check --
        if user_type == 'student':
            allowed = any(
                path == p or path.startswith(p + '/')
                for p in STUDENT_ALLOWED_PATHS
            )
            if not allowed:
                if _is_api_request(request):
                    return JsonResponse(
                        {
                            'error': 'Access denied. Students can only access the dashboard.',
                            'user_type': 'student'
                        },
                        status=403
                    )
                return redirect('/dashboard?access_denied=1')

        # Volunteers pass through to everything
        return self.get_response(request)

    # -- Helpers --

    def _unauthenticated(self, request, reason='Authentication required. Please log in.'):
        if _is_api_request(request):
            return JsonResponse({'error': reason}, status=401)
        return redirect('/login')