
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
import matplotlib
matplotlib.use("TkAgg")


#Reading the CSV file
properties = pd.read_csv('property_details.csv')



properties['price'] = properties['price'].astype(int)

#Printing the information related to properties dataframe
print(properties.info())


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
properties.plot(x='livingArea', y='price', kind='bar', legend=True)
# Add labels and title
plt.xlabel('Living Area')
plt.ylabel('Price')
plt.title('Bar Graph using Matplotlib')

# Show the plot
plt.show()