import matplotlib.pyplot as pl



def plot_routine(arr,n):
    #plots the contents of arr#
    #creation of the plot#
    g=range(n)
    pl.plot(g, arr)
    pl.show()


a=[]
s=input("give me the size of the array: ")
answer="y"
i=0
while (answer=="y") and (i in range (s)):
    b=input("give me element: ")
    a.append(b)
    print("would you like to continue?")
    answer=raw_input()
    i=i+1
plot_routine(a,s)
