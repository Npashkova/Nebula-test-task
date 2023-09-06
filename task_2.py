from sklearn.linear_model import LinearRegression
import freecurrencyapi

import os
from dotenv import load_dotenv

from datetime import datetime, timedelta

import pandas as pd

import plotly.express as px

# Get API key from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Calculate the dates needed
current_date = datetime.now()
one_month_7_days_ago = current_date - timedelta(days=37)
date_from = one_month_7_days_ago.strftime("%Y-%m-%d")
date_to = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
next_week = (datetime.today() + timedelta(days=6)).strftime("%Y-%m-%d")

# Call currency API
client = freecurrencyapi.Client(API_KEY)
data = client._request('/historical', params={
    'date_from': date_from,
    'date_to': date_to,
    'currencies': ['EUR']
})

# Extract data from the dictionary
date_list = []
exchange_rate_list = []

for date, values in data['data'].items():
    date_list.append(date)
    exchange_rate_list.append(values['EUR'])

# Create a DataFrame
df = pd.DataFrame({'Date': date_list, 'EUR Exchange Rate': exchange_rate_list})

train_data = df[23:30]
validation_data = df[30:37]

start_date = validation_data['Date'].iloc[0]
end_date = next_week

x_train = pd.to_datetime(train_data['Date']).dt.day.values.reshape(-1, 1)
y_train = train_data['EUR Exchange Rate']

x_validation = pd.to_datetime(validation_data['Date']).dt.day.values.reshape(-1, 1)

model = LinearRegression()
model.fit(x_train, y_train)
predicted_exchange_rate = model.predict(x_validation)

prediction_data = {
    'Date': pd.date_range(start_date, end_date),
    'Predicted EUR Exchange Rate': predicted_exchange_rate
}
# prediction_df = pd.DataFrame(prediction_data)

figure = px.line(validation_data, x="Date",
                 y="EUR Exchange Rate",
                 title='USD - Euro Conversion Rate over the week')
figure.show()
