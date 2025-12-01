# tail
def draw_tail(n:int):
    _ = ["_"]*(2*n)
    for i in range(n+1):
        print(f"\\{'.'.join(_)}/")

    for i in range(1,n+1):
        _ = ["_"]*(2*n-i)
        print ( f"{" "*(i)}\\{'.'.join(_)}/")

#draw_tail(7)
def ornithorynque(text:str):
    text_list = list(text.lower())
    ans = []
    for c in "ornithorynque":
        try:
            n=text_list.index(c)
            ans.append(n)
            text_list[n] = "."
        except ValueError:
            ans.append(-1)
    print(ans)
ornithorynque("Platypus is the best animal in the world")
ornithorynque("What exactly is that thing called an ornithorynque in fremch??")



