from django.core.exceptions import ValidationError

def validateMaxMin(self, data):
    if data['max_inventory'] <= data['min_inventory']:
        raise ValidationError('Max value is less than or equal to min value.')
    
def validateInventory(self, data):
    if data['inventory'] > data['max_inventory']:
        raise ValidationError('Inventory must be less than max.')
    if data['inventory'] < data['min_inventory']:
        raise ValidationError('Inventory must be greater than min.')