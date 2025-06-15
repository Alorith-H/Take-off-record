#pip install customtkinter
#图形界面依赖
#customtkinter现代化图形库

import customtkinter as ctk
#引用图形界面依赖
from datetime import datetime
#用于获取时间

ctk.set_appearance_mode("System")
#设置界面外观模式 或 "Light", "Dark" ,跟随系统
ctk.set_default_color_theme("blue")

'''
ctk.set_default_color_theme("blue")     # 默认蓝色主题
ctk.set_default_color_theme("green")    # 绿色主题
ctk.set_default_color_theme("dark-blue")# 深蓝色主题
'''

class LoggerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("起飞日志")
        self.geometry("400x250")

        self.label = ctk.CTkLabel(self, text="请输入起飞备注：", font=("微软雅黑", 16))
        self.label.pack(pady=20)
        #ctk.CTkLabel(...)是 customtkinter 中的标签控件（比 tkinter 的 Label 美观），用来显示文字提示。
        #pack(pady=20)是布局方法，表示“垂直方向的边距是20像素”。

        self.entry = ctk.CTkEntry(self, width=300, font=("微软雅黑", 14))
        self.entry.pack(pady=10)
        #在图形界面中创建一个输入框，供用户输入文字。

        self.button = ctk.CTkButton(self, text="记录事件", command=self.save_log)
        self.button.pack(pady=10)
        #按钮，command指令调用函数。

        self.status = ctk.CTkLabel(self, text="", font=("微软雅黑", 12), text_color="gray")
        self.status.pack(pady=5)
        #也是文本框，不过没有内容。

    def save_log(self):
        content = self.entry.get().strip()
        #从输入框中获取用户输入的文字，并去掉首尾的空格。
        #self.entry	指之前创建的 CTkEntry 输入框组件。
        #.get()	调用 .get() 方法来获取输入框中的文本内容。
        #.strip()	去掉用户输入内容开头和结尾的空格、换行符等。
        if not content:
            #判断用户是否输入。
            self.status.configure(text="请输入内容再记录")
            #修改界面上的某个标签（self.status）的文字内容，显示为：“请输入内容再记录”
            return

        #获取当前日期和时间，并格式化成字符串，再拼接上用户输入的内容，形成一条日志记录。
        now = datetime.now()
        #获取当前系统的日期和时间（精确到秒）。
        date_str = now.strftime("%Y-%m-%d")
        #将 now 格式化为日期字符串，例如"2025-06-15"
        time_str = now.strftime("%H:%M:%S")
        #将 now 格式化为时间字符串，例如"14:32:18"
        log_entry = f"{date_str} {time_str} - {content}\n"
        #使用f字符串拼接出完整日志条目，\n代表换行。
        #f"...{...}..."	是 f字符串，可以将变量值插入到字符串中。

        filename = f"log.txt"
        #文件名为log.txt，
        with open(filename, "a", encoding="utf-8") as f:
            f.write(log_entry)
            #以追加模式("a")打开文件 filename，用 UTF-8 编码写入 log_entry 内容，然后自动关闭文件。
            #with ... as f:：Python 的上下文管理器，会在代码块结束时自动关闭文件，不用手动调用 f.close()。

        self.status.configure(text="✅ 已记录！")
        self.entry.delete(0, ctk.END)
        #清空输入框里的内容。
if __name__ == "__main__":
    #主函数
    app = LoggerApp()
    app.mainloop()