#import pandas as pd
import multiprocessing
from multiprocessing import Queue
from threading import Thread

strategies = ['strategy_1', 'strategy_2']
budgets = [90,100,110,120,130,140,150,160]
formations=['343','352','433','442','451','532','541']
models = ['model_1', 'model_2', 'model_3']

 #shared Queue if you want to reduce write locking use 3 Queues
Q = Queue()

# Retrive async if you want to speed up the process
def function(q,strategy,budget,curr_formation,model):
    q.put("Team")

def runTask(model,q):
    for strategy in strategies:
        for budget in budgets:
            for formation in formations:
                Thread(target=function,args=(q,strategy,budget,formation,model)).start()

def main():
    p1 = multiprocessing.Process(target=runTask, args=('model_1',Q))
    p2 = multiprocessing.Process(target=runTask, args=('model_2',Q))
    p3 = multiprocessing.Process(target=runTask, args=('model_3',Q))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    all = []
    for i in range(0,Q.qsize()):
        all.append(Q.get())
    print(all)
    print(len(all))

if __name__ == "__main__": 
    main()