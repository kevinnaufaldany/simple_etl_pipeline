import pandas as pd
 
def transform_data(data, exchange_rate):
    """Menggabungkan semua transformasi data menjadi satu fungsi."""
    data['price_in_dolars'] = data['price'].replace(r'\$', '', regex=True).astype(float)
    
    data['price_in_rupiah'] = (data['price_in_dolars'] * exchange_rate).astype(float)
    
    data = data.drop(columns=['price'])
    data = data.drop(columns=['price_in_dolars'])

    data = data.rename(columns={'price_in_rupiah': 'price'})

    data['rating'] = data['rating'].astype('float')
    data['colors'] = data['colors'].astype('int64')
    
    column_order = ['title', 'price', 'rating', 'colors', 'size', 'gender', 'timestamp']
    data = data[column_order]
    
    return data