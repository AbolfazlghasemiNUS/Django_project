from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from blog.views import HomeView, goodbye_view
from django.conf import settings
from django.conf.urls.static import static
from blog.views import PostDetailView
from django.urls import path, include
from django.urls import path
from blog.views import signup_view






urlpatterns = [
    
    path('signup/', signup_view, name='signup'),

    path("home/", HomeView.as_view(), name="home"),
    
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    
    path("admin/", admin.site.urls),
    
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    path("goodbye/", goodbye_view, name="goodbye"),
    
    path("", RedirectView.as_view(url="/home/", permanent=True)),
    
    path('accounts/', include('django.contrib.auth.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
