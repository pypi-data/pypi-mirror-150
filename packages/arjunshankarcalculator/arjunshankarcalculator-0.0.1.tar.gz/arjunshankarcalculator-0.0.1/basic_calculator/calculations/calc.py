

class calculate:

    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
    
    def validate(self):
        if self.num1 is None or self.num2 is None:
            raise TypeError(
                "Please provide invalid input "
            )
            return False
        else:
            return True

    def add(self):
        if not(self.validate()):
            return
        return self.num1 + self.num2
    
    def sub(self):
        if not(self.validate()):
            return
        return self.num1 - self.num2

    def mul(self):
        if not(self.validate()):
            return
        return self.num1 * self.num2

    def div(self):
        if not(self.validate()):
            return
        return self.num1 / self.num2