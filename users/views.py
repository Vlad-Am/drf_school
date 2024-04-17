from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from users.models import User, Pays
from users.serializer import UserSerializer, PaymentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer


class DjangoFilterBackend:
    pass


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Pays.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date']
    filterset_fields = ['course', 'payment_method']


class PaymentRetrieveAPIView(RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Pays.objects.all()


class PaymentUpdateAPIView(UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Pays.objects.all()


class PaymentDestroyAPIView(DestroyAPIView):
    queryset = Pays.objects.all()
