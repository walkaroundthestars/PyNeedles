

class Yarn:
    def __init__(self, brand:str, type:str, color_name:str, blend:str, code:str, length:int, weight:int, quantity:int):
        self.brand = brand
        self.type = type
        self.color_name = color_name
        self.code = code
        self.length = length
        self.weight = weight
        self.blend = blend
        self.quantity = quantity

    def __str__(self):
        return f"{self.brand} {self.type} {self.color_name}"