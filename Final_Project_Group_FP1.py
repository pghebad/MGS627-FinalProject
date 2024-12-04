#This project is about creating charts and graphs to analyze the property data
#and derive actionable insights for home selection.
#In this project, we are using Zillow API to fetch real-time property related data based on the location using web scraping.
#API result data is then manipulated to get the required data for charts and graphs creation.

#Importing the required libraries
import pandas as pd
import requests
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from dash import Dash, dcc, html, Input, Output
import dash
import plotly.express as px
import matplotlib
matplotlib.use("TkAgg")

#--------------------------Web Scraping-----------------------------------------
#Creating variables url, querystring and headers which are required for using API.

#Creating url variable to store Zillow API URL.
url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"

#Creating querystring variable which is a dictionary of parameters required for API to fetch property data.
querystring = {"location":"Buffalo, NY","status_type":"ForSale","home_type":"Houses","daysOn":"30"}

#Creating headers variable which contains required parameters: API key and host.
headers = {
	"x-rapidapi-key": "a3f41ca30fmshe057d7ba522a5cfp180ca1jsnc2cd5b413e7d",
	"x-rapidapi-host": "zillow-com1.p.rapidapi.com"
}

#Packaging and sending the request, and catching the response.
response = requests.get(url, headers=headers, params=querystring)

#Converting response to JSON and storing the required result in a variable
r = response.json()
result = r['props']

#Creating a list to store required columns from the result
main_list = []
for item in result:
	temp_list = [item['address'], item['zpid'], int(item['price']), item['bedrooms'], item['rentZestimate'], item['livingArea']]
	main_list.append(temp_list)

#Defining a function to save properties data as csv.
def save_as_csv():
	#Creating a dataframe to store list data
	properties_df = pd.DataFrame(main_list, columns = ['address', 'zpid', 'price', 'bedrooms', 'rentZestimate', 'livingArea'])

	#Saving dataframe as CSV
	properties_df.to_csv('property_details.csv', index = False)

#Calling function
save_as_csv()

#----------------------Data Manipulation------------------------------------

#Reading the CSV file
properties = pd.read_csv('property_details.csv')

#Printing the information related to properties dataframe
print(properties.info())

#Remove rows with missing values in 'price' and 'livingArea' columns
properties = properties.dropna(subset=['price', 'livingArea'])

#Filling missing values in address column.
properties['address'].fillna('Unknown', inplace=True)

#Filling missing values in rentZestimate column based on similar properties.
#Grouping properties by bedrooms and filling missing values with group's mean.
properties['rentZestimate'] = properties.groupby('bedrooms')['rentZestimate'].transform(
	lambda x: x.fillna(x.mean()))
print(properties[['price', 'rentZestimate']])

print(properties['rentZestimate'])

#--------------------------Multiple Regression------------------------------
#Function for multiple regression to make the decision whether to buy or rent the property
def multiple_regression():
	properties['rentZestimate'] = properties['rentZestimate'] * 12
	# Multiple Regression to predict 'rentZestimate' based on 'price', 'bedrooms', and 'livingArea'
	model = ols('rentZestimate ~ price + bedrooms + livingArea', data=properties).fit()

	# Print the regression parameters
	print("Regression Parameters:\n", model.params)

	# model.params['price'] > model.params['livingArea'] (Buy the property):
	# If price has a higher influence on rent, it implies that purchasing property may lead to better investment (long-term capital appreciation).
	# model.params['livingArea'] > model.params['price'] (Rent the property):
	# If size has a higher influence on rent, renting a property might be a better choice, as rent prices are more closely tied to the size of the property

	# Make the decision based on the regression analysis.
	if model.params['price'] > model.params['livingArea']:
		print("It is better to Buy the property!")
	else:
		print("It is better to Rent the property!")

#Calling a function
multiple_regression()

#---------------------Layout of the Dashboard---------------------------

#Initialize Dash app
app = dash.Dash(__name__)

#Creating variable for logo link
logo_path = 'https://www.buffalo.edu/content/www/brand/TrademarksLicensing/creating-promotional-products/design-ordering/_jcr_content/par/image_1072637049.img.original.jpg/1632234168774.jpg'

app.layout = html.Div([
	#Header and Logo
	html.Div([
		html.Img(src= logo_path, style={'height':'100px'}),
		html.H1("Property Trends Dashboard", style={'textAlign': 'center'}),
	], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'flex-direction':'column'}),

	#Adding price range filter on the dashboard
	html.Div([
		html.Label("Filter by Price Range:"),
		dcc.RangeSlider(
			id='price-slider',
			min=properties['price'].min(),
			max=properties['price'].max(),
			step=50000,
			marks={i: f"${i:,.0f}" for i in range(int(properties['price'].min()), int(properties['price'].max()), 200000)},
			value=[properties['price'].min(), properties['price'].max()],
		)
	], style={'padding': '20px'}),

	#Adding charts on the dashboard
	html.Div([
		dcc.Graph(id='scatter-price-livingarea', style={'width': '48%', 'display': 'inline-block'}),
		dcc.Graph(id='bar-price-bedrooms', style={'width': '48%', 'display': 'inline-block'}),
		dcc.Graph(id='scatter-price-rent', style={'width': '48%', 'display': 'inline-block'}),
		dcc.Graph(id='hist-rent-price-ratio', style={'width': '48%', 'display': 'inline-block'}),
	])
])

#Callbacks for interactivity
@app.callback(
	[
		Output('scatter-price-livingarea', 'figure'),
		Output('bar-price-bedrooms', 'figure'),
		Output('scatter-price-rent', 'figure'),
		Output('hist-rent-price-ratio', 'figure'),
	],
	[Input('price-slider', 'value')]
)

#Defining function to create different charts.
#Function has one parameter price range which is used as filter for charts
def update_plot(price_range):
	#Filter data based on price range
	filtered_data = properties[(properties['price'] >= price_range[0]) & (properties['price'] <= price_range[1])]

	#Chart 1: Scatter Plot - Price vs Living Area
	scatter_fig = px.scatter(
		filtered_data, x='livingArea', y='price',
		title='Price vs Living Area',
		labels={'livingArea': 'Living Area (sq. ft.)', 'price': 'Price (USD)'},
	)

	#Chart 2: Bar Chart - Average Price by Bedrooms
	avg_price = filtered_data.groupby('bedrooms')['price'].mean().reset_index()
	bar_fig = px.bar(
		avg_price, x='bedrooms', y='price',
		title='Average Price by Number of Bedrooms',
		labels={'bedrooms': 'Number of Bedrooms', 'price': 'Average Price (USD)'},
	)

	#Chart 3: Scatter Plot - Price vs Rent Estimate
	scatter_rent_fig = px.scatter(
		filtered_data, x='price', y='rentZestimate',
		title='Price vs Rent Estimate',
		labels={'price': 'Price (USD)', 'rentZestimate': 'Rent Estimate (USD)'},
	)

	#Chart 4: Histogram - Rent-to-Price Ratio
	#Calculating rent(annual value) to price ratio to be used in the chart.
	properties['rent_to_price_ratio'] = (properties['rentZestimate'] * 12) / properties['price']
	#Plotting a chart
	hist_fig = px.histogram(
		filtered_data, x='rent_to_price_ratio',
		title='Distribution of Rent-to-Price Ratio',
		labels={'rent_to_price_ratio': 'Rent-to-Price Ratio'},
	)

	return scatter_fig, bar_fig, scatter_rent_fig, hist_fig

#Setting the app to run
if __name__ == '__main__':
	app.run_server(debug=False)