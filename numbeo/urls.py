"""
from django.urls import path
from . import views

urlpatterns = [
    # 當使用者訪問 /my_app/select/ 時，會觸發 views.py 中的 country_select_view 函式
    path('', views.index, name='index'),
    path('select/', views.country_select_view, name='country_select_view'),
]
"""
# numbeo/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CostOfLivingViewSet

# 建立一個路由器 (Router)
router = DefaultRouter()
# 註冊我們的視圖集，並設定 URL 的前綴為 'costs'
router.register(r'costs', CostOfLivingViewSet, basename='costofliving')

# API 的 URL 模式會由路由器自動產生
urlpatterns = [
    path('', include(router.urls)),
]
