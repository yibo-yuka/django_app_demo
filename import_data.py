import os
import sys
import django
import pandas as pd
import re
from pathlib import Path

# --- 動態設定 Django 環境 ---
# 將腳本所在的目錄加到 Python 的搜尋路徑中
# 這樣不論從哪裡執行，都可以找到 mysite 專案
# 注意：這裡假設 import_data.py 和 manage.py 在同一個目錄下
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# 將 'mysite' 替換為您的 Django 專案名稱
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
# --- Django 環境設定完畢 ---

from numbeo.models import CostOfLiving

def clean_value(value):
    """
    清理字串中的非數字字元 (除了小數點)。
    例如： "2,603.41 NT$" -> "2603.41"
    """
    if isinstance(value, str):
        # 移除貨幣符號、千分位逗號和空格
        cleaned_value = re.sub(r'[^\d.]', '', value)
        try:
            # 嘗試轉換為浮點數
            return float(cleaned_value)
        except (ValueError, TypeError):
            # 如果轉換失敗，返回 None
            return None
    # 如果值本身就是數字，直接返回
    return value


def import_data_from_xlsx(filepath):
    """
    從 xlsx 檔案讀取資料並存入資料庫
    """
    # 讀取 xlsx
    df = pd.read_excel(filepath)
    df = df.replace(" ", "")  # 將" "替換為空字串
    df = df.replace("NT$", "")  # 將"NT$"替換為空字串
    cols = df.columns.tolist()
    #print("原始資料欄位：", cols)
    for c in cols[1:-1]:
        df[c] = [i[:-4] for i in df[c]]
        df[c] = df[c].str.replace(",","")
        df[c] = pd.to_numeric(df[c],errors = "coerce")
    
    # 只取用水果相關column
    fruit_cols = ['Apples (1kg)', 'Banana (1kg)', 'Oranges (1kg)', 'Tomato (1kg)']
    df = df[['CountryName'] + fruit_cols ]
    # 將欄位名稱映射到模型的欄位名稱
    column_mapping = {
        'CountryName': 'country_name',
        'Apples (1kg)': 'apples_1kg',
        'Banana (1kg)': 'banana_1kg',
        'Oranges (1kg)': 'oranges_1kg',
        'Tomato (1kg)': 'tomato_1kg',
    }
    # 將 DataFrame 的欄位名稱轉換為 Django 模型的欄位名稱
    df.rename(columns=column_mapping, inplace=True)
    print(df.info())
    # 遍歷 DataFrame 的每一行
    for index, row in df.iterrows():
        # 將 row 轉換為字典
        data = row.to_dict()
        
        # 使用 update_or_create 來避免重複創建
        # 它會嘗試用 country_name 找到物件，如果找到就更新，沒找到就創建
        CostOfLiving.objects.update_or_create(
            country_name=data['country_name'],
            defaults=data
        )
        print(f"已處理: {data['country_name']}")

    print("資料匯入完成！")

if __name__ == '__main__':
    xlsx_file_path = 'cost_of_global(in TWD_cleaned).xlsx'
    import_data_from_xlsx(xlsx_file_path)
