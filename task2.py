from math import isnan
from time import sleep
from mpi4py import MPI
from random import randint

N=100

comm=MPI.COMM_WORLD
size=comm.Get_size()
rank=comm.Get_rank()

def f(x,rank,size):
    delay=randint(10,100)
    sleep(delay/1000)

if rank==0:
    points=list(map(float,range(0,N)))
    results=[]
    for i in range(1,size):
        point=points.pop()
        comm.send(point,i)
    print("results.len = ", end="",flush=True)
    while points:
        free_process=None
        for i in range(1,size):
            status=comm.iprobe(i)
            if status is not None:
                free_process=i
                break
        if free_process is None:
            continue
        result=comm.recv(source=free_process)
        results.append(result)
        print(len(results), end=" ",flush=True)
        point=points.pop()
        comm.send(point,free_process)
    for i in range(1,size):
        result=comm.recv(source=i)
        results.append(result)
        print(len(results), end=" ",flush=True)
        comm.send(float("nan"),i)
else:
    while True:
        point=comm.recv(source=0)
        if isnan(point):
            break
        result=f(point,rank,size)
        comm.send(result,0)

