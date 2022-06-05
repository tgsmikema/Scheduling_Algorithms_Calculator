class CyclicProcess:

    def __init__(self, c, p, d, process_id):
        self.process_id = process_id
        self.c = c
        self.p = p
        self.d = d
        self.remaining_c = c
        self.next_deadline = d
        self.previous_on = False

