import math
def factorize(input):
    #rozklad na prvočísla
    tmp=input
    i=2
    output=[]
    while tmp > 1:
        if(tmp%i==0):
            tmp=tmp/i
            output.append(i)
            i-=1
        i+=1
    return output

def queen(sloupce,radky,x,y):
    #vykresli n*m pole, dámu a ohrožená pole 
    x=x-1
    y=y-1
    line=""
    for i in range(radky):
        diagonalOffset=y-i
        for j in range(sloupce):
            if(i==y and j==x):
                line+="D"
            elif(i==y or j==x or (i==y-diagonalOffset and j==x-diagonalOffset) or (i==y-diagonalOffset and j==x+diagonalOffset)or(i==y+diagonalOffset and j==x-diagonalOffset)or(i==y+diagonalOffset and j==x+diagonalOffset)):
                line+="*"
            else:
                line+="."
        print(line)
        line=""
    return 0

def censor_number(length,censored):
    #vypis 1-length, nahrad censored *
    out1=[]
    for i in range(length):
        txt=str(i)
        out1.append(txt)
    out2=[]
    for i in out1:
        string=""
        for x in i:
            if(str(x)==str(censored)):
                string+="*"
            else:
                string+=x
        out2.append(string)
    return out2

def text_analysis(filePath):
    f=open(filePath,"r")
    chars_i_want = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ -")
    tmp= f.read().upper()
    f.close()
    final_string = ''.join(c for c in tmp if c in chars_i_want)
    dicLetter={}
    dicWord={}
    i=0

    tmp2 = final_string.split(" ")
    
    print(len(tmp2))
    
    while i < len(tmp):
        if ord('A') <= ord(tmp[i]) <= ord('Z'):
            if dicLetter.__contains__(tmp[i]):
                dicLetter[tmp[i]] += 1
            else:
                dicLetter[tmp[i]] = 1
        i+=1

    i=0
    while i < len(tmp2):
        if dicWord.__contains__(tmp2[i]):
            dicWord[tmp2[i]] += 1
        else:
            dicWord[tmp2[i]] = 1
        i+=1
    
    return dicLetter,dicWord

def get_words(N,M,structure):
    structure=list(structure.items())
    out=[]
    i=0
    structure.sort(key=lambda x: x[1],reverse=True)
    print(structure[0][0])
    while len(out) < N and i<len(structure):
        if len(structure[i][0])>=M:
            out.append(structure[i])
        i+=1
    return out

def cypher(source,dest):
    alphabet_length=26
    salt=7
    f=open(source,"r")
    word=f.read()
    f.close()
    offset=-3
    output=""
    #a-97,z-122,A-65,Z-90
    k=0
    for i in word:
        if 97<=ord(i)<=122:
            tmp=ord(i)+(offset+(salt*(k**3)))%alphabet_length
            if 97<=tmp<=122:
                output+=chr(tmp)
            elif 97<=tmp:
                output+=chr(97+(tmp-122)-1)
            else:
                output+=chr(122-(tmp-97)-1)
        elif 65<=ord(i)<=90:
            tmp=ord(i)+(offset+(salt*(k**2)))%alphabet_length
            if 65<=tmp<=90:
                output+=chr(tmp)
            elif 65<=tmp:
                output+=chr(65+(tmp-90)-1)
            else:
                output+=chr(90-(tmp-65)-1)
        else:
            output+=i
        k+=1
    f=open(dest,"w")
    f.write(output)
    f.close()
    return output

def decypher(source,dest):
    alphabet_length=26
    salt=7
    f=open(source,"r")
    word=f.read()
    f.close()
    offset=+3
    output=""
    #a-97,z-122,A-65,Z-90
    k=0
    for i in word:
        if 97<=ord(i)<=122:
            tmp=ord(i)+(offset-(salt*(k**3)))%alphabet_length
            if 97<=tmp<=122:
                output+=chr(tmp)
            elif 97<=tmp:
                output+=chr(97+(tmp-122)-1)
            else:
                output+=chr(122-(tmp-97)-1)
        elif 65<=ord(i)<=90:
            tmp=ord(i)+(offset-(salt*(k**2)))%alphabet_length
            if 65<=tmp<=90:
                output+=chr(tmp)
            elif 65<=tmp:
                output+=chr(65+(tmp-90)-1)
            else:
                output+=chr(90-(tmp-65)-1)
        else:
            output+=i
        k+=1
    f=open(dest,"w")
    f.write(output)
    f.close()
    return output

print(factorize(257))
queen(8,5,2,4)
print(censor_number(30,2))
letters,words = text_analysis("c:/Users/DANK/Desktop/book.txt")
print(get_words(5,10,words))
