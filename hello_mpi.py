from mpi4py import MPI

comm=MPI.COMM_WORLD
size=comm.Get_size()
rank=comm.Get_rank()

print ("hello world form rank", str(rank),"of",str(size))

