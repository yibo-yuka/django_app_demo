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


def import_data_from_csv(filepath):
    """
    從 CSV 檔案讀取資料並存入資料庫
    """
    # 讀取 CSV
    df = pd.read_excel(filepath)

    # 將欄位名稱轉換為 Django model field 的格式 (小寫並用底線分隔)
    column_mapping = {
        'CountryName': 'country_name',
        'Meal, Inexpensive Restaurant': 'meal_inexpensive_restaurant',
        'Meal for 2 People, Mid-range Restaurant, Three-course': 'meal_for_2_people_mid_range_restaurant',
        'McMeal at McDonalds (or Equivalent Combo Meal)': 'mcmeal_at_mcdonalds',
        'Cappuccino (regular)': 'cappuccino_regular',
        'Coke/Pepsi (0.33 liter bottle)': 'coke_pepsi_0_33_liter_bottle',
        'Water (0.33 liter bottle)': 'water_0_33_liter_bottle',
        'Milk (regular), (1 liter)': 'milk_regular_1_liter',
        'Loaf of Fresh White Bread (500g)': 'loaf_of_fresh_white_bread_500g',
        'Rice (white), (1kg)': 'rice_white_1kg',
        'Eggs (regular) (12)': 'eggs_regular_12',
        'Local Cheese (1kg)': 'local_cheese_1kg',
        'Chicken Fillets (1kg)': 'chicken_fillets_1kg',
        'Apples (1kg)': 'apples_1kg',
        'Banana (1kg)': 'banana_1kg',
        'Oranges (1kg)': 'oranges_1kg',
        'Tomato (1kg)': 'tomato_1kg',
        'Potato (1kg)': 'potato_1kg',
        'Onion (1kg)': 'onion_1kg',
        'Lettuce (1 head)': 'lettuce_1_head',
        'Water (1.5 liter bottle)': 'water_1_5_liter_bottle',
        'Cigarettes 20 Pack (Marlboro)': 'cigarettes_20_pack_marlboro',
        'One-way Ticket (Local Transport)': 'one_way_ticket_local_transport',
        'Monthly Pass (Regular Price)': 'monthly_pass_regular_price',
        'Taxi Start (Normal Tariff)': 'taxi_start_normal_tariff',
        'Taxi 1km (Normal Tariff)': 'taxi_1km_normal_tariff',
        'Taxi 1hour Waiting (Normal Tariff)': 'taxi_1hour_waiting_normal_tariff',
        'Gasoline (1 liter)': 'gasoline_1_liter',
        'Volkswagen Golf 1.4 90 KW Trendline (Or Equivalent New Car)': 'volkswagen_golf_1_4_90_kw_trendline',
        'Toyota Corolla Sedan 1.6l 97kW Comfort (Or Equivalent New Car)': 'toyota_corolla_sedan_1_6l_97kw_comfort',
        'Basic (Electricity, Heating, Cooling, Water, Garbage) for 85m2 Apartment': 'basic_electricity_heating_cooling_water_garbage_for_85m2_apartment',
        'Mobile Phone Monthly Plan with Calls and 10GB+ Data': 'mobile_phone_monthly_plan_with_calls_and_10gb_data',
        'Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)': 'internet_60_mbps_or_more_unlimited_data_cable_adsl',
        'Fitness Club, Monthly Fee for 1 Adult': 'fitness_club_monthly_fee_for_1_adult',
        'Tennis Court Rent (1 Hour on Weekend)': 'tennis_court_rent_1_hour_on_weekend',
        'Cinema, International Release, 1 Seat': 'cinema_international_release_1_seat',
        'Preschool (or Kindergarten), Full Day, Private, Monthly for 1 Child': 'preschool_or_kindergarten_full_day_private_monthly_for_1_child',
        'International Primary School, Yearly for 1 Child': 'international_primary_school_yearly_for_1_child',
        '1 Pair of Jeans (Levis 501 Or Similar)': 'one_pair_of_jeans_levis_501_or_similar',
        # --- 已修正 ---
        '1 Summer Dress in a Chain Store (Zara, H&M, ...)': 'one_summer_dress_in_a_chain_store_zara_h_m',
        '1 Pair of Nike Running Shoes (Mid-Range)': 'one_pair_of_nike_running_shoes_mid_range',
        '1 Pair of Men Leather Business Shoes': 'one_pair_of_men_s_leather_business_shoes',
        # --- 修正完畢 ---
        'Apartment (1 bedroom) in City Centre': 'apartment_1_bedroom_in_city_centre',
        'Apartment (1 bedroom) Outside of Centre': 'apartment_1_bedroom_outside_of_centre',
        'Apartment (3 bedrooms) in City Centre': 'apartment_3_bedrooms_in_city_centre',
        'Apartment (3 bedrooms) Outside of Centre': 'apartment_3_bedrooms_outside_of_centre',
        'Price per Square Meter to Buy Apartment in City Centre': 'price_per_square_meter_to_buy_apartment_in_city_centre',
        'Price per Square Meter to Buy Apartment Outside of Centre': 'price_per_square_meter_to_buy_apartment_outside_of_centre',
        'Average Monthly Net Salary (After Tax)': 'average_monthly_net_salary_after_tax',
        'Mortgage Interest Rate in Percentages (%), Yearly, for 20 Years Fixed-Rate': 'mortgage_interest_rate_in_percent_yearly_for_20_years_fixed_rate'
    }
    df.rename(columns=column_mapping, inplace=True)
    
    # 遍歷 DataFrame 的每一行
    for index, row in df.iterrows():
        # 將 row 轉換為字典
        data = row.to_dict()
        
        # 清理除了國家名稱和利率以外的所有欄位
        for key, value in data.items():
            if key not in ['country_name', 'mortgage_interest_rate_in_percent_yearly_for_20_years_fixed_rate']:
                 # 在模型中，這些欄位是 CharField，所以我們保留清理後的字串
                 if isinstance(value, str):
                    data[key] = re.sub(r'[^\d.]', '', value)

        # 處理利率欄位，它是一個 FloatField
        data['mortgage_interest_rate_in_percent_yearly_for_20_years_fixed_rate'] = clean_value(data.get('mortgage_interest_rate_in_percent_yearly_for_20_years_fixed_rate'))

        # 使用 update_or_create 來避免重複創建
        # 它會嘗試用 country_name 找到物件，如果找到就更新，沒找到就創建
        CostOfLiving.objects.update_or_create(
            country_name=data['country_name'],
            defaults=data
        )
        print(f"已處理: {data['country_name']}")

    print("資料匯入完成！")

if __name__ == '__main__':
    # 將 'your_csv_file.csv' 替換為您的 CSV 檔案路徑
    csv_file_path = 'cost_of_global(in TWD_cleaned).xlsx'
    import_data_from_csv(csv_file_path)
