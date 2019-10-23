width, height = map(int, input().split(" "))

lost = False
cords = ()
dict_dir = {'N':1, 'E':2, 'S':3, 'W':4}
dict_rid = {1:'N', 2:'E', 3:'S', 4:'W'}
dict = { 'N':(0,1), 'S':(0,-1), 'E':(1,0), 'W':(-1,0)}
while cords != ():
    inp = list(map(input().split(" ")))
    cords = (inp[0], inp[1])
    moves = input()
    direction = dict_dir.get(inp[2])
    for i in range(len(moves)):
        if moves[i] == 'F':
            cords += dict.get(direction[i])
        elif moves[i] == 'R':
            direction += 1
            direction %= 4
        elif moves[i] == 'L':
            direction -= 1
            direction %= 4
        if cords[0] > width or cords[1] > height:
            lost = True
            break
    print(cords, dict_rid.get(direction))
    if lost:
        print("LOST")
