class Process:

    def __init__(self, process_id, burst_time=0, arrival_time=0):
        self.process_id = process_id
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.cumulative_waiting_time = 0
        self.arrival_time = arrival_time
