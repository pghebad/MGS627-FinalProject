
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
	temp_list = [item['address'], item['zpid'], item['price'], item['bedrooms'], item['rentZestimate'], item['livingArea']]
	main_list.append(temp_list)

print(main_list)

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(main_list, columns = ['address', 'zpid', 'price', 'bedrooms', 'rentZestimate', 'livingArea'])

df.to_csv('property_details.csv', index = False)
