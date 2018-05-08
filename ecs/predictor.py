# -*- coding: utf-8 -*-
import datetime,time,knapsack,math

class PhyInfo:
    def __init__(self, cpu, mem, sto):
        self.cpu = cpu
        self.mem = mem
        self.sto = sto

class VMInfo:
    def __init__(self):
        self.CPU = []
        self.MEM = []
        self.ID = []
    def add_VM(self,VMlist):
        self.ID.append(VMlist[0])
        self.MEM.append(int(int(VMlist[2])/1024))
        self.CPU.append(int(VMlist[1]))
    def sort(self):
        self.ID=list(reversed(self.ID))
        self.MEM=list(reversed(self.MEM))
        self.CPU=list(reversed(self.CPU))

def exponential_smoothing(l,a,b):
    avg=Math.avg(l)
    s,t = [0*i for i in range(len(l))],[0*i for i in range(len(l))]
    for i in range(1, len(s)):
        s[i] = a*l[i]+(1-a)*(s[i-1]+t[i-1])
        if s[i]<0:s[i]=avg
        t[i] = b*(s[i]-s[i-1])+(1-b)*t[i-1]
    return s,t

class Math:
    @staticmethod
    def avg(l):
        return float(sum(l))/len(l);
    @staticmethod
    def variance(l):
        s1=0;
        s2=0;
        for i in l:
            s1+=i**2;
            s2+=i;
        return math.sqrt(float(s1)/len(l)-(float(s2)/len(l))**2);
def noise(l):
    l1=[]#第i周
    l1=Denoising(l)
    return l1

def Denoising(l):
    print Math.avg(l),Math.variance(l)
    max_l=Math.avg(l)+3*Math.variance(l)
    avg_l=Math.avg(l)
    while max(l)>max_l:
        l[l.index(max(l))]=max_l
    return l

def moving_windows(lists,length=7,step=1):
    l=[]
    begin=0
    while begin<len(lists)-length+1:
        l.append(sum(lists[begin:begin+length]))
        begin+=step
    return l

def try_alpha(l,t1):#t1预测天数
    train=l[0:int(-1*t1+1)]
    test=l[-1]
    a_list=[i*0.1+0.1 for i in range(9)]
    b_list=[i*0.1+0.1 for i in range(9)]
    error,errors=[],[]
    for a in a_list:
        for b in b_list:
            s,t = exponential_smoothing(train,a,b)
            error.append((s[-1]+t[-1]*t1-test)**2)
        errors.append(error)
        error=[]
    mins=[]
    mins_index=[]
    for i in errors:
        mins.append(min(i))
        mins_index.append(i.index(min(i)))
    return a_list[mins.index(min(mins))],b_list[mins_index[mins.index(min(mins))]]
        

def predict_vm(ecs_lines, input_lines):
    # Do your work from here#
    result = []
    if ecs_lines is None:
        print 'ecs information is none'
        return result
    if input_lines is None:
        print 'input file information is none'
        return result
    #读取input文件信息
    values=input_lines[0].split(" ")
    phyInfo=PhyInfo(int(values[0]),int(values[1]),int(values[2]))
    VM_num=int(input_lines[2])
    VM=VMInfo()
    for i in range(3,3+VM_num):
        VM.add_VM(input_lines[i].split(" "))
    VM.sort()
    DIM=input_lines[3+VM_num+1][0:-1]
    predict_daySpan=(str2time(input_lines[3+VM_num+4])-str2time(input_lines[3+VM_num+3][0:-1])).days
    #读取traindata
    train_begin_time=str2time(ecs_lines[0].split("\t")[-1][0:-1])
    train_end_time=str2time(ecs_lines[-1].split("\t")[-1][0:-1])
    train_daySpan=(str2time(ecs_lines[-1].split("\t")[-1][0:-1])-str2time(ecs_lines[0].split("\t")[-1][0:-1])).days+1
    sequence=[]
    start=train_begin_time
    ecs=ecs_lines
    ecs_list=[]
    predict=[]
    alpha = 0.60
    beta= 0.2
    for i in range(len(VM.ID)):
        sequence=[j*0 for j in range(train_daySpan)]
        for item in ecs:
            if item.split("\t")[1]==VM.ID[i]:
                sequence[(str2time(item.split("\t")[-1][0:10])-start).days]+=1
            else:
                ecs_list.append(item)
        sequence=noise(sequence)
        sequence=moving_windows(sequence,predict_daySpan,1)
        #alpha,beta=try_alpha(sequence,predict_daySpan)
        s,t = exponential_smoothing(sequence,alpha,beta)
        predict.append(int(max(round(s[-1]+t[-1]*predict_daySpan,0),0)))
        ecs=ecs_list
        ecs_list=[]
    result=0
    print "predict:",predict
    to_kp=knapsack_list(predict,VM)
    kp,reuse=knapsack.read_input(to_kp,phyInfo.cpu,phyInfo.mem,DIM)
    #if reuse[0]*1.0/PhyInfo.cpu
    if ((reuse[0]<0.2*phyInfo.cpu) or (reuse[1]<0.2*phyInfo.mem)) and (len(kp[-1])<=5):
        for i in kp[-1]:
            predict[VM.ID.index(i)]-=1
        kp.pop()
    else:
        #给最后一个物理机添加虚拟机
        for i in range(len(VM.CPU)):
            x=predict[i]//7+1
            while(reuse[0]>=VM.CPU[i] and reuse[1]>=VM.MEM[i]):
                x-=1
                if x==0:
                    break
                reuse[0]-=VM.CPU[i]
                reuse[1]-=VM.MEM[i]
                kp[-1].append(VM.ID[i])
                predict[i]+=1
    result=result_writer1(predict,VM)
    result+=result_writer2(kp)
    return result

def knapsack_list(num_list,vminfo):
    cpu,mem,vmid=[],[],[]
    for i in range(len(num_list)):
        if num_list[i]!=0:
            for j in range(num_list[i]):
                cpu.append(vminfo.CPU[i]),mem.append(vminfo.MEM[i]),vmid.append(vminfo.ID[i])
    return [cpu,mem,vmid]
            
def result_writer1(num_list,vminfo):
    out=[]
    out.append(str(sum(num_list)))
    for i in range(len(num_list)):
        out.append(vminfo.ID[i]+' '+str(num_list[i]))
    return out
def result_writer2(lists):
    out=[]
    out.append('\n'+str(len(lists)))
    n=0
    for i in lists:
        n+=1
        lines=str(n)+' '
        dic = {}
        for j in i:
          if i.count(j)>=1:
            dic[j] = i.count(j)    
        for k in dic.items():
            lines+=k[0]+' '+str(k[1])+' '
        out.append(lines.strip())
        del lines
    return out

def str2time(inputStr):
    return datetime.datetime.strptime(inputStr[0:10],"%Y-%m-%d")