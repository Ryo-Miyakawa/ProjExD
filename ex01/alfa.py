import random
import datetime
import time

totalalfa = 26
tai = 10 
kesson = 2
chall = 2

def shutudai(alphabet):
    all_chars = random.sample(alphabet, tai)
    print("対象文字")
    for c in all_chars:
        print(c, end=" ")
    print()

    abs_chars = random.sample(all_chars, kesson)
    print("欠損文字（デバッグ用）")
    for c in abs_chars:
        print(c, end=" ")
    print()

    print("表示文字")
    for c in all_chars:
        if c not in abs_chars:
            print(c, end= " ")
    print()

    return abs_chars

def kaitou(abs_chars):
    num = int(input("欠損文字はいくつあるでしょうか？"))
    if num != kesson:
        print("不正解です")
    else:
        print("正解！！！")
        for i in range(num):
            ans = input(f"{i+1}つ目のもじをにゅうりょくしてください")
            if ans not in abs_chars:
                print("不正解です")
                return False
            else:
                abs_chars.remove(ans)
        print("全部正解です")
        return True

if __name__ == "__main__":
    st = time.time()
    alphabet = [chr(i + 65) for i in range(totalalfa)]
    
    for _ in range (chall):
        abs_chars = shutudai(alphabet)
        ret = kaitou(abs_chars)
        if ret:
            break
        else:
            print("-"*20)

    ed = time.time()
    print(f"所要時間：{(ed -st):.2f}秒")

    
