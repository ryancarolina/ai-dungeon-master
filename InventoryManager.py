import json

class InventoryManager:
    def __init__(self, existing_inventory=None):
        if existing_inventory:
            self.inventory = existing_inventory
        else:
            self.inventory = {
                'Weapons': {},
                'Armor': {},
                'Items': {},
                'Currency': {}
            }

    def add_item(self, category, item_name, quantity):
        if item_name in self.inventory[category]:
            self.inventory[category][item_name] += quantity
        else:
            self.inventory[category][item_name] = quantity

    def remove_item(self, category, item_name, quantity):
        if item_name in self.inventory[category]:
            self.inventory[category][item_name] -= quantity
            if self.inventory[category][item_name] <= 0:
                del self.inventory[category][item_name]

    def update_currency(self, type, amount):
        self.inventory['Currency'][type] = self.inventory['Currency'].get(type, 0) + amount

    def to_json(self):
        return json.dumps(self.inventory)

    @classmethod
    def from_json(cls, inventory_dict):
        return cls(existing_inventory=inventory_dict)

