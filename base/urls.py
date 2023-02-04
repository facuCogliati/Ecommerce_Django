from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("check-out", views.checkOut, name="checkOut"),
    path("order-ended", views.orderEnded, name="order_ended"),

    path("login-user", views.login_user, name="loginUser"),
    path("logout-user", views.logout_user, name="logoutUser"),
    path("register-user", views.register_user, name="registerUser"),

    path("update-order", views.update_order, name="updateOrder"),
    path("eliminate-item", views.eliminateItem, name="eliminateItem"),



    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)