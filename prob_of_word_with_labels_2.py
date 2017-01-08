import math

probability = open('vocab_bigram_3count.txt' ,'r')
probability1 = open('vocab_unigram_2count.txt' ,'r')
count = 0
for line in probability:    
    count+= 1
print count

count1 = 0
for line in probability1:
    count1+= 1
print count1

probability1 = open('vocab_unigram_2count.txt' ,'r')
matrix = {}
for line in probability1:
    line=line.split()
    matrix[line[0]]={"UNIGRAM":[0,0]}

probability = open('vocab_bigram_3count.txt' ,'r')

for line in probability:
    line=line.split()
    matrix [line[0]] [line[1]] = [0,0]
#print matrix['suit']
cleanpositive=open("positive_train.txt",'r')
flag=0
for line in cleanpositive:
    line=line.split()
    for i in range(0,len(line)):
        try:
            if i == len(line)-1:
                if flag==1:
                    flag=0
                    continue
                matrix [line[i]]["UNIGRAM"] [0]+=1
                continue
        except:
            pass
        try:
            matrix [line[i]] [line[i+1]] [0]+=1
            flag=1
            
        except:
            #print line[i]
            try:
                if flag==1:
                    flag=0
                    continue
                matrix [line[i]]["UNIGRAM"] [0]+=1
            except:
                pass
cleannegative=open("negative_train.txt",'r')
flag=0
for line in cleannegative:
    line=line.split()
    for i in range(0,len(line)):
        try:
            if i == len(line)-1:
                if flag==1:
                    flag=0
                    continue
                matrix [line[i]]["UNIGRAM"] [1]+=1
                continue
        except:
            pass
        try:
            matrix [line[i]] [line[i+1]] [1]+=1
            flag=1
            
        except:
            #print line[i]
            try:
                if flag==1:
                    flag=0
                    continue
                matrix [line[i]]["UNIGRAM"] [1]+=1
            except:
                pass
'''
#printing matrix
for k in matrix:
    for l in matrix[k]:
        if l=="UNIGRAM":
            print k,matrix[k][l]
'''

sum_pos=sum_neg=0
sum_pos1=sum_neg1=0
for k in matrix :                 ##finding count of words in class postive and negative
    for l in matrix[k]:
        if l =="UNIGRAM":
            sum_pos1+=matrix[k][l][0]
            sum_neg1+=matrix[k][l][1]
        else:
            sum_pos+=matrix[k][l][0]
            sum_neg+=matrix[k][l][1]
#print count
print sum_pos
print sum_neg
print sum_pos1
print sum_neg1



for k in matrix:                         ## smoothing and converting into probability
    for l in matrix[k]:
        if l =="UNIGRAM":
            matrix[k][l][0]= -1 * math.log( (matrix[k][l][0]+1.0)/float(sum_pos1+count1),2)
            matrix[k][l][1]= -1 * math.log( (matrix[k][l][1]+1.0)/float(sum_neg1+count1),2)
        else:
            #print "sadsa"
            matrix[k][l][0]= -1 * math.log((matrix[k][l][0]+1.0)/float(sum_pos+count),2)
            matrix[k][l][1]= -1 * math.log((matrix[k][l][1]+1.0)/float(sum_neg+count),2)


cleaned=open('kfoldtraining.txt','r')
pos=neg=0
for line in cleaned:
    l1=line.split()
    if(l1[0]=="ratingpositive"):
        pos+=1
    if(l1[0]=="ratingnegative"):
        neg+=1

check=float(pos)/float(pos+neg)
check+=float(neg)/float(pos+neg)
print check
prob_positive=-1*math.log(float(pos)/float(pos+neg),2)    ##probablity of classes
prob_negative=-1*math.log(float(neg)/float(pos+neg),2)

print prob_positive
print prob_negative
print sum_pos,sum_pos1
print sum_neg,sum_neg1
print count,count1

test=open("kfoldtesting.txt",'r')
result=0
chance_p=0
chance_n=0
tp=fp=fn=tn=0
for line in test:
    line=line.split()
    if line[0]=='ratingpositive' or line[0]=='ratingnegative':
        if chance_n+prob_negative<= chance_p+prob_positive:
            x= "ratingnegative"
        else:
            x= "ratingpositive"
        if(x=='ratingpositive' and line[0]=='ratingpositive'):
            tp+=1
        if(x=='ratingnegative' and line[0]=='ratingnegative'):
            tn+=1
        if(x=='ratingpositive' and line[0]=='ratingnegative'):
            fn+=1
        if(line[0]=='ratingpositive' and x=='ratingnegative'):
            fp+=1
        chance_p=0
        chance_n=0
        continue
    flag=0
    for i in range(0,len(line)):
        try:
            if i == len(line)-1:
                if flag==1:
                    flag=0
                    continue
                chance_p+=matrix[line[i]]['UNIGRAM'][0]
                chance_n+=matrix[line[i]]['UNIGRAM'][1]
                continue
        except:
            chance_p+=-1*math.log(1.0/float(sum_pos1+count1+1),2)
            chance_n+=-1*math.log(1.0/float(sum_neg1+count1+1),2)
            continue
        try:
            chance_p+=matrix[line[i]][line[1]][0]
            chance_n+=matrix[line[i]][line[1]][1]
            flag=1
        except:
            try:
                if flag==1:
                    flag=0
                    continue
                chance_p+=matrix[line[i]]["UNIGRAM"][0]
                chance_n+=matrix[line[i]]["UNIGRAM"][1]
            except:
                chance_n+=-1*math.log(1.0/float(sum_neg1+count1+1),2)
                chance_p+=-1*math.log(1.0/float(sum_pos1+count1+1),2)
accu=float(tp+tn)/float(tp+tn+fp+fn)

print tp
print tn
print fp
print fn
print accu
