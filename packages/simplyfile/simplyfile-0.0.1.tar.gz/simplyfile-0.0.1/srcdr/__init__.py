def readnline(filename,n):
    f = open(filename,'r')
    data = ""
    for i in range(n):
        data += f.readline()
    f.close()
    return data
def append(filename,string):
    a = filename
    f = open(a,'a')
    f.write(string)
    f.close()
def appendline(filename,string):
    a = filename
    f = open(a,'a')
    temp = string + '\n'
    f.write(temp)
    f.close()
def newfile(filename):
    a = filename
    f = open(a,'w')
    f.close()
    print(f"Your file {a} was successfuly created")
def numsplit(filename):
    f = open(filename,'r')
    data = f.read()
    l1,l2,l3 = [],[],[]
    if ('\n' in data):
        l1 = data.split('\n')
    elif (','in data):
        l2 = data.split(',')
    elif(' 'in data):
        l3 = data.split(' ')
    f.close()
    l = l1+l2+l3
    listlen = len(l)
    fe = open('even','a')
    fo = open('odd','a')
    for i in l:
        x = int(i)
        x = x%2
        if x == 0:
            fe.write(i+'\n')
        else:
            fo.write(i+'\n')
    fe.close()
    fo.close()
    print('2 files were created names even and odd')
def counted(filename):
    f = open(filename,'r')
    data = f.read()
    line = 0
    words = 0
    chars = 0
    if ('\n' in data):
        l1 = data.split('\n')
        line = len(l1)        
    if(' 'in data):
        l2 = data.split(' ')
        words = len(l2)
    chars = len(data)
    s = f"No of characters in this file : {chars}\nNo of Words in this file : {words}\nNo of lines in this file : {line}"
    f.close()
    return s
def writelist(filename,l,ender = ' '):
    a = filename
    f = open(a,'a')
    for i in l:
        x = str(i)
        f.write(x + ender)
    f.close()



    