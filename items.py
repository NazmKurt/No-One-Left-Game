class Items:
    def __init__(self, name, item_type, value):
        self.name = name 
        self.item_type = item_type 
        self.value = value 
    
    def __str__(self):
        return f"{self.name} ({self.item_type}, {self.value})"
    
    