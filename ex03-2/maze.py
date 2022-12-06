import tkinter as tk
import maze_maker as mm
import tkinter.messagebox as tkm

def key_down(event):
    global key
    key = event.keysym

def key_up(event):
    global key
    key = ""

def main_proc():
    global cx,cy,mx,my
    if key == "Up":my -= 1
    if key == "Down":my += 1
    if key == "Left":mx -=1
    if key == "Right":mx += 1
    if key == "w":my -=2#追加１：2倍移動(壁が１つなら乗り越えられる、2つ以上は無理)
    if key == "s":my += 2
    if key == "a":mx -= 2
    if key == "d":mx += 2
    if maze_lst[mx][my] == 1: #移動先が壁だったら
        if key == "Up":
            my += 1
            tkm.showwarning("こうかとん", "いてっ！")#追加3：壁にぶつかったらこうかとんが反応する
        if key == "Down":
            my -= 1
            tkm.showwarning("こうかとん", "いてっ！")
        if key == "Left":
            mx +=1
            tkm.showwarning("こうかとん", "いてっ！")
        if key == "Right":
            mx -= 1
            tkm.showwarning("こうかとん", "いてっ！")
        if key == "w":
            my +=2
            tkm.showwarning("こうかとん", "さすがに無理！")
        if key == "s":
            my -= 2
            tkm.showwarning("こうかとん", "さすがに無理！")
        if key == "a":
            mx += 2
            tkm.showwarning("こうかとん", "さすがに無理！")
        if key == "d":
            mx -= 2
            tkm.showwarning("こうかとん", "さすがに無理！")
    cx,cy = mx*100+50, my*100+50
    canvas.coords("kokaton",cx,cy)
    root.after(100,main_proc)

def count_up():#追加２：カウントダウン
    global tmr
    label["text"] =tmr
    tmr = tmr+1
    root.after(1000,count_up)


if __name__ == "__main__":
    root= tk.Tk()
    root.title("迷えるこうかとん")
    canvas = tk.Canvas(root, width= 1500, height = 900, bg = "black")
    canvas.pack()
    label = tk.Label(root,font=("",80))
    label.pack()

    tmr = 0
    count_up()

    maze_lst = mm.make_maze(15, 9)
    #print(maze_lst)
    mm.show_maze(canvas, maze_lst)

    mx,my = 1,1
    cx,cy = mx*100+50, my*100+50

    gx,gy = 13,7
    gcx,gcy = gx*100+50, gy*100+50



    kokaton = tk.PhotoImage(file = "fig/8.png")

    goal = tk.PhotoImage(file = "fig/6.png")#追加4：ゴール目印としてこうかとんの仲間の画像を右下に配置

    canvas.create_image(cx, cy, 
                        image = kokaton,
                        tag = "kokaton")

    canvas.create_image(gcx, gcy, 
                        image = goal,
                        tag = "goal")
    
    


    key =""
    root.bind("<KeyPress>",key_down)
    root.bind("<KeyRelease>", key_up)
    main_proc()
    root.mainloop()