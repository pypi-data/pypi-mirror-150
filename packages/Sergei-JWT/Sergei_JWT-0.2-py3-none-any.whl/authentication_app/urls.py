from django.urls import path

from authentication_app.views import Health, Generate, Validate, Refresh, Test, Revoke


urlpatterns = [
    path('health', Health.as_view()),
    path('generate', Generate.as_view()),
    path('validate', Validate.as_view()),
    path('refresh', Refresh.as_view()),
    path('test', Test.as_view()),
    path('revoke', Revoke.as_view()),
]
