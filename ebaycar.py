import pandas as pd
import numpy as np

autos = pd.read_csv('D:\\dataquest\\autos.csv', encoding='Latin-1')
autos.info()
autos.head()

autos.columns

autos.columns = ['date_crawled', 'name', 'seller', 'offer_type', 'price', 'ab_test',
       'vehicle_type', 'registration_year', 'gearbox', 'power_ps', 'model',
       'odometer', 'registration_month', 'fuel_type', 'brand',
       'unrepaired_damage', 'ad_created', 'num_photos', 'postal_code',
       'last_seen']
autos.head()
autos.describe(include='all')

autos["num_photos"].value_counts()

autos = autos.drop(["num_photos", "seller", "offer_type"], axis=1)

autos["price"] = (autos["price"]
                          .str.replace("$","")
                          .str.replace(",","")
                          .astype(int)
                          )
autos["price"].head()

autos["odometer"] = (autos["odometer"]
                             .str.replace("km","")
                             .str.replace(",","")
                             .astype(int)
                             )
autos.rename({"odometer": "odometer_km"}, axis=1, inplace=True)
autos["odometer_km"].head()

autos["odometer_km"].value_counts()

print(autos["price"].unique().shape)
print(autos["price"].describe())
autos["price"].value_counts().head(20)

autos["price"].value_counts().sort_index(ascending=False).head(20)
autos["price"].value_counts().sort_index(ascending=True).head(20)

autos = autos[autos["price"].between(1,351000)]
autos["price"].describe()

autos[['date_crawled','ad_created','last_seen']][0:5]

(autos["date_crawled"]
        .str[:10]
        .value_counts(normalize=True, dropna=False)
        .sort_values()
        )
(autos["last_seen"]
        .str[:10]
        .value_counts(normalize=True, dropna=False)
        .sort_index()
        )

print(autos["ad_created"].str[:10].unique().shape)
(autos["ad_created"]
        .str[:10]
        .value_counts(normalize=True, dropna=False)
        .sort_index()
        )

autos["registration_year"].describe()

(~autos["registration_year"].between(1900,2016)).sum() / autos.shape[0]

# Many ways to select rows in a dataframe that fall within a value range for a column.
# Using `Series.between()` is one way.
autos = autos[autos["registration_year"].between(1900,2016)]
autos["registration_year"].value_counts(normalize=True).head(10)

autos["brand"].value_counts(normalize=True)

brand_counts = autos["brand"].value_counts(normalize=True)
common_brands = brand_counts[brand_counts > .05].index
print(common_brands)

brand_mean_prices = {}

for brand in common_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_price = brand_only["price"].mean()
    brand_mean_prices[brand] = int(mean_price)

brand_mean_prices

bmp_series = pd.Series(brand_mean_prices)
pd.DataFrame(bmp_series, columns=["mean_mileage"])

brand_mean_mileage = {}

for brand in common_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_mileage = brand_only["odometer_km"].mean()
    brand_mean_mileage[brand] = int(mean_mileage)

mean_mileage = pd.Series(brand_mean_mileage).sort_values(ascending=False)
mean_prices = pd.Series(brand_mean_prices).sort_values(ascending=False)

brand_info = pd.DataFrame(mean_mileage,columns=['mean_mileage'])
brand_info

brand_info["mean_price"] = mean_prices
brand_info
