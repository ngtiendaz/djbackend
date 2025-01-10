from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.authtoken')),


    path("api/product/",include("core.urls")),
    path("api/address/",include("extras.urls")),
    path("api/orders/",include("order.urls")),
    path("api/newcart/",include("newcart.urls")),
    path("api/newwishlist/",include("newwishlist.urls")),
    path("api/notification/",include("notification.urls")),
    path("api/rating/",include("rating.urls"))
    
    
]
