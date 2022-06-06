import first_come_first_serve
import round_robin
import pre_emptive_short_job_first
from EDF_earliest_deadline_first import EDF
from SCT_shortest_comp_time import SCT

print("PLEASE enter which Algo you would like to use: \n "
      "FCFS (first come first serve) ; RR (round robin) ; SJF (preemptive shortest job first) \n"
      "EDF (Earliest deadline first) ; SCT (shortest compute time) :\n")
input_str = input()
if input_str == "FCFS":
    first_come_first_serve.FCFS()
elif input_str == "RR":
    round_robin.RR()
elif input_str == "SJF":
    pre_emptive_short_job_first.PE_SJF()
elif input_str == "EDF":
    EDF()
elif input_str == "SCT":
    SCT()
else:
    print("WRONG INPUT!!!!!!")