import tkinter as tk
from tkinter import messagebox

class MoneyClicker:
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title("Money Clicker")
        self.money = 0
        self.property = 0

        #Money初期表示
        self.Money_label = tk.Label(self.root, text="Moneys: 0")
        self.Money_label.pack(pady=5)
        #AutoGain
        self.auto_label = tk.Label(self.root, text="Auto Gain: 0")
        self.auto_label.pack(pady=5)

        #Workボタン
        self.work = tk.Button(self.root, text="Work!", command=self.click_work)
        self.work.pack(pady=10)
        #buyボタン
        self.buy = tk.Button(self.root, text="Buy Property", command=self.get_Property)
        self.buy.pack(pady=3)

      

        self.auto_Gain()

    def click_work(self):
        self.money += 1
        self.update_Money_count()

    def get_Property(self):
        #もしカウントが10より大きい場合
        if self.money >= 10:
            #10消費してオートを増やす
            self.money -= 10
            self.property += 1
            #表示を更新
            self.update_Money_count()
            self.update_Gain()
            self.auto_Gain()
        else:
            messagebox.showinfo("お金が足りません", "財産を手に入れるには、少なくとも10の元手が必要です")

    def auto_Gain(self):
        #もし財産が1つでもあれば、財産の数だけマネーを増やす
        if self.property > 0:
            self.money += self.property
            self.update_Money_count()
            self.root.after(1000, self.auto_Gain)

    #現在のマネーの表示
    def update_Money_count(self):
        self.Money_label.config(text=f"Moneys: {self.money}")
    #現在の利得の表示
    def update_Gain(self):
        self.auto_label.config(text=f"Auto Gain: {self.property}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    clicker = MoneyClicker()
    clicker.run()