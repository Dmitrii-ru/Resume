from django.contrib import admin
from django.contrib.auth.views import PasswordResetView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authViews
from user_app.views import CustomPasswordResetView
from user_app.forms import EmailValidationPasswordResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('resume.urls', namespace='resume_urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('user/', include('user_app.urls', namespace='user_urls')),
    path('mptt_blog/', include('mptt_blog.urls', namespace='mptt_blog_urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('quiz/', include('quiz.urls', namespace='quiz_urls')),

    path('_nested_admin/', include('nested_admin.urls')),
    path('user/pass-reset/',
         CustomPasswordResetView.as_view(
             template_name='user_app/pass-reset.html',
             email_template_name="user_app/password_reset_form.html",
             form_class=EmailValidationPasswordResetView
         ),
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
