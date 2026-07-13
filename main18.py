class CheckMethods(type):
    def __new__(cls, name, bases, attrs):

        for method_name, value in attrs.items():

           
            if callable(value):

                
                if not method_name.startswith("_"):
                    raise ValueError(
                        f"Method '{method_name}' must start with '_'"
                    )

        return super().__new__(cls, name, bases, attrs)


class MyClass(metaclass=CheckMethods):

    name = "Gigi"   

    def _hello(self):
        print("Hello")

    def _test(self):
        print("Test")


obj = MyClass()

obj._hello()
obj._test()