from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from order_api.orders.views import OrderViewSet
from order_api.users.api.views import UserRegistrationViewSet
from order_api.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("registration", UserRegistrationViewSet, basename="user-registration")
router.register("orders", OrderViewSet)


app_name = "api"
urlpatterns = router.urls
