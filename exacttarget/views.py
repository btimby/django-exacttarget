from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    try:
        if request.method != 'POST':
            raise PermissionDenied('Only accessible via ExactTarget SSO')
        try:
            user = authenticate(**request.POST.dict())
        except KeyError:
            raise PermissionDenied('Missing JWT')
        auth_login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
    except PermissionDenied, e:
        return render(request, '403.html', {'reason': str(e)}, status=403)
