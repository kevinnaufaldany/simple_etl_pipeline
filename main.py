import pandas as pd
from utils.extract import scrape_fashion_data
from utils.transform import transform_data
from utils.load import load_to_csv, store_to_postgre, load_to_spreetsheet

def main():
    """Fungsi utama untuk keseluruhan proses scraping hingga penyimpanan."""
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}.html'
    SPREADSHEET_NAME = 'scraping'
    SPREADSHEET_ID = '15Rgqw0n-wWYLz6DwCggKWe1YLNAiJo_OoQ6aemPHhDY'
    CLIENT_SECRET_FILE = 'client_secret.json'
    
    print("EXTRACT: Melakukan web scraping...")
    all_fashion_data = scrape_fashion_data(BASE_URL)

    if len(all_fashion_data) == 0:
        print("Tidak ada data yang berhasil diambil!")
        return

    df = pd.DataFrame(all_fashion_data)
    print(f"DataFrame berhasil dibuat dengan shape: {df.shape}")
    print("\nPreview data (sebelum transformasi):")
    print(df.head())
    print(f"\nTipe data sebelum transformasi:\n{df.dtypes}")

    print("\nTRANSFORM: Melakukan transformasi data...")
    df = transform_data(df, exchange_rate=16000)
    print(f"DataFrame setelah transformasi dengan shape: {df.shape}")
    print("\nPreview data (setelah transformasi):")
    print(df.head())
    print(f"\nTipe data setelah transformasi:\n{df.dtypes}")

    print("\nLOAD: Menyimpan data...")
    load_to_csv(df, 'fashion_data.csv')

    print("\nMenyimpan ke Google Sheets...")
    try:
        load_to_spreetsheet(df, SPREADSHEET_ID, SPREADSHEET_NAME, CLIENT_SECRET_FILE)
    except FileNotFoundError:
        print("CATATAN: File client_secret.json tidak ditemukan")
        print("Lihat GOOGLE_SHEETS_SETUP.md untuk setup Google Sheets")
    except Exception as e:
        print(f"CATATAN: Gagal load ke Sheets: {str(e)[:80]}")
        print("Anda bisa setup Google Sheets nanti, data sudah tersimpan di CSV")

    print("\nMenyimpan ke PostgreSQL...")
    try:
        db_url = 'postgresql+psycopg2://developer:developer@localhost:5432/db_fashion'
        store_to_postgre(df, db_url)
    except Exception as e:
        print(f"CATATAN: Gagal load ke PostgreSQL")
        print(f"Jalankan: python setup_postgre.py")
        print(f"Error: {str(e)[:80]}")

if __name__ == "__main__":
    main()