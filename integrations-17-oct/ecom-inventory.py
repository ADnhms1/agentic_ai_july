# InventoryAPI: allow us manage the inventory, (get_stock, update_stock)

class InventoryAPI:
    def __init__(self):
        self.stock = {
            "CHAIR_101": 12,
            "DESK_201": 5,
            "LAMP_301": 20
        }

    def get_stock(self, skuId):
        return self.stock.get(skuId)

    def update_stock(self, skuId, quantity):
        if skuId not in self.stock:
            return {
                "success": False,
                "error": "Product not found"
            }
        
        if quantity <= 0:
            return {
                "success": False,
                "error": "Quantity has to be positive and greater then 0"
            }

        self.stock[skuId] = quantity

        return {
            "success": True,
            "sku": skuId,
            "new_quantity": quantity
        }

# use this inventory class to do some CRUD

api = InventoryAPI()

skuId = "CHAIR_101"

print("Stock before update: ", api.get_stock(skuId))

result = api.update_stock(skuId, 10)

print("API response : ", result)
print("Stock after update : ", api.get_stock(skuId))