
import math

def get_ScoringMatrix(data,pA,pG,p):
    for x in range(len(data)):
        print(p[x], end=" ")
        for y in range(len(data[x])):
            a=0.0
            if (p[x] == "A" or p[x] == "T"):
                a=data[x][y] /pA
            if (p[x] == "G" or p[x] == "C"):
                a=data[x][y]/pG
            print(str(round(a,2)),end=",\t"),
        print(' ')


def get_frequencymatrix(p, s):
    all_text = "";
    data = [[0 for x in range(len(s[0]))] for y in range(len(p))]
    for pi in range(len(p)):
        # print("  ", p[pi], end="    ")

        text = p[pi] + " "
        count = 0
        for sii in range(len(s[0])):
            m = 0
            for si in range(len(s)):
                if p[pi] == s[si][sii]:
                    m += 1
                    count += 1
            # print("  ", m, end="    ")
            data[pi][sii] = m
            text = text + str(round(m / 8, 1)) + ", \t"
        if count > 0:
            # return text

            all_text += text + "\n"
        # v = int(m) / (3)
        # print("  ", v, end="    ")
    # print("/n")
    print(all_text)
    return data

    #pass
def get_CorrectedFrequencyMatrix(p,data):
    for x in range(len(data)):
        print(p[x],end=" ")
        for y in range(len(data[x])):
            pA=pT=0.325
            pG=pC=0.175
            k=1
            if(p[x]=="A" or p[x]=="T"):
                data[x][y]=(data[x][y] +(pA*k))/(8+k)
            if (p[x]=="G" or p[x]=="C"):
                data[x][y]=(data[x][y] +(pG*k))/(8+k)

            print(str(round(data[x][y],2)),end=",\t"),

        print(" ")
    return data


class PSSM:
    n = 8  # int(input("Enter the no of sequence: ")) #3
    s = [[''] for i in range(n)]
    s[0] = 'TCACACGTGGGA'
    s[1] = 'GGCCACGTGCAG'
    s[2] = 'TGACACGTGGGT'
    s[3] = 'CAGCACGTGGGG'
    s[4] = 'TTCCACGTGCGA'
    s[5] = 'ACGCACGTTGGT'
    s[6] = 'CAGCACGTTTTC'
    s[7] = 'TACCACGTTTTC'



    # for i in range(n):
    # s[i] = input("Enter the sequene: ")

    print("Entered sequences are:")
    for i in range(n):
        print(s[i])

    p = "AGTC"
    pA = pT = 0.325
    pG = pC = 0.175
    k = 1
    print("\nFrequency Metrix");
    data = get_frequencymatrix(p,s)
    print("\nCorrectedFrequencyMatrix");
    data1 = get_CorrectedFrequencyMatrix(p, data)
    print("\nScoringMatrix");
    get_ScoringMatrix(data,pA,pG,p)






