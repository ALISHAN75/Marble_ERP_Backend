from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
# models
from accounts.model.Account import User
# serializers
from accounts.serializer.UsersSerializer import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer, UserSerializer

# Generate Token Manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id

        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        read_serializer = UserSerializer(user)
        token = get_tokens_for_user(user)
        return Response({'token': token, 'user': read_serializer.data, 'msg': 'Registration Successful'  ,  'msg_ur': 'رجسٹریشن کامیاب'  }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            user_serialzier = UserSerializer(user)
            permissions = list(user.get_group_permissions())
            user_serialzier
            token = get_tokens_for_user(user)
            return Response({'token': token, 'user': user_serialzier.data, "permissions": permissions, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':  'Email or Password is not Valid' , 'error_ur':  'ای میل یا پاس ورڈ درست نہیں ہے۔' }, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        serializer.data["user_permissions"] = list(
            request.user.get_group_permissions())
        return Response({'user': serializer.data, 'permissions': list(request.user.get_group_permissions())}, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully' , 'msg_ur': 'پاس ورڈ کامیابی سے تبدیل ہو گیا۔'  }, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link send. Please check your Email' , 'msg_ur': 'پاس ورڈ ری سیٹ لنک بھیجیں۔ براہ کرم اپنا ای میل چیک کریں۔' }, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully' , 'msg_ur': 'پاس ورڈ کامیابی سے دوبارہ ترتیب دیا گیا۔' }, status=status.HTTP_200_OK)


class UsersListView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            query_set = User.objects.all()
        except User.DoesNotExist:
            Response({'error': 'The User does not exist.'  , 'error_ur': 'صارف موجود نہیں ہے۔'}, status=status.HTTP_404_NOT_FOUND)
        user_serialzier = UserSerializer(query_set, many=True)
        return Response(user_serialzier.data, status=status.HTTP_200_OK)


class UsersByGroupListView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def get(self, request, format=None, group_name=None):
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            Response({'error': 'The Group does not exist.'  , 'error_ur': 'گروپ موجود نہیں ہے۔'}, status=status.HTTP_404_NOT_FOUND)
        try:
            query_set = User.objects.filter(groups__name=group.name)
        except User.DoesNotExist:
            Response({'error': 'The User does not exist.'  , 'error_ur': 'صارف موجود نہیں ہے۔'}, status=status.HTTP_404_NOT_FOUND)
        user_serialzier = UserSerializer(query_set, many=True)
        return Response(user_serialzier.data, status=status.HTTP_200_OK)


class UsersDetailView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def get(self, request, id=None):
        if id:
            try:
                queryset = User.objects.get(id=id)
            except User.DoesNotExist:
                Response({'error': 'The User Detail does not exist.'  , 'error_ur': 'صارف کی تفصیل موجود نہیں ہے۔' }, status=status.HTTP_404_NOT_FOUND)
            user_serialzier = UserSerializer(queryset)
            return Response(user_serialzier.data, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def put(self, request, id=None):
        try:
            user_to_update = User.objects.get(id=id)
        except User.DoesNotExist:
            Response({'error': 'The User does not exist.'  , 'error_ur': 'صارف موجود نہیں ہے۔'}, status=status.HTTP_404_NOT_FOUND)

        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id

        update_serializer = UserRegistrationSerializer(
            user_to_update, data=request.data)
        if update_serializer.is_valid(raise_exception=True):
            updated_user = update_serializer.save()
        read_serializer = UserRegistrationSerializer(updated_user)
        # token = get_tokens_for_user(user)
        # return Response({'token':token, 'user': read_serializer.data , 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
        # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'success' : "Account is updated successfully" ,  'success_ur' : "اکاؤنٹ کامیابی کے ساتھ اپ ڈیٹ ہو گیا ہے۔" } , status=status.HTTP_200_OK)