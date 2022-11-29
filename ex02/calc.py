import tkinter as tk
import tkinter.messagebox as tkm

def button_click(event):
    btn = event.widget
    num = btn["text"]
    if num == "=":
        siki = entry.get() #数式の取得
        try:
            
            res = eval(siki) #式の評価
            entry.delete(0,tk.END) #表示されている文字列の削除
            entry.insert(tk.END, res) #結果の挿入

        except:
            tkm.showerror("警告", "無効な式です") #追加4：式が成り立たない場合にエラー文を出す

    elif num == "AC":
        entry.delete(0,tk.END) #追加5：表示されている文字列の削除
    
    
    else:
    #tkm.showinfo("", f"{num}ボタンがクリックされました")
        entry.insert(tk.END,num)

root = tk.Tk()
root.geometry("400x600")

entry = tk.Entry(root, justify = "right", width = 10, font = ("",40))
entry.grid(row = 0, column = 0,columnspan=3)

r,c = 2,2

for i in range(9,-1, -1):
    button = tk.Button(root, text = f"{i}",width = 4, height=2, font =("", 30))
    button.grid(row = r, column= c)
    button.bind("<1>", button_click)
    c -= 1
    if c == -1:
        r += 1
        c = 2 #追加1：数の順序の変更

operators = ["AC","*", "/","+", "="] #追加2：オールクリアボタン、四則演算

r = 1
c = 3

for ope in operators:
    button = tk.Button(root, text = f"{ope}",width = 4, height=2, font =("", 30))
    button.grid(row = r, column= c)
    button.bind("<1>", button_click) #追加3：四則演算の配置の変更
    r += 1

sp_r = 1
sp_c = 0
special_ope = ["√","^2","C"] #ルート、2乗、クリアボタン
for sp in special_ope:
    spbutton = tk.Button(root, text = f"{sp}",width = 4, height=2, font =("", 30))
    spbutton.grid(row = sp_r, column= sp_c)
    sp_c += 1

root.mainloop()