#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
class bag():
    def __init__(self,weight,value):
        self.weight = weight
        self.value = value
    def knapsack(self, full_weight,full_v):#weight value存数组
        result = [[0 for i in range(full_weight+1)],]
        id=[[[] for i in range(full_weight+1)],]
        count = len(self.weight)#物品个数
        #min_v,min_w=min(self.value),min(self.weight)
        for n in range(1,count+1):#n当前最大物品个数
            result_list = [0 for i in range(full_weight+1)]
            id_list = [[] for i in range(full_weight+1)]
            for weight in range(0,full_weight+1):#背包内重量递增
                if self.weight[n-1]<=weight:#第n个背包的重量为weight[n-1]判断是否小于允许容量
                    if result[n-1][weight]<(result[n-1][weight-self.weight[n-1]]+self.value[n-1]):
                        #如果当前物品在相同重量情况下价值更高
                        if(result[n-1][weight-self.weight[n-1]]+self.value[n-1])<full_v:
                            result_list[weight]=result[n-1][weight-self.weight[n-1]]+self.value[n-1]
                            id_list[weight]=id[n-1][weight-self.weight[n-1]]+[n,]
                        elif(result[n-1][weight-self.weight[n-1]]+self.value[n-1])==full_v:
                            result_list[weight]=result[n-1][weight-self.weight[n-1]]+self.value[n-1]
                            id_list[weight]=id[n-1][weight-self.weight[n-1]]+[n,]
                            result.append(result_list)
                            break
                        else:
                            result_list[weight]=result_list[weight-1]
                            id_list[weight]=id_list[weight-1]
                    else:
                        result_list[weight]=result[n-1][weight]
                        id_list[weight]=id[n-1][weight]
                else:
                    result_list[weight] =result[n-1][weight]
                    id_list[weight]=id[n-1][weight]
            result.append(result_list)
            id.append(id_list)
            if full_v in result[n]:break
        return result,id
    def find_which(self,full_weight,full_v):
        result,id = self.knapsack(full_weight,full_v)
        for i in id[-1][::-1]:
            if i:
                ilist=i
                break
        return ilist

def del_vm(cpu,mem,idvm,ilist,max_cpu,max_mem,ratio):#将已放置的VM删除
    put_idvm=[]
    rm_cpu=[]
    rm_mem=[]
    n=1
    for i in ilist:
        rm_cpu.append(cpu.pop(i-n))
        rm_mem.append(mem.pop(i-n))
        put_idvm.append(idvm.pop(i-n))
        n+=1
    if (sum(rm_cpu)*1.0/max_cpu<ratio)|(sum(rm_mem)*1.0/max_mem<ratio):
        is_full=False
    else:
        is_full=True
        print '-----'*10
        print 'cpu',sum(rm_cpu)*1.0/max_cpu
        print 'mem',sum(rm_mem)*1.0/max_mem
        print '-----'*10
    return cpu,rm_cpu,mem,rm_mem,idvm,put_idvm,is_full,[max_cpu-sum(rm_cpu),max_mem-sum(rm_mem)]

def run(cpu,mem,idvm,max_cpu,max_mem):
    phy_num=0
    vmlist=[]
    use_ratio=[]
    full_ratio=0.95
    while cpu:
        phy_num+=1
        for i in range(100):
            new_cpu,new_mem,new_vm=[],[],[]
            while cpu:
                sort_instance = bag(cpu,mem)#前1项为约束，后1项为价值
                put_vm=sort_instance.find_which(max_cpu,max_mem)#定义背包总重量，体积
                cpu,rm_cpu,mem,rm_mem,idvm,put_idvm,is_full,reuse=del_vm(cpu,mem,idvm,put_vm,max_cpu,max_mem,(full_ratio-0.05*(phy_num-1)**2))
                if is_full:
                    vmlist.append(put_idvm)
                else:
                    new_cpu+=rm_cpu
                    new_mem+=rm_mem
                    new_vm+=put_idvm
            if new_cpu==[]:
                break
            if sum(new_cpu)<=max_cpu & sum(new_mem)<=max_mem:
                vmlist.append(new_vm)
                cpu=[]
                reuse=[max_cpu-sum(new_cpu),max_mem-sum(new_mem)]
                print "sort program complited"
                break
            seed_int=random.randint(1,100)
            random.seed(seed_int)
            random.shuffle(new_cpu)
            random.seed(seed_int)
            random.shuffle(new_mem)
            random.seed(seed_int)
            random.shuffle(new_vm)
            cpu,mem,idvm=new_cpu,new_mem,new_vm
    return vmlist,reuse
        
def read_input(lists,max_CPU,max_MEM,dim):#lists:[cpu,mem,vmid]
    CPU=lists[0];MEM=lists[1];IDvm=lists[2]
    if dim=='CPU':
        result,reuse=run(MEM,CPU,IDvm,max_MEM,max_CPU)
    else:
        result,reuse=run(CPU,MEM,IDvm,max_CPU,max_MEM)
    print "result",result
    return result,reuse
