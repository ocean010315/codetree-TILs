import numpy as np

is_moved = [] # 모든 원소가 True여야 최종적으로 이동할 수 있음
knights_rc = [] # is_moved가 전부 True일 때 knights들의 좌표 update

def move_knight(i, d):
    # up
    if d==0:
        tmp = knights[i][0]
        tmp -= 1

        # knigths[i]의 위 영역 탐색
        while tmp >= 0:
            for a in range(knights[i][1], knights[i][1]+knights[i][2]+1):
                # 이동한 위쪽 방향에 벽이 있을 때
                if field[a] == 2:
                    is_moved.append(False)
                    return
                
                # 위쪽에 다른 knights가 있을 때
                for idx, k in enumerate(knights):
                    #knights[i]의 가장 위 row가 다른 knights의 가장 아래 row와 겹치는지?
                    if k[0]+k[1] == tmp:
                        for r in range(k[1], k[1]+k[3]+1):
                            if a==r:
                                is_moved = False
                                return
                    
                    i = idx
                    move_knight(i, d)

            is_moved.append(True)
            knights_rc.append((i, tmp, knights[i][1])) # kngihts의 idx, r, c 저장
        
        is_moved.append(False)

    # right    
    elif d==1:
        tmp = knights[i][2]
        tmp += 1

    # down
    elif d==2:
        tmp = knights[i][0] + knights[i][2]
        tmp += 1

    # left
    else:
        tmp = knights[i][2]
        tmp  -= 1


L, N, Q = [int(i) for i in input().split()]

# initialize field
field = np.empty(shape=(L, L))
for i in range(L):
    row = [int(f) for f in input().split()]
    field[i] = row

# knights setting
knights = np.zeros(shape=(N, 5))
for j in range(N):
    info = [int(k)-1 for k in input().split()] # r, c, h, w, k

    # # field 배열 기준 (0, 0)을 시작 지점으로
    # info[0] -= 1
    # info[1] -= 1

    # # h, w도 바로 더하고 뺄 수 있게
    # info[2] -= 1
    # info[3] -= 1

    info[4] += 1

    knights[j] = info

# fight!
for k in range(Q):
    i, d = [int(f) for f in input().split()]

    move_knight(i, d)
    if is_moved.pop():
        for k in knights_rc:
            idx, r, c = k
            knights[idx][0] = r
            knights[idx][1] = c