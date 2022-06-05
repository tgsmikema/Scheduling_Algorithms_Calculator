from queue import PriorityQueue
from queue import Queue

from Process import Process


def PE_SJF():
    burst_str = input("Enter Burst Times separate with SPACE :\n")
    arrival_str = input("Enter Arrival Times separate with SPACE :\n")

    # convert burst_str into int list
    try:
        b_str = burst_str.split(" ")
        a_str = arrival_str.split(" ")
        if len(b_str) != len(a_str):
            print("CHECK YOUR INPUT!!")
            exit(1)
        burst_list = []
        arrival_list = []
        for b_ele in b_str:
            burst_list.append(int(b_ele))
        for a_ele in a_str:
            arrival_list.append(int(a_ele))
        # print(burst_list)
        # print(arrival_list)
    except ValueError:
        print("WRONG FORM OF INPUT!!!")
        exit(1)
    #####################################################

    process_list = []
    # create Process lists ID starting from 0
    for i in range(len(burst_list)):
        process_list.append(Process(process_id=i, burst_time=burst_list[i], arrival_time=arrival_list[i]))

    schedule = PriorityQueue(maxsize=len(burst_list))
    waiting_q = PriorityQueue(maxsize=len(burst_list))

    for process in process_list:
        arr_t = process.arrival_time
        rem_t = process.remaining_time
        if arr_t == 0:
            # tuples
            schedule.put((rem_t, arr_t, process))
        else:
            waiting_q.put((arr_t, process))

    process_event_list = []
    time = 0
    while not schedule.empty():
        # print(schedule.get()[2].burst_time)
        # checking if more process arrives, if yes, put it into schedule queue, else remain in waitingQ
        event = []
        if not waiting_q.empty():
            waiting_process = waiting_q.get()[1]
            waiting_arrival = waiting_process.arrival_time
            remain_time = waiting_process.remaining_time
            if time == waiting_arrival:
                schedule.put((remain_time, waiting_arrival, waiting_process))
            else:
                waiting_q.put((waiting_arrival, waiting_process))

        current_ready_list = get_processes_in_queue(schedule)

        current_process = schedule.get()[2]

        event.append(current_process.process_id)

        current_process.remaining_time -= 1
        time += 1
        other_ready_process_waiting_plus_1(current_process.process_id, current_ready_list)

        event.append(time)

        if current_process.remaining_time == 0:
            pass
        else:
            schedule.put((current_process.remaining_time, current_process.arrival_time, current_process))

        process_event_list.append(event)


    # print(process_event_list)


def get_processes_in_queue(queue):
    ps_l = []
    while not queue.empty():
        ps_l.append(queue.get())

    for ele in ps_l:
        queue.put(ele)

    ps_li = []
    for ii in range(len(ps_l)):
        ps_li.append(ps_l[ii][2])

    return ps_li


def other_ready_process_waiting_plus_1(the_id, obj_l):
    new_list = other_process_havent_done(the_id, obj_l)
    for ele in new_list:
        ele.cumulative_waiting_time += 1




def other_process_havent_done(the_id, obj_l):
    new_list = []
    for element in obj_l:
        if element.remaining_time != 0 and element.process_id != the_id:
            new_list.append(element)
    return new_list
