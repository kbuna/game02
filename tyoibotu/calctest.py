





関数定義
calc


# view
# bg・見下ろし
# 　・真横


# ・マス管理　透明
# ・

# move

# ・上下左右チェック


# ・壁チェック？
# ・ランダム






import time

def press_button(button, plus):
    print(f"ボタン {button} が押されました。")
    return plus

def main():
    money = 0
    plus = 1

    while True:
        money += plus
        print(f"お金: {money} 円", end='\r')  # '\r' はカーソルを行の先頭に移動させるための制御文字

        # ボタンの押下を模擬
        button_pressed = input("ボタンを押してください (A, B, C): ")
        
        # ボタンごとに対応する数値を加算
        if button_pressed == 'A':
            plus = press_button('A', 2)
        elif button_pressed == 'B':
            plus = press_button('B', 5)
        elif button_pressed == 'C':
            plus = press_button('C', 10)
        else:
            print("無効なボタンです。再度押してください。")
            continue

if __name__ == "__main__":
    main()
