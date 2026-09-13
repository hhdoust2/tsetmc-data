import pytse_client as tse
import pandas as pd
import sys
from concurrent.futures import ThreadPoolExecutor

def get_symbol_data(symbol):
    """دریافت اطلاعات و قیمت‌های یک نماد"""
    try:
        ticker = tse.Ticker(symbol)
        return {
            'Symbol': symbol,                     # نماد
            'Title': ticker.title,                # نام شرکت
            'LastPrice': ticker.last_price,       # آخرین قیمت
            'ClosePrice': ticker.adj_close,       # قیمت پایانی
            'YesterdayPrice': ticker.yesterday_price, # قیمت دیروز
            'Volume': ticker.volume,              # حجم معاملات
            'State': ticker.state                 # وضعیت نماد (مجاز/ممنوع)
        }
    except Exception:
        return None

def main():
    print("در حال دریافت لیست نمادهای بورس...")
    try:
        symbols = list(tse.all_symbols())
        print(f"تعداد {len(symbols)} نماد یافت شد. در حال دریافت قیمت‌ها...")

        data = []
        # استفاده از ۱۰ پردازش همزمان برای دریافت سریع قیمت‌ها
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(get_symbol_data, symbols)
            for res in results:
                if res:
                    data.append(res)

        # ساخت جدول داده‌ها
        df = pd.DataFrame(data)
        
        # ذخیره در فایل CSV
        df.to_csv("market_data.csv", index=False, encoding='utf-8-sig')
        print(f"موفقیت کامل: اطلاعات و قیمت‌های {len(df)} نماد در market_data.csv ذخیره شد.")

    except Exception as e:
        print(f"خطا در دریافت اطلاعات: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
