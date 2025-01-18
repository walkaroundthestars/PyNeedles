

class Yarn:
    def __init__(self, brand:str, type:str, color_name:str, code:str, length:int, weight:int, blend:str, quantity:int):
        self.brand = brand
        self.type = type
        self.color_name = color_name
        self.code = code
        self.length = length
        self.weight = weight
        self.blend = blend
        self.quantity = quantity

    def __str__(self):
        return f"{self.brand} {self.type} {self.color_name} {self.code} {self.blend} {self.length} {self.weight} {self.quantity}"