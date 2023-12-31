import heapq

waiting_judger = [] # queue(J_id)
waiting_queue = [] # priority queue
judging = []
history = []

class Task:
    def __init__(self, t, p, u):
        self.t = t
        self.p = p
        self.u = u

        self.start = None
        self.j_id = None

        self.end = None
    
    def __lt__(self, other):
        if self.p!=other.p:
            return self.p < other.p
        else: return self.t < other.t

    def getDomain(self):
        return self.u.split('/')[0]

    def startTask(self, start, j_id):
        self.start = start
        self.j_id = j_id

    def endTask(self, end):
        self.end = end

# 100 N u0
def init(N, u):
    global n
    n = int(N)
    for i in range(n):
        heapq.heappush(waiting_judger, i+1) # i+1로 machine 오름차순 정렬
    
    task = Task(0, 1, u)
    heapq.heappush(waiting_queue, task)

# 200 t p u
def insert(t, p, u):
    for waiting_task in waiting_queue:
        if waiting_task.u==u:
            return
    
    task = Task(t, p, u)
    heapq.heappush(waiting_queue, task)

# 300 t
def start(t):
    if waiting_queue and waiting_judger:
        target = heapq.heappop(waiting_queue)

        # domain
        domain = target.getDomain()
        for j in judging:
            if domain==j.getDomain(): # 같은 도메인이라면 다음 task 확인하기
                tmp = heapq.heappop(waiting_queue)
                heapq.heappush(waiting_queue, target)    
                target = tmp
                
        # start + 3 * gap
        if history:
            for i in range(len(history)):
                lastTask = history[len(history)-i-1]
                if lastTask.getDomain()==target.getDomain():
                    lastStart = lastTask.start
                    lastEnd = lastTask.end
                    if t < (lastStart+(lastEnd-lastStart)*3):
                        heapq.heappush(waiting_queue, target)
                        return
        
        # start
        judger = heapq.heappop(waiting_judger)
        target.startTask(t, judger)
        judging.append(target)

# 400 t J_id
def end(t, j_id):
    for task in judging:
        if task.j_id==j_id:
            judging.remove(task)
            task.endTask(t)
            history.append(task)
            heapq.heappush(waiting_judger, j_id)
            return

# 500
def capture(t):
    print(len(waiting_queue))


### main ###
Q = int(input())
while(Q):

    query = input().split(' ')
    if query[0]=="100":
        init(query[1], query[2])

    elif query[0]=="200":
        insert(int(query[1]), int(query[2]), query[3])

    elif query[0]=="300":
        start(int(query[1]))

    elif query[0]=="400":
        end(int(query[1]), int(query[2]))

    elif query[0]=="500":
        capture(int(query[1]))
    
    Q -= 1