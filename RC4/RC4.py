def KSA(key):
    S = [i for i in range(0, 256)]

    i = 0
    for j in range(0, 256):
        i = (i + S[j] + key[j % len(key)]) % 256

        temp = S[j]
        S[j] = S[i]
        S[i] = temp
    print(S)
    return S


def PRG(S):
    stream = []
    i = 0
    j = 0
    while True:
        i = (1 + i) % 256
        j = (S[i] + j) % 256

        tmp = S[j]
        S[j] = S[i]
        S[i] = tmp
        t=(S[i]+S[j])% 256
        stream.append(S[t])
        if(len(stream)==512):
            break
    return  stream
def PRF(stream,plain_text):
    lst = []
    for char in plain_text:
        lst.append((bin(ord(char))))
    check_b=False
    for i in range(len(lst)):
        check_b=False
        for char in lst:
            if (check_b):
                if(char=='1'):
                    stream=(PRG(stream[256:511]))
                else:
                    stream=(PRG(stream[0:255]))
            if(char=='b'):
                check_b=True
    return stream
if __name__ == '__main__':
    S = KSA([1,2,3,4,5])
    stream = PRG(S)
    plain_text=input("input text")
    encryption=PRF(stream,plain_text)
    print(encryption)




