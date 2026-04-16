from order import view_order
from verify import verify_token
from model import Product

view_ordered = view_order()
product_id = Product

get_ordered = next((v for v in view_ordered),None)
get_item = next((g for g in get_ordered['items']),None)

print('order: ',get_ordered)
print('item: ',get_item)