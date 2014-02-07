# modex parameter list is below.
climate = 1
inflation = 1.03
interest_rate = 1.01
land_tax = 1.00

import csv
from definitions import Product
    
def csv_to_dict(raw_csv_file):
    product_data = [] 
    products = [] 

    with open(raw_csv_file, "r") as csv_file:
        reader = csv.reader(csv_file)
        
        rownum = 0
        for row in reader:
            if rownum == 0:
                for col in row:
                    product_data.append(col)
                rownum += 1

            else:
               current_product = {}
               colnum = 0
               for col in row:
                   category = product_data[colnum]
                   current_product[category] = col
                   colnum += 1
               products.append(current_product)

    return products

def objectify(products):
    object_list = []
    for product in products:
        object_list.append(Product(product))
    
    return object_list

def calculate_profits(product_objects):
    for product_object in product_objects:
        print product_object.calculate_profit()

def get_products():
    # The first is when the file is called normally, 
    # the second is when the file is called directly.
    try:
        processed_csv = csv_to_dict("econ_model/farm_data.csv")
    except:
        processed_csv = csv_to_dict("farm_data.csv")

    return objectify(processed_csv)

if __name__ == "__main__":
    # This is called like this because state.py is in the parent
    # directory.
    probjects = get_products()
    calculate_profits(probjects)
   
