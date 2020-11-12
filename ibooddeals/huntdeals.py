"""
Created on 12/11/2020

@author: Lucas V. dos Santos
"""

from ibooddeals.helpers import WishList, Ibood
import re
from notifypy import Notify


class HuntDeals(Ibood):

    def __init__(self, url=None):
        super().__init__(url)

    def get_product(self):
        html = self.get_html()
        for script in html.find_all('script'):
            pattern = re.compile("product.push\(\s+(\{[\s\S]*),\s+\);\s+return product;")
            json_data = script.find(text=pattern)
            if json_data:
                product = dict()
                data = pattern.search(json_data).group(1)
                for line in data.splitlines():
                    if ':' in line:
                        category, value, *_ = line.strip().split(':')
                        if value_strip:=re.search("'(.*?)'", value) :
                            value = value_strip.group(1)
                            product[category] = value
        return product

    def find_product_match(self, wishlist_file=None):

        wish_list = WishList(wishlist_file).items

        product = self.get_product()
        print(product)
        for item in wish_list:
            if item.lower() in product['productName'].lower() or item.lower() in product['offerName'].lower():
                print('Found')

                notification = Notify()
                message = f"Price: {product['price']} ({product['discount']}%)"
                notification.title = product['productName']
                notification.message = message

                notification.send()



def main():
    a =HuntDeals()
    a.find_product_match('wishlist.txt')



if __name__ == "__main__":
    main()
