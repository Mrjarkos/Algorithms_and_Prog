# context_processors.py
def user_auth_status(request):
    return {'user_authenticated': request.user.is_authenticated}
