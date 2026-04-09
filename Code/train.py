import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle

# Sample housing data
data = {
    'area': [1000, 1500, 2000, 2500, 3000, 3500, 4000, 1200, 1800, 2200,
             800, 1100, 1600, 2100, 2800, 3200, 900, 1300, 1700, 2400],
    'bath': [1, 2, 2, 3, 3, 4, 4, 1, 2, 3,
             1, 1, 2, 2, 3, 3, 1, 2, 2, 3],
    'balcony': [1, 1, 2, 2, 2, 3, 3, 1, 1, 2,
                0, 1, 1, 2, 2, 3, 0, 1, 2, 2],
    'price': [45, 65, 85, 110, 135, 160, 185, 52, 78, 95,
              35, 48, 68, 88, 120, 145, 38, 55, 75, 105]
}

df = pd.DataFrame(data)

X = df[['area', 'bath', 'balcony']]
y = df['price']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

pickle.dump(model, open('model.pkl', 'wb'))
print("✅ model.pkl saved successfully!")