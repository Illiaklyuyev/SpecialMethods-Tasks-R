from time import sleep
from math import factorial
from mpi4py import MPI
from random import randint

N=100

comm=MPI.COMM_WORLD
size=comm.Get_size()
rank=comm.Get_rank()
def f(x,rank,size):
    delay=randint(10,1000)
    sleep(delay)

if rank==0:
    points=list(map(float,range(0,N-1)))
    results=[]
    for i in range(1,size):
        point=points.pop()
        comm.send(point,i)
        print("results.len = ", end="")
    while points:
        free_process=None
        for i in range(1,size):
            status=comm.improbe(i)
            if status is not None:
                free_process=i
                break
        if free_process is None:
            continue
        result=comm.recv(source=free_process)
        results.append(result)
        print(len(result), end=" ")
        point=points.pop()
        comm.send(point,free_process)
        for i in range(1,N-1):
            result=comm.recv()
            results.append(result)
            print(len(results), end=" ")
            comm.send(float("nan"),0)
else:
    while True:
        point=comm.recv(0)
        if point==float("nan"):
            break
        result=f(point,rank,size)

