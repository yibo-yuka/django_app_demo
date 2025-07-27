# numbeo/serializers.py
from rest_framework import serializers
from .models import CostOfLiving

class CostOfLivingSerializer(serializers.ModelSerializer):
    """
    這個序列化器會將 CostOfLiving 模型實例轉換為 JSON 格式。
    """
    class Meta:
        model = CostOfLiving
        # '__all__' 表示序列化所有模型欄位
        fields = '__all__'
