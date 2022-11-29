import tkinter as tk
import tkinter.messagebox as tkm

def button_click(event):
    btn = event.widget
    num = btn["text"]
    if num == "=":
        siki = entry.get() #数式の取得
        res = eval(siki) #式の評価
        entry.delete(0,tk.END) #表示されている文字列の削除
        entry.insert(tk.END, res) #結果の挿入
    else:
    #tkm.showinfo("", f"{num}ボタンがクリックされました")
        entry.insert(tk.END,num)

root = tk.Tk()
root.geometry("300x500")

entry = tk.Entry(root, justify = "right", width = 10, font = ("",40))
entry.grid(row = 0, column = 0,columnspan=3)
r,c = 1,2
for i in range(9,-1, -1):
    button = tk.Button(root, text = f"{i}",width = 4, height=2, font =("", 30))
    button.grid(row = r, column= c)
    button.bind("<1>", button_click)
    c -= 1
    if c == -1:
        r += 1
        c = 2 #追加1：数の順序の変更
operators = ["+", "="]
for ope in operators:
    button = tk.Button(root, text = f"{ope}",width = 4, height=2, font =("", 30))
    button.grid(row = r, column= c)
    button.bind("<1>", button_click)
    c += 1
    if c%3 == 0:
        r += 1
        c = 0

root.mainloop()