import requests
import json

def get_data():
    # https://curlconverter.com/#python  конвертер curl
#################################################################
    cookies = {'your': 'cookie'}

    headers = {'your': 'headers'}

    params = {
        'categoryId': '195',
        'offset': '0',
        'limit': '24',
        'filterParams': [
            'WyLQotC+0LLQsNGA0Ysg0YHQviDRgdC60LjQtNC60L7QuSIsIi04Iiwi0JHQvtC70LXQtSA1JSJd',
            'WyLQotC+0LvRjNC60L4g0LIg0L3QsNC70LjRh9C40LgiLCItOSIsItCU0LAiXQ==',
        ],
    }

    response = requests.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies,headers=headers).json()

    products = response.get("body").get("products") # id  всех планшетов


    with open("1_proucts_ids.json", "w") as file: #  записываем в файл
        json.dump(products, file, indent=4, ensure_ascii="False") #  записываем в файл
#################################################################
    json_data = {
        'productIds':products,
        'mediaTypes': [
            'images',
        ],
        'category': True,
        'status': True,
        'brand': True,
        'propertyTypes': [
            'KEY',
        ],
        'propertiesConfig': {
            'propertiesPortionSize': 5,
        },
        'multioffer': False,
    } # формируем описание товаров с магазина

    response_post = requests.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies, headers=headers,
                             json=json_data).json()



    with open("2_item.json", "w") as file:
        json.dump(response_post, file, indent=4, ensure_ascii="False")
    #print(len(response_post.get("body").get("products")))
#################################################################
    products_str = ",".join(products)

    params = {
        'productIds': products_str,
        'addBonusRubles': 'true',
        'isPromoApplied': 'true',
    }

    response_prices = requests.get('https://www.mvideo.ru/bff/products/prices', params=params, cookies=cookies,
                            headers=headers).json()
    with open("3_prices.json", "w") as file: #  записываем в файл
        json.dump(response_prices, file, indent=4, ensure_ascii="False") #  записываем в файл

##################################################################
    item_prices = {}
    material_prices = response_prices.get("body").get("materialPrices")
    for item in material_prices:
        item_id = item.get("price").get("productId")
        item_base_prise = item.get("price").get("basePrice")
        item_sale_prise = item.get("price").get("salePrice")
        item_bonus = item.get("bonusRubles").get("total")

        item_prices[item_id] = {
            'item_basePrice': item_base_prise,
            'item_salePrise': item_sale_prise,
            'Item_bonus': item_bonus
        }

    with open("4_item_prices.json", "w") as file: #  записываем в файл
        json.dump(item_prices, file, indent=4, ensure_ascii="False") #  записываем в файл

##################################################################
def get_result():
    with open("2_item.json") as file:
        products_data = json.load(file)
    with open("4_item_prices.json") as file:
        product_prices = json.load(file)
    product_data = products_data.get("body").get("products")

    for item in product_data:
        product_id = item.get("productId")

        if product_id in product_prices:
            prices = product_prices[product_id]
            item['item_basePrice'] = prices.get("item_basePrice")
            item['item_salePrice'] = prices.get("item_salePrice")
            item['Item_bonus'] = prices.get("Item_bonus")

    with open("5_result.json", "w") as file: #  записываем в файл
        json.dump(products_data, file, indent=4, ensure_ascii="False") #  записываем в файл

def main():
    get_data()
    get_result()

if __name__ == '__main__':
    main()
