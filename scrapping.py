from bs4 import BeautifulSoup
import requests
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0'
}

session = requests.Session()

for j in range(427, 543):

    print(f"Scraping page {j}/543")

    page_data = []

    url = f'https://www.nepalhomes.com/search?find_property_category=5d660cb27682d03f547a6c4a&page={j}&sort=1'

    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    houses = soup.find_all('div', class_='property__card')

    for i in houses:

        # listing page data
        price = (
            i.find('span', class_='price-tag').text.strip()
            if i.find('span', class_='price-tag') else None
        )

        location = (
            i.find('p', class_='property__card-location').text.strip()
            if i.find('p', class_='property__card-location') else None
        )

        property_type = (
            i.find('span', class_='property__card-type').text.strip()
            if i.find('span', class_='property__card-type') else None
        )

        # default detail fields
        road_access = None
        facing = None
        floor = None
        parking = None
        bedrooms = None
        bathrooms = None
        area = None
        furnish_status = None

        # detail page
        link_tag = i.find('a', class_='btn btn-primary btn-details')

        if link_tag:
            full_link = "https://www.nepalhomes.com" + link_tag['href']
            print(f"Fetching: {full_link}")

            detail_response = session.get(full_link, headers=headers)
            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

            overview = detail_soup.find('ul', class_='list-overview')

            if overview:
                house_data = {}

                items = overview.find_all('li')

                for item in items:
                    key = item.find('h3').text.strip()
                    value = item.find('h5').text.strip()
                    house_data[key] = value

                road_access = house_data.get('ROAD ACCESS')
                facing = house_data.get('FACING')
                floor = house_data.get('FLOOR')
                parking = house_data.get('PARKING')
                bedrooms = house_data.get('BEDROOM')
                bathrooms = house_data.get('BATHROOM')
                area = house_data.get('BUILTUP AREA')
                furnish_status = house_data.get('FURNISH STATUS')

        # store one house
        page_data.append({
            'price': price,
            'location': location,
            'property_type': property_type,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'area': area,
            'road_access': road_access,
            'facing': facing,
            'floor': floor,
            'parking': parking,
            'furnish_status': furnish_status
        })

    # save after each page
    df = pd.DataFrame(page_data)

    df.to_csv(
        '../data/raw/house_data.csv',
        mode='a',
        header=(j == 1),
        index=False
    )

print("Scraping completed successfully")