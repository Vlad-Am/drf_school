from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny

from users.models import User, Pays
from users.serializer import UserSerializer, PaymentSerializer
from users.services import create_price, create_stripe_session, create_product


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        strip_prod_id = create_product(payment)
        strip_price_id = create_price(payment, strip_prod_id)
        payment.link, payment.payment_id = create_stripe_session(strip_price_id)
        payment.save()


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
