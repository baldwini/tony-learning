class Parent:
    def __init__(self):
        self.session = False

    def create_session(self):
        self.session = True


class Child(Parent):
    def __init__(self):
        super().__init__()


child = Child()
child.create_session()
print(child.session)
