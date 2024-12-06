import random
from collections import deque


class Process:
    def init(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority


random.seed(42)
def generate_processes(num_processes):
    processes = []
    for i in range(num_processes):
        arrival_time = random.randint(0, 10)
        burst_time = random.randint(1, 10)
        priority = random.randint(1, 5)  
        processes.append(Process(i + 1, arrival_time, burst_time, priority))
    return processes



def round_robin(processes, time_quantum):
    queue = deque(sorted(processes, key=lambda p: p.arrival_time))
    current_time = 0
    execution_log = []

    while queue:
        process = queue.popleft()
        execution_time = min(process.remaining_time, time_quantum)
        process.remaining_time -= execution_time
        current_time += execution_time
        execution_log.append((process.pid, execution_time, process.remaining_time))

        
        if process.remaining_time > 0:
            queue.append(process)

    return execution_log


def fcfs(processes):
    processes.sort(key=lambda p: p.arrival_time)
    current_time = 0
    log = []

    for process in processes:
        start_time = max(current_time, process.arrival_time)
        wait_time = start_time - process.arrival_time
        finish_time = start_time + process.burst_time
        log.append((process.pid, start_time, finish_time, wait_time))
        current_time = finish_time

    return log



def priority_scheduling(processes):
    processes.sort(key=lambda p: (p.arrival_time, p.priority))
    current_time = 0
    log = []

    for process in processes:
        start_time = max(current_time, process.arrival_time)
        finish_time = start_time + process.burst_time
        log.append((process.pid, start_time, finish_time, process.priority))
        current_time = finish_time

    return log



def analyze_efficiency(log, is_fcfs=True):
    total_wait_time = 0
    total_turnaround_time = 0

    for record in log:
        if is_fcfs:
            pid, start_time, finish_time, wait_time = record
            turnaround_time = finish_time - start_time + wait_time
        else:
            pid, execution_time, remaining_time = record
            turnaround_time = execution_time
            wait_time = max(0, turnaround_time - execution_time)
        total_wait_time += wait_time
        total_turnaround_time += turnaround_time

    avg_wait_time = total_wait_time / len(log)
    avg_turnaround_time = total_turnaround_time / len(log)

    return avg_wait_time, avg_turnaround_time


if name == "main":
    num_processes = 5
    time_quantum = 3
    processes = generate_processes(num_processes)

   
    print("Round Robin")
    rr_log = round_robin(processes.copy(), time_quantum)
    for log in rr_log:
        print(f"Process {log[0]} executed for {log[1]} time units, remaining: {log[2]} units")
    avg_wait_rr, avg_ta_rr = analyze_efficiency(rr_log, is_fcfs=False)
    print(f"RR Avg Wait Time: {avg_wait_rr}, Avg Turnaround Time: {avg_ta_rr}")

    
    print("\nFirst Come First Serve (FCFS)")
    fcfs_log = fcfs(processes.copy())
    for log in fcfs_log:
        print(f"Process {log[0]} started at {log[1]}, finished at {log[2]}, waited {log[3]} units")
    avg_wait_fcfs, avg_ta_fcfs = analyze_efficiency(fcfs_log)
    print(f"FCFS Avg Wait Time: {avg_wait_fcfs}, Avg Turnaround Time: {avg_ta_fcfs}")

    
    print("\nPriority Scheduling")
    ps_log = priority_scheduling(processes.copy())
    for log in ps_log:
        print(f"Process {log[0]} started at {log[1]}, finished at {log[2]}, priority {log[3]}")
        import random
from collections import deque

class Process:
    def init(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.original_priority = priority  

    def str(self):
        return f"Process {self.pid}: arrival={self.arrival_time}, burst={self.burst_time}, priority={self.priority}"


random.seed(42)

def generate_processes(num_processes):
    processes = []
    for i in range(num_processes):
        arrival_time = random.randint(0, 10)
        burst_time = random.randint(1, 10)
        priority = random.randint(1, 5) 
        processes.append(Process(i + 1, arrival_time, burst_time, priority))
    return processes



def sjf(processes):
    processes.sort(key=lambda p: (p.arrival_time, p.burst_time))  
    current_time = 0
    log = []
    
    while processes:
    
        available_processes = [p for p in processes if p.arrival_time <= current_time]
        if not available_processes:
          
            current_time = min(p.arrival_time for p in processes)
            available_processes = [p for p in processes if p.arrival_time <= current_time]
        
     
        process = min(available_processes, key=lambda p: p.burst_time)
        start_time = max(current_time, process.arrival_time)
        finish_time = start_time + process.burst_time
        wait_time = start_time - process.arrival_time
        log.append((process.pid, start_time, finish_time, wait_time))
        current_time = finish_time
        processes.remove(process)

    return log



def priority_scheduling_with_aging(processes, aging_interval=3):
    processes.sort(key=lambda p: p.arrival_time)
    current_time = 0
    log = []
    
    while processes:
        
        available_processes = [p for p in processes if p.arrival_time <= current_time]
        if not available_processes:
            
            current_time = min(p.arrival_time for p in processes)
            available_processes = [p for p in processes if p.arrival_time <= current_time]
        
        
        for p in available_processes:
            if current_time - p.arrival_time >= aging_interval:
                p.priority = max(1, p.priority - 1)  

       
        process = min(available_processes, key=lambda p: (p.priority, p.arrival_time))  
        start_time = max(current_time, process.arrival_time)
        finish_time = start_time + process.burst_time
        wait_time = start_time - process.arrival_time
        log.append((process.pid, start_time, finish_time, process.priority, wait_time))
        current_time = finish_time
        processes.remove(process)

    return log


def analyze_efficiency(log):
    total_wait_time = 0
    total_turnaround_time = 0

    for record in log:
        pid, start_time, finish_time, wait_time = record[:4]
        turnaround_time = finish_time - start_time
        total_wait_time += wait_time
        total_turnaround_time += turnaround_time

    avg_wait_time = total_wait_time / len(log)
    avg_turnaround_time = total_turnaround_time / len(log)

    return avg_wait_time, avg_turnaround_time


if name == "main":
    num_processes = 5
    time_quantum = 3
    processes = generate_processes(num_processes)
   
    print("Round Robin")
    rr_log = round_robin(processes.copy(), time_quantum)
    for log in rr_log:
        print(f"Process {log[0]} executed for {log[1]} time units, remaining: {log[2]} units")
    avg_wait_rr, avg_ta_rr = analyze_efficiency(rr_log)
    print(f"RR Avg Wait Time: {avg_wait_rr}, Avg Turnaround Time: {avg_ta_rr}")

    
    print("\nFirst Come First Serve (FCFS)")
    fcfs_log = fcfs(processes.copy())
    for log in fcfs_log:
        print(f"Process {log[0]} started at {log[1]}, finished at {log[2]}, waited {log[3]} units")
    avg_wait_fcfs, avg_ta_fcfs = analyze_efficiency(fcfs_log)
    print(f"FCFS Avg Wait Time: {avg_wait_fcfs}, Avg Turnaround Time: {avg_ta_fcfs}")

   
    print("\nPriority Scheduling")
    ps_log = priority_scheduling(processes.copy())
    for log in ps_log:
        print(f"Process {log[0]} started at {log[1]}, finished at {log[2]}, priority {log[3]}")
    avg_wait_ps, avg_ta_ps = analyze_efficiency(ps_log)
    print(f"PS Avg Wait Time: {avg_wait_ps}, Avg Turnaround Time: {avg_ta_ps}")

    print("\nShortest Job First (SJF)")
    sjf_log = sjf(processes.copy())
    for log in sjf_log:
        print(f"Process {log[0]} started at {log[1]}, finished at {log[2]}, waited {log[3]} units")
    avg_wait_sjf, avg_ta_sjf = analyze_efficiency(sjf_log)
    print(f"SJF Avg Wait Time: {avg_wait_sjf}, Avg Turnaround Time: {avg_ta_sjf}")


    print("\nPriority Scheduling with Aging")
    ps_aging_log = priority_scheduling_with_aging(processes.copy())
    for log in ps_aging_log:
        print(f"Process {log[0]} started at {log[1]}, finished at {log[2]}, priority {log[3]}, waited {log[4]} units")
    avg_wait_ps_aging, avg_ta_ps_aging = analyze_efficiency(ps_aging_log)
    print(f"PS with Aging Avg Wait Time: {avg_wait_ps_aging}, Avg Turnaround Time: {avg_ta_ps_aging}")
