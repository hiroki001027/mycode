import numpy as np
import cv2
import tkinter as tk
import copy


red = (128, 128, 255)
dark_red = (64, 64, 200)
green = (64, 180, 64)
dark_green = (64, 128, 64)
blue = (255, 128, 128)
dark_blue = (200, 64, 64)
gray = (200, 200, 200)
dark = (0,0,0)


def keycontrol_left(key,x,y,v):
    # if key == 37:
    if key == ord('a'):
        x += -v
        user = np.array([x,y])
    return x

def keycontrol_right(key,x,y,v):
    # if key == 39:
    if key == ord('d'):
        x += v
        user = np.array([x,y])
    return x

def keycontrol_down(key,x,y,v):
    # if key == 40:
    if key == ord('s'):
        y += v
        user = np.array([x,y])
    return y
        
def keycontrol_up(key,x,y,v):
    # if key == 38:
    if key == ord('w'):
        y += -v
        user = np.array([x,y])
    return y


def keycontrol(x,y,reslut,answer_which,build_info):
    if reslut and all(answer_which):
        x = keycontrol_left(key,x,y,v)
        x = keycontrol_right(key,x,y,v)
        y = keycontrol_up(key,x,y,v)
        y = keycontrol_down(key,x,y,v)
    
    else:
        if answer_which[0]:
            x = keycontrol_right(key,x,y,v)

        if answer_which[1]:
            x = keycontrol_left(key,x,y,v)

        if answer_which[2]:
            y = keycontrol_down(key,x,y,v)

        if answer_which[3]:
            y = keycontrol_up(key,x,y,v)
            
        user = np.array([x,y])
        
        answer ,answer_which,answernew,coodinate_transfomation = conclusion_answer(build_info,user,v)
        
        x = coodinate_transfomation[0]
        y = coodinate_transfomation[1]

    return x,y
            


def conclusion_answer(build_info,coodinate_transfomation,v):
    answer = []
    answernew = False
    answer_which = [True,True,True,True]
    
    for n in range(len(build_info)):
        coodinate = build_info[n]
        
        coodinate_left = coodinate[0][0]
        coodinate_up = coodinate[0][1]
        coodinate_right = coodinate[1][0]
        coodinate_dowm = coodinate[1][1]
        
        
        if (coodinate_left < coodinate_transfomation[0] < coodinate_right) and (coodinate_up < coodinate_transfomation[1] < coodinate_dowm):
            answer.append(False)
            #右から建物にあたるとき
            if coodinate_left < coodinate_transfomation[0] <= coodinate_left + v+1:
                answer_which[0] = False
                coodinate_transfomation = np.array([coodinate_left,coodinate_transfomation[1]])
                
            #左から建物にあたるとき
            if coodinate_right - v-1 <= coodinate_transfomation[0] < coodinate_right:
                answer_which[1] = False
                coodinate_transfomation = np.array([coodinate_right,coodinate_transfomation[1]])
                
            #上から建物にあたるとき
            if coodinate_up < coodinate_transfomation[1] <= coodinate_up + v+1:
                answer_which[2] = False
                coodinate_transfomation = np.array([coodinate_transfomation[0],coodinate_up])

            #下から建物に当たるとき
            if coodinate_dowm - v-1 <= coodinate_transfomation[1] < coodinate_dowm:
                answer_which[3] = False
                coodinate_transfomation = np.array([coodinate_transfomation[0],coodinate_dowm])

        else:
            answer.append(True)
            
        if (coodinate_left < coodinate_transfomation[0] < coodinate_right) and (coodinate_up < coodinate_transfomation[1] < coodinate_dowm):
            answernew = False
        else:
            answernew = True
        
    answer = all(answer)
            
    return answer ,answer_which,answernew,coodinate_transfomation
        
            
    

def user_plot(img ,user):
    cv2.circle(img ,user,5,green,thickness=2)
    

def build_plot(img):
    build_info = []
    
    x_build = np.random.randint(0, width - 100, n_rectangle)
    y_build = np.random.randint(0, height - 100, n_rectangle)
    width_rect_build = np.random.randint(50, 100, n_rectangle)
    height_rect_build = np.random.randint(50, 100, n_rectangle)

    
    for n in range(len(x_build)):
        if not(x_build[n] < goal[0] < x_build[n] +width_rect_build[n]) and not(y_build[n] < goal[0] < y_build[n] + height_rect_build[n]):
            cv2.rectangle(img, (x_build[n], y_build[n]), (x_build[n] +width_rect_build[n], y_build[n] + height_rect_build[n]), blue,-1)
            build_info.append(np.array([[x_build[n], y_build[n]],[x_build[n] + width_rect_build[n], y_build[n] + height_rect_build[n]]]))
    
        # if x_build[n] < goal[0] < x_build[n] +width_rect_build[n] and y_build[n] < goal[0] < y_build[n] + height_rect_build[n]:
        #     build_info[n] = np.array([0,0])
            
    cv2.circle(img ,goal,goal_range,red,thickness=2)
    
    return build_info

v_NPC = 2
    
def NPC_update(img,user,NPC_position):
    for n in range(NPC_number):
        if user[0] > NPC_position[n][0]:
            NPC_position[n][0] += np.random.randint(0,v_NPC)
            
        if user[0] < NPC_position[n][0]:
            NPC_position[n][0] -= np.random.randint(0,v_NPC)
            
            if user[0] == NPC_position[n][0]:
                    NPC_position[n][1] += np.random.randint(-v_NPC,v_NPC)
                
        if user[1] < NPC_position[n][1]:
            NPC_position[n][1] -= np.random.randint(0,v_NPC)
            
        if user[1] > NPC_position[n][1]:
            NPC_position[n][1] += np.random.randint(0,v_NPC)
            
            if user[1] == NPC_position[n][1]:
                    NPC_position[n][0] += np.random.randint(-v_NPC,v_NPC)
            
        
    return NPC_position


def NPC_conclusion_build(img,build_info,NPC_position):
    for n in range(NPC_number):
        reslut,answer_which_NPC,answernew,NPC_position[n] = conclusion_answer(build_info,NPC_position[n],v_NPC)
        # if not answer_which_NPC[0] or NPC_position[n][0] > width:
        #     NPC_position[n][0] = NPC_position[n][0]-v_NPC
            
        # if not answer_which_NPC[1] or 0 > NPC_position[n][0]:
        #     NPC_position[n][0] = NPC_position[n][0]+v_NPC
            
        # if not answer_which_NPC[2] or NPC_position[n][1] > height:
        #     NPC_position[n][1] = NPC_position[n][1]-v_NPC
            
        # if not answer_which_NPC[3] or 0 > NPC_position[n][1]:
        #     NPC_position[n][1] = NPC_position[n][1]+v_NPC
    
    return NPC_position
    
    

def NPC_plot(img,NPC_position):
    for n in range(NPC_number):
        cv2.circle(img,NPC_position[n],r_NPC,dark_red, thickness=2)
            
        # print(NPC_position)
        
def fail_verdict(user,NPC_position,NPC_range):
    judgment = False
    for n in range(NPC_number):
        if NPC_position[n][0] - NPC_range < user[0] < NPC_position[n][0] + NPC_range and NPC_position[n][1] - NPC_range < user[1] < NPC_position[n][1] + NPC_range:
            print("gameover")
            return True
            


n_rectangle = np.random.randint(15,20)
height, width = 600 , 600
size = 600
img = np.full((height,width,3),500, dtype=np.uint8)

x_build = np.random.randint(0, width - 100, n_rectangle)
y_build = np.random.randint(0, height - 100, n_rectangle)
width_rect_build = np.random.randint(50, 100, n_rectangle)
height_rect_build = np.random.randint(50, 100, n_rectangle)

start = np.array([10,10])
goal_range = 10
goal = np.array([np.random.randint(width/2,width),np.random.randint(height/2,height)])
x_user,y_user = np.random.randint(0,width/2),np.random.randint(0,height/2)
user = np.array([x_user,y_user])
x_user_before = 0
y_user_before = 0

NPC_number = np.random.randint(15,20)
x_NPC = np.random.randint(0, width,NPC_number)
y_NPC = np.random.randint(0, width,NPC_number)
r_NPC = 5

NPC_range = 5

NPC_position = []
for n in range(NPC_number):
    NPC = np.array([x_NPC[n],y_NPC[n]])
    NPC_position.append(NPC)

while True:
    img = np.full((height, width, 3),500, dtype=np.uint8)

    np.random.seed(20)
    
    build_info = build_plot(img)
    
    key = cv2.waitKey(1)
    
    v = 10
    x_user_before = copy.deepcopy(x_user)
    y_user_before = copy.deepcopy(y_user)
    
    reslut,answer_which,answernew,user = conclusion_answer(build_info,user,v)
    x_user,y_user = keycontrol(x_user,y_user,reslut,answer_which,build_info)
    
    
    # answer = any(item == False for item in answer_which)
    print(user)
    # print(re)
    user = np.array([x_user,y_user])
    # if not all(answer_which):
    #     user = user_re
    # else:
    #     user = np.array([x_user,y_user])
        
    
    
        
    NPC_position = NPC_update(img,user,NPC_position) 
    NPC_position = NPC_conclusion_build(img,build_info,NPC_position)
    NPC_plot(img,NPC_position)
        
    user_plot(img,user)
    
    cv2.imshow("img",img)
 
    if key == ord('q'):
        break
    
    if goal[0] - goal_range < user[0] < goal[0] + goal_range and goal[1] - goal_range < user[1] < goal[1] + goal_range:
        print("clear")
        break    

    if fail_verdict(user,NPC_position,NPC_range):
        n_rectangle = np.random.randint(15,20)
        height, width = 600 , 600
        size = 600
        img = np.full((height,width,3),500, dtype=np.uint8)

        x_build = np.random.randint(0, width - 100, n_rectangle)
        y_build = np.random.randint(0, height - 100, n_rectangle)
        width_rect_build = np.random.randint(50, 100, n_rectangle)
        height_rect_build = np.random.randint(50, 100, n_rectangle)

        start = np.array([10,10])
        goal_range = 10
        goal = np.array([np.random.randint(width/2,width),np.random.randint(height/2,height)])
        x_user,y_user = np.random.randint(0,width/2),np.random.randint(0,height/2)
        user = np.array([x_user,y_user])
        x_user_before = 0
        y_user_before = 0

        NPC_number = np.random.randint(15,20)
        y_NPC = np.random.randint(0, width,NPC_number)
        r_NPC = 5

        NPC_range = 5

        NPC_position = []
        for n in range(NPC_number):
            NPC = np.array([x_NPC[n],y_NPC[n]])
            NPC_position.append(NPC)
        
    
cv2.destroyAllWindows()
    