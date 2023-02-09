from math import factorial
from mpi4py import MPI

comm=MPI.COMM_WORLD
size=comm.Get_size()
rank=comm.Get_rank()

x=1 
n=100
def calc_partial_series():
    sum=0
    for i in range(rank,n,size-1):
        sum+=x**i/factorial(i)
    return sum

if rank != 0:
    comm.send(calc_partial_series(),0)
else:
    sum=1
    for i in range(size-1):
        sum+=comm.recv()
    print(sum)
