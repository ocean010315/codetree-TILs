import heapq

class Task:
    def __init__(self, t, p, u):
        self.t = t
        self.p = p
        self.u = u
        self.domain = u.split("/")[0]

        self.start = None
        self.end = None
    
    def __lt__(self, other):
        if self.p != other.p:
            return self.p < other.p
        else:
            return self.t < other.t
    
    def gap(self):
        return (self.end - self.start)
    
    def setStart(self, t):
        self.start = t
    
    def setEnd(self, t):
        self.end = t

waiting_judger = {} # { j_id : None/task }
waiting_queue = {} # { u : task }
judging = {} # { domain : task(start) }
history = {} # { domain : task(start, end) }

# 100 N u0
def init(N, u):
    global n
    n = N

    for i in range(n):
        waiting_judger[i+1] = None

    task = Task(0, 1, u)
    waiting_queue[u] = task

# 200 t p u
def insert(t, p, u):
    if u in waiting_queue:
        return
    
    newTask = Task(t, p, u)
    waiting_queue[u] = newTask

# 300 t
def startJudging(t):
    judger = None
    for j_id, task in waiting_judger.items():
        if task is None:
            judger = j_id
            break
    
    if judger is not None:
        available = {}
        for _, waitingTask in waiting_queue.items():
            domain = waitingTask.domain

            if domain in judging:
                continue
            
            if domain in history:
                current = history[domain]
                if t < current.start + 3*current.gap():
                    continue
            
            available[waitingTask.u] = waitingTask

        if available:
            available_queue = list(available.values())
            heapq.heapify(available_queue)
            target = heapq.heappop(available_queue)
            if target is not None:
                del waiting_queue[target.u]
                target.setStart(t)
                waiting_judger[judger] = target
                judging[target.domain] = target

# 400 t j_id
def endJudging(t, j_id):
    if j_id in waiting_judger and waiting_judger[j_id] is not None:
        endTask = waiting_judger[j_id]
        del judging[endTask.domain]
        endTask.setEnd(t)
        history[endTask.domain] = endTask
        waiting_judger[j_id] = None

# 500 t
def capture(t):
    print(len(waiting_queue))

### main ###
Q = int(input())
while(Q):
    query = input().split(' ')
    if query[0]=="100":
        init(int(query[1]), query[2])

    elif query[0]=="200":
        insert(int(query[1]), int(query[2]), query[3])

    elif query[0]=="300":
        startJudging(int(query[1]))

    elif query[0]=="400":
        endJudging(int(query[1]), int(query[2]))

    elif query[0]=="500":
        capture(int(query[1]))
    
    Q -= 1