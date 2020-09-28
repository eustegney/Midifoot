class Proverka:

    def __init__(self):
        self.arg0 = 4
        self.arg1 = 0

    def test_function(self, earg1):
        self.arg1 = earg1

    def test_function_2(self):
        print(self.arg0, self.arg1)


n = Proverka()
n.test_function(2)
n.test_function_2()