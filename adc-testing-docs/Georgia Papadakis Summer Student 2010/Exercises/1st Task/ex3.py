#f_name=input()
#print(f_name)
question = "What is the name of the file?"
print (question)
answer = raw_input()
print ("ok,so the name of the file is " + answer + "let me show it")
f=open(answer)
for line in f:
        print line

