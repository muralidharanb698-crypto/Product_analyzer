from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegisterSerializer
from .models import Register

@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": True,
            "message": "Registration Successful"
        })

    return Response(serializer.errors, status=400)


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = Register.objects.get(email=email, password=password)

        return Response({
            "status": True,
            "message": "Login Successful",
            "name": user.name,
            "email": user.email
        })

    except Register.DoesNotExist:
        return Response({
            "status": False,
            "message": "Invalid Email or Password"
        }, status=401)