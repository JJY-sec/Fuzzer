import os
import subprocess
import random
import glob
#TODO remove fuzzer inp
class Run:
    def __init__(self):
        #self.max=0
        pass
    def run(self,program,mode,f,num):
        #print("Run")
        if mode=="file":
            
            command = "%s '%s'"%(program,f)
            pro = subprocess.run(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            fd = open(f)
            data = fd.read()
            fd.close()
            command = "%s"%program
            #print(data)
            pro = subprocess.run(command.split(' '),input = data.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,timeout =0x4)
            
            #TODO handle Timeout error


        ret = pro.returncode
        if ret ==-11 or ret == -6:
            print("found crash")
            self.handle_error(ret,data,num)
            #print(data)
            return ret
        return 1
    def handle_error(self,sig,data,num):
        print("Find crash sig%d"%sig)
        fd = open("out/crash_sig%d_%d"%(sig,num),"w")
        fd.write(data)
        fd.close()
        pass
class Fuzzer:
    def __init__(self):
        self.seed=[]
        self.inp_que = []
        self.num=0
        self.generation={}
    def get_cov(self,source):
        #TODO not total cov, only branch cov
        #TODO qemu mode (black box)
        #TODO Wine?
        #TODO lots of files (  -p, --preserve-paths            Preserve all pathname components)
        
        for f in source:
            data = subprocess.Popen(("gcov -b %s"%f).split(' '),stdout=subprocess.PIPE).stdout.read()
        
        #print(data)
        #exit(1)
        st = b"Lines executed:"
        #st = "Branches executed:"
        idx = data.index(st)+len(st)
        data = data[idx:idx+3]
        #print(data)
        if b"." in data:
            data = float(data)
            
        cov = int(data)
        os.system("rm %s.gcda"%f.replace('.c',''))

        #calc cov
        return cov
    def minimize_crash(self):
        pass
    def classify_crash(self):
        pass
    def mutate(self,data,mode):
        data = list(data)
        loop = int(len(data)/10)
        if len(data)==0:
            mode = 2
        if loop==0:
            loop+=1
        if mode==0:
            for _ in range(loop):
                data[random.randint(0,len(data)-1)] = chr(random.randint(0,0xff))
        elif mode==1:
            for _ in range(loop):
                data.pop(random.randint(0,len(data)-1))
        elif mode==2:
            for _ in range(loop):
                data.insert(random.randint(0,len(data)-1),chr(random.randint(0,0xff)))
        else:
            print("mutate : unknown mode error")
        return "".join(data)
    
    def read_seed(self,path):
        files = glob.glob("%s/*"%path)
        print("seeds = %s"%str(files))
        tmp = 0
        for x in files:
            fd = open(x)
            data = fd.read()
            fd.close()

            self.seed.append("/tmp/seed%d"%tmp)
            fd =  open("/tmp/seed%d"%tmp,'w')
            fd.write(data)
            fd.close()
            tmp+=1
        return 
    
    def fuzz(self,program,mode,seed,runner,source):
    #TODO dumb mode

        self.read_seed(seed)
        tmp = 0 
        for x in self.seed:
            #print(self.seed)
            #print("set seed")
            self.generation[x] = 0
            tmp+=1
        while 1:
            if len(self.inp_que)==0:
                #gen self.inp_que
                tmp = self.num
                for ge in self.generation:
                    for _ in range(int(0x100/len(self.generation))):
                        fd2 = open(ge)
                        data = fd2.read()
                        fd2.close()
                        fd = open("/tmp/fuzzer_inp%d"%tmp,"w")
                        fd.write(self.mutate(data,random.randint(0,2)))
                        fd.close()
                        self.inp_que.append("/tmp/fuzzer_inp%d"%tmp)
                        tmp+=1
                for _ in range(0x100 - len(self.inp_que)):
                    self.inp_que.append("/tmp/fuzzer_inp%d"%tmp)
                    fd = open("/tmp/fuzzer_inp%d"%tmp,"w")
                    print(self.generation.keys())
                    fd.write(self.mutate(self.generation[self.generation.keys()[0]],random.ranint(0,2)))
                    fd.close()
                    tmp+=1
                #clear new generation
                self.generation={}
                pass
            ret = runner.run(program,mode,self.inp_que.pop(0) ,self.num)
            if ret ==1:
                cov = self.get_cov(source)
            else:
                #TODO No cov when crash
                cov = 0

            self.generation["/tmp/fuzzer_inp%d"%self.num] = cov
            self.num+=1
            if len(self.inp_que)==0:
                #next generation
                #select top 10 cov, and set top 10 new seed
                next_g={}
                #print(self.generation.values())
                selects = list(self.generation.values())[0:]
                selects.sort(reverse=True)
                unselects = selects[0x10:]

                for unselect in unselects:
                    idx = list(self.generation.values()).index(unselect)
                    unselect = list(self.generation.keys())[idx]
                    del self.generation[unselect]
                    os.system("rm %s"%unselect)
                    #print(unselect)
                #self.generation = next_g

fuzz = Fuzzer()
run = Run()
fuzz.fuzz("./vul","stdin","./in",run,["./vul.c"])
