from django.shortcuts import render

# Create your views here.

def index(request):
    if request.method == 'POST':
        accType = request.POST['accType']
        password = request.POST['password']
        email = request.POST['email']

        if accType == 'admin':
            pass
        elif accType == 'seller':
            pass
        elif accType == 'Tester':
            pass
        elif accType == 'user':
            pass
    return render(request, 'tesafe/index.html')