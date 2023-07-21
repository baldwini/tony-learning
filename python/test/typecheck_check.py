# Python3 code to demonstrate working of

class Check:
    def __init__(
        self,
        test: str | None = None
    ):
        self.test: str = test


check: Check = Check()
print(check.test)
