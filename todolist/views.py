from rest_framework import viewsets, generics, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Todo
from .serializers import TodoSerializer, RegistrationSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class TodoViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)

    filterset_fields = ['is_completed', 'due_date']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Todo.objects.all()
        return Todo.objects.filter(owner=user)

    # Set the owner to the logged-in user when creating
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # new tokens tied to specific user
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response(
            {
                'id': user.id,
                'username': user.username,
                'access': str(access),
                'refresh': str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )