def main():
    print(f"foo: {foo()}")
    print(f"bar: {bar()}")

    d = foo(5)
    e = bar(5)

    print(f"foo: {d}")
    print(f"bar: {e}")

    foo(10,d)
    bar(10,e)

    print(f"foo: {d}")
    print(f"bar: {e}")


def foo(a=3,b=[]):
    b.append(a)
    return b

def bar(a=3,b=None):
    if b is None: b = []
    b.append(a)
    return b


# ===================================================================
# Entry point
# ===================================================================
if __name__ == '__main__':
    main()    
