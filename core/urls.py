from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authViews
from user_app.views import CustomPasswordResetView


###APPS###

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('resume.urls', namespace='resume_urls')),
    path('user/', include('user_app.urls', namespace='user_urls')),
    path('mptt_blog/', include('mptt_blog.urls', namespace='mptt_blog_urls')),
    path('quiz/', include('quiz.urls', namespace='quiz_urls')),
]

###API###

urlpatterns += [
    path('v1/resume/', include('resume_api.urls', namespace='resume_api')),
    path('v1/user_app/', include('user_app_api.urls', namespace='user_app_api')),
    path('api/mptt_blog/', include('mptt_blog_api.urls', namespace='mptt_blog_api')),
    path('api/verification_phone/', include('verification_phone_api.urls', namespace='verification_phone_api')),
]

###USER_AUTH###

urlpatterns += [
    path('user/pass-reset/',
         CustomPasswordResetView.as_view(),
         name='pass-reset',
         ),
    path('user/password_reset_confirm/<uidb64>/<token>/',
         authViews.PasswordResetConfirmView.as_view(
             template_name='user_app/password_reset_confirm.html'
         ),
         name='password_reset_confirm'
         ),

    path('user/password_reset_done/',
         authViews.PasswordResetDoneView.as_view(
             template_name='user_app/password_reset_done.html'
         ),
         name='password_reset_done'
         ),

    path('user/password_reset_complete/',
         authViews.PasswordResetCompleteView.as_view(
             template_name='user_app/password_reset_complete.html'
         ),
         name='password_reset_complete'
         ),
]




###ATHER###

urlpatterns += [
    path('_nested_admin/', include('nested_admin.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
