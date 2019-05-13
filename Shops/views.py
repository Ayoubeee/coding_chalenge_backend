from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.authentication import  TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser,Shops
from rest_framework.response import Response
from .serializers import ShopSerializer

# Sign Up View.
@api_view(['POST'])
@permission_classes((AllowAny,))
def SignUp(request):
    user=CustomUser.objects.create(
        email=request.POST.get("email"),
        password=request.POST.get("password")
    )
    Token.objects.create(user=user)
    return Response(user.to_dict())

# Sign In View.
@api_view(["POST"])
@permission_classes((AllowAny,))
def SignIn(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    if CustomUser.objects.filter(email=email,password=password):
         token= Token.objects.get(user=CustomUser.objects.get(email=email,password=password))
         return JsonResponse({'token': token.key,'is_login':True,'SignIn':False})
    else:
        return JsonResponse({'token': 'no authorization','is_login':False,'SignIn':True})

@api_view(["GET"])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def is_login(request):
    return JsonResponse({'is_login':True,'email':request.user.email,'SignIn':False})

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def list_shops(request):
    shops=[shop for shop in Shops.objects.filter().order_by('distance')]
    T=[]
    for i in range(len(shops)):
        if shops[i].likes.filter(id=request.user.id).exists()==False:
            T.append(shops[i])

    serializer = ShopSerializer(T, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def list_prefer_shops(request):
    shops=request.user.likes.filter()
    serializer = ShopSerializer(shops, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def like_shop(request):
    shop= Shops.objects.get(id=request.GET.get("id"))
    if shop.likes.filter(id=request.user.id).exists()==False:
        shop.likes.add(request.user)
    return JsonResponse({'success':True})

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def remove_shop(request):
    shop= Shops.objects.get(id=request.GET.get("id"))
    if shop.likes.filter(id=request.user.id).exists():
        shop.likes.remove(request.user)
    return JsonResponse({'success':True})
