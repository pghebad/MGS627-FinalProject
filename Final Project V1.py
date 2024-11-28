
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


#-----------------------------------Write a Function------------------

#executing a def(function) to know the decision whether to buy a property or rent.

import pandas as pd
from statsmodels.formula.api import ols
import seaborn as sns
import matplotlib.pyplot as plt


def buy_or_rent(data):
    # Data Cleaning
    # Fill missing 'rentZestimate' values with the mean of the column
    data['rentZestimate'].fillna(data['rentZestimate'].mean(), inplace=True)

    # Remove rows with missing values in 'price' and 'livingArea' columns
    data = data.dropna(subset=['price', 'livingArea'])

    # Fill missing values in other important columns
    data['address'].fillna('Unknown', inplace=True)
    data['bedrooms'].fillna(data['bedrooms'].mean(), inplace=True)  # Fill missing bedrooms with mean if any

    # Data Visualization (Optional)
    # Plot the relationship between Price and Rent
    sns.regplot(x='price', y='rentZestimate', data=data, ci=None)
    plt.title('Price vs Rent Estimate')
    plt.xlabel('Price (USD)')
    plt.ylabel('Rent Estimate (USD)')
    plt.show()

    # Plot the relationship between Living Area and Rent
    sns.regplot(x='livingArea', y='rentZestimate', data=data, ci=None)
    plt.title('Living Area vs Rent Estimate')
    plt.xlabel('Living Area (sq. ft.)')
    plt.ylabel('Rent Estimate (USD)')
    plt.show()

    # Multiple Regression to predict 'rentZestimate' based on 'price', 'bedrooms', and 'livingArea'
    model = ols('rentZestimate ~ price + bedrooms + livingArea', data=data).fit()

    # Print the regression parameters
    print("Regression Parameters:\n", model.params)
    print('\n')

    #logic:
    #model.params['price'] > model.params['livingArea'] (Buy the property):
    # If price has a higher influence on rent, it implies that purchasing property may lead to better investment (long-term capital appreciation).
    #model.params['livingArea'] > model.params['price'] (Rent the property):
    # If size has a higher influence on rent, renting a property might be a better choice, as rent prices are more closely tied to the size of the property


    # Make the decision based on the regression analysis
    if model.params['price'] > model.params['livingArea']:
        print("It is better to Buy the property.")
    else:
        print("It is better to Rent the property.")


property_data = pd.read_csv('property_details.csv')

# Call the function to determine buy or rent
buy_or_rent(property_data)


#----------------V3----------Creating a dashboard-------------------------

from dash import Dash, dcc, html
import plotly.express as px

# Create the Dash app
app = Dash(__name__)

# Print a statement before the Dash app starts
print("Preparing to start the dashboard...")

import os
current_directory = os.getcwd()

logo_path = 'https://images.unsplash.com/photo-1732640452152-8cca8e1d68ef?q=80&w=2072&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'

# Layout of the dashboard
app.layout = html.Div([
    html.Img(src=logo_path, style={'width': '250px'}),
    html.H1("Real Estate Data Dashboard", style={'textAlign': 'center'}),

    # Scatter plot: Price vs Living Area
    html.Div([
        dcc.Graph(
            id='scatter-living-area',
            figure=px.scatter(
                properties,
                x='livingArea',
                y='price',
                title='Price vs Living Area',
                labels={'livingArea': 'Living Area (sq. ft.)', 'price': 'Price (USD)'},
                template='plotly_white'
            )
        )
    ]),

    # Bar chart: Average Price by Number of Bedrooms
    html.Div([
        dcc.Graph(
            id='bar-avg-price-bedroom',
            figure=px.bar(
                properties.groupby('bedrooms')['price'].mean().reset_index(),
                x='bedrooms',
                y='price',
                title='Average Price by Number of Bedrooms',
                labels={'bedrooms': 'Number of Bedrooms', 'price': 'Average Price (USD)'},
                template='plotly_white'
            )
        )
    ]),

    # Scatter plot: Price vs Rent Estimate
    html.Div([
        dcc.Graph(
            id='scatter-price-rent',
            figure=px.scatter(
                properties,
                x='price',
                y='rentZestimate',
                title='Price vs Rent Estimate',
                labels={'price': 'Price (USD)', 'rentZestimate': 'Rent Estimate (USD)'},
                template='plotly_white'
            )
        )
    ]),

    # Histogram: Distribution of Rent-to-Price Ratio
    html.Div([
        dcc.Graph(
            id='hist-rent-to-price-ratio',
            figure=px.histogram(
                properties,
                x='rent_to_price_ratio',
                nbins=20,
                title='Distribution of Rent-to-Price Ratio',
                labels={'rent_to_price_ratio': 'Rent-to-Price Ratio'},
                template='plotly_white'
            )
        )
    ])
])

# Print a message to show app is starting
print("Starting the Dash app...")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
