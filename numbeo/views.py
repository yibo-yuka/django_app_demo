from django.http import HttpResponse
import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the Numbeo index.")

def country_select_view(request):
    # 因為資料是寫死的，所以 view 函式不需要傳遞任何資料
    return render(request, 'numbeo/country_form.html')

# numbeo/views.py
from rest_framework import viewsets
from .models import CostOfLiving
from .serializers import CostOfLivingSerializer

class CostOfLivingViewSet(viewsets.ModelViewSet):
    """
    這個視圖集 (ViewSet) 會自動提供 'list' (GET), 'retrieve' (GET), 
    'update' (PUT), 'partial_update' (PATCH), 和 'destroy' (DELETE) 操作。
    我們主要會使用到 GET 和 PUT。
    """
    queryset = CostOfLiving.objects.all()
    serializer_class = CostOfLivingSerializer
    # 我們使用 'country_name' 作為查找的欄位
    lookup_field = 'country_name'
    