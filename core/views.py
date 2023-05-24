from http import HTTPStatus
from django.contrib.auth import authenticate, login
from django.http import HttpResponseNotAllowed, JsonResponse



def hello_world(request):
    return JsonResponse({"message": "Hello World!"})

# TODO: Para origens diferentes, isso aqui não vai dar certo : (
# Vai cair no caso do csrf_token, vai ser chato de resolver.
def login_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Method not allowed.")

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse(
        {
            'success': False,
            'message': 'User or password invalid!.'
        }, status=HTTPStatus.UNAUTHORIZED)

    login(request, user)
    return JsonResponse({'success': True, 'message': 'Login success.'})
