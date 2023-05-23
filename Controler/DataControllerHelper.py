
class DataControllerHelper:
    """
    Helper class for DataController
    """
    
    def __init__(self):
        self.active = True

    def substract_wrapping(self,num, sub):
        result = num - sub
        if result < 1:
            result += 12
        return result
    
    def add_wrapping(self, num, add):
        result = num + add
        if result > 12:
            result -= 12
        return result