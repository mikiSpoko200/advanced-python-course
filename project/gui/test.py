
SOME_GLOBAL_DEFAULT = ["Jestem default"]


class A:
    def __init__(self, foo):
        self.shared = foo or SOME_GLOBAL_DEFAULT


class B(A):
    def __init__(self, bar, foo):
        super().__init__(foo)
        self.bar = bar


class C(A):
    def __init__(self, baz, foo):
        super().__init__(foo)
        self.baz = baz


def main():
    print("Hello from test.py")
    b = B("B attr value", None)
    c = C("C attr value", None)
    print(b.shared)
    print(c.shared)
    print(f"shared is the same instance: {b.shared is c.shared}")




if __name__ == '__main__':
    main()
