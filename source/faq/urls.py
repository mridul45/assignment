from rest_framework.routers import DefaultRouter
from faq.api.views import FaqViewset,GptViewset
from django.urls import path, include


router = DefaultRouter()
router.register(r'faq', FaqViewset, basename='faq')
router.register(r'gpt',GptViewset,basename='gpt')


urlpatterns = [
    path('', include(router.urls)),
]