from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
                  path('home/', views.home, name='home'),
                  path('signup/', views.signup_user, name='signup'),
                  path('login/', views.login_user, name='login'),
                  path('handlesignup/', views.handleSignup, name='handleSignup'),
                  path('handlelogin/', views.handleLogin, name='handleLogin'),
                  path('logout/', views.handleLogout, name='handleLogout'),
                  path('addtocart/', views.addToCart, name='addToCart'),
                  path('cart/', views.viewCart, name='viewCart'),
                  path('setsession/', views.setSession, name='setSession'),
                  path('add/', views.add_item_by_one, name='add_item_by_one'),
                  path('sub/', views.reduce_item_by_one, name='reduce_item_by_one'),
                  path('checkout/', views.checkout, name='checkout'),
                  path('placeorder/', views.placeOrder, name='placeOrder'),
                  path('remove/', views.removeItem, name='removeItem'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
