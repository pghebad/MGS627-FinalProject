
import requests
import pandas as pd

url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"

querystring = {"location":"Buffalo, NY","status_type":"ForSale","home_type":"Houses","daysOn":"7","soldInLast":"1"}

headers = {
	"x-rapidapi-key": "a3f41ca30fmshe057d7ba522a5cfp180ca1jsnc2cd5b413e7d",
	"x-rapidapi-host": "zillow-com1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

houses = response.json()
result = houses['props']

main_list = []
for item in result:
	temp_list = [item['address'], item['zpid'], int(item['price']), item['bedrooms'], item['rentZestimate'], item['livingArea']]
	main_list.append(temp_list)

print(main_list)

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(main_list, columns = ['address', 'zpid', 'price', 'bedrooms', 'rentZestimate', 'livingArea'])

df.to_csv('property_details.csv', index = False)


#importing required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.formula.api import ols
import plotly.express as px
from matplotlib.ticker import ScalarFormatter


import matplotlib
matplotlib.use("TkAgg")

#Reading the CSV file
properties = pd.read_csv('property_details.csv')


properties['price'] = properties['price'].astype(int)

#Printing the information related to properties dataframe
print(properties.info())


print(properties['price'].head())
print(properties['price'].dtype)
properties['price'] = properties['price'].astype(float)  # If prices might have decimal values


#------------------V2---------------------

#Insight: Helps understand the price per square foot and identify trends.
plt.figure(figsize=(10, 6))
plt.scatter(properties['livingArea'], properties['price'])
plt.title('Price vs. Living Area')
plt.xlabel('Living Area (sq. ft.)')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.show()


#Insight: Understand how the number of bedrooms correlates with average property prices.
#Create a bar chart showing the average price per number of bedrooms.
# Group by bedrooms and calculate average price
avg_price_per_bedrooms = properties.groupby('bedrooms')['price'].mean()

# Bar chart
avg_price_per_bedrooms.plot(kind='bar', figsize=(8, 6), title="Average Price by Number of Bedrooms")
plt.xlabel('Number of Bedrooms')
plt.ylabel('Average Price (USD)')
plt.grid(axis='y')
plt.show()



# Scatter plot: Price vs. Rent Estimate
plt.figure(figsize=(10, 6))
plt.scatter(properties['price'], properties['rentZestimate'], alpha=0.7)
plt.title('Price vs. Rent Estimate')
plt.xlabel('Price (USD)')
plt.ylabel('Rent Estimate (USD)')
plt.grid(True)
plt.show()


# Calculate Rent-to-Price ratio
properties['rent_to_price_ratio'] = properties['rentZestimate'] / properties['price']

# Histogram of Rent-to-Price Ratio
plt.figure(figsize=(8, 6))
plt.hist(properties['rent_to_price_ratio'].dropna(), bins=20, alpha=0.7)
plt.title('Distribution of Rent-to-Price Ratio')
plt.xlabel('Rent-to-Price Ratio')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()



#--------------------------V1-----------------------------
#Scatterplot
sns.regplot(x='livingArea', y='price',
            data = properties,
            scatter_kws = {"color": "blue"},
            line_kws = {"color": "red"},
            ci = None)
#Adding a title to the plot
plt.title('Relationship between living area and price')
plt.ylim(90000, 600000)  # Set x-axis range from 0 to 5
plt.show()


#Histogram
properties.hist()
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.title('Histogram of Property Prices')
plt.show(block=True)


# Plot the bar graph
#plt.bar(properties['livingArea'], properties['price'])
properties.plot(x='livingArea', y='price', kind='bar', legend=True)
# Add labels and title
plt.xlabel('Living Area')
plt.ylabel('Price')
plt.title('Bar Graph using Matplotlib')

# Show the plot
plt.show()