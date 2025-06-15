import customtkinter as ctk
from datetime import datetime


class LoggerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("起飞日志")
        self.geometry("500x500")

        # --- 创建页面容器 ---
        # 三个页面：输入页、日志页、统计页，互斥显示
        self.page_input = ctk.CTkFrame(self)
        self.page_logs = ctk.CTkFrame(self)
        self.page_stats = ctk.CTkFrame(self)

        # 初始都 pack（填满），但先隐藏日志和统计页
        for page in (self.page_input, self.page_logs, self.page_stats):
            page.pack(fill="both", expand=True)
        self.page_logs.pack_forget()
        self.page_stats.pack_forget()

        # --- 输入页面控件 ---
        self.center_frame = ctk.CTkFrame(self.page_input, fg_color="transparent")
        self.center_frame.pack(expand=True)

        # 提示标签
        self.label = ctk.CTkLabel(self.center_frame, text="请输入起飞备注：", font=ctk.CTkFont("微软雅黑", 18, "bold"))
        self.label.pack(pady=10)

        # 文本输入框
        self.entry = ctk.CTkEntry(self.center_frame, width=420, font=ctk.CTkFont("微软雅黑", 14))
        self.entry.pack(pady=10)

        # 按钮容器（水平排列）
        button_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        # 记录事件按钮，点击保存日志
        self.save_button = ctk.CTkButton(button_frame, text="记录事件", command=self.save_log, width=140, corner_radius=12)
        self.save_button.pack(side="left", padx=10)

        # 查看当天日志按钮，切换到日志页面
        self.view_button = ctk.CTkButton(button_frame, text="查看当天日志", command=self.show_logs_page, width=140, corner_radius=12)
        self.view_button.pack(side="left", padx=10)

        # 状态提示标签，用于显示保存成功或错误消息
        self.status = ctk.CTkLabel(self.center_frame, text="", font=ctk.CTkFont("微软雅黑", 12), text_color="gray")
        self.status.pack(pady=10)

        # --- 日志页面控件 ---
        self.log_title_frame = ctk.CTkFrame(self.page_logs)
        self.log_title_frame.pack(fill="x")

        # 日志页标题
        self.log_label = ctk.CTkLabel(self.log_title_frame, text="📜 当天日志", font=ctk.CTkFont("微软雅黑", 20, "bold"))
        self.log_label.pack(side="left", padx=20, pady=10)

        # 返回按钮，返回输入页
        self.back_button = ctk.CTkButton(self.log_title_frame, text="返回", command=self.show_input_page, width=80, corner_radius=10)
        self.back_button.pack(side="right", padx=10, pady=10)

        # 统计按钮，跳转到统计页面
        self.stats_button = ctk.CTkButton(self.log_title_frame, text="统计", command=self.show_stats_page, width=80, corner_radius=10)
        self.stats_button.pack(side="right", padx=10, pady=10)

        # 日志文本框，用于显示日志内容，禁用编辑，自动换行
        self.log_textbox = ctk.CTkTextbox(self.page_logs, width=460, height=320, corner_radius=12, wrap="word")
        self.log_textbox.pack(pady=20, padx=20)
        self.log_textbox.configure(state="disabled")

        # --- 统计页面控件 ---
        self.stats_title_frame = ctk.CTkFrame(self.page_stats)
        self.stats_title_frame.pack(fill="x")

        # 统计页标题
        self.stats_label = ctk.CTkLabel(self.stats_title_frame, text="📊 统计信息", font=ctk.CTkFont("微软雅黑", 20, "bold"))
        self.stats_label.pack(side="left", padx=20, pady=10)

        # 返回日志页按钮
        self.stats_back_button = ctk.CTkButton(self.stats_title_frame, text="返回", command=self.show_logs_page, width=80, corner_radius=10)
        self.stats_back_button.pack(side="right", padx=20, pady=10)

        # 统计信息显示区
        self.stats_frame = ctk.CTkFrame(self.page_stats, width=460, height=350)
        self.stats_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def save_log(self):
        """保存日志到文件"""
        content = self.entry.get().strip()
        if not content:
            # 如果输入为空，提示用户
            self.status.configure(text="请输入内容再记录")
            return

        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        # 格式化日志：日期 时间 - 内容
        log_entry = f"{date_str} {time_str} - {content}\n"

        filename = "log.txt"
        with open(filename, "a", encoding="utf-8") as f:
            f.write(log_entry)

        # 显示成功提示，3秒后清除
        self.status.configure(text="✅ 已记录！")
        self.entry.delete(0, ctk.END)
        self.entry.focus()
        self.after(3000, lambda: self.status.configure(text=""))

    def show_logs_page(self):
        """显示当天日志"""
        today = datetime.now().strftime("%Y-%m-%d")
        filename = "log.txt"
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            # 文件不存在，显示提示
            self.display_log_text("日志文件不存在。")
            return

        # 过滤出当天日志
        today_logs = [line for line in lines if line.startswith(today)]

        self.log_textbox.configure(state="normal")  # 允许编辑以插入内容
        self.log_textbox.delete("0.0", ctk.END)    # 清空旧内容

        if today_logs:
            for line in today_logs:
                if " - " in line:
                    # 分割时间和内容
                    time_part, content = line.split(" - ", 1)
                    # 时间部分使用蓝色并带下划线
                    self.log_textbox.insert(ctk.END, f"{time_part} ", "time")
                    # 内容部分用默认黑色
                    self.log_textbox.insert(ctk.END, f"- {content}", "content")
                else:
                    self.log_textbox.insert(ctk.END, line, "content")
                # 每条日志后插入灰色分隔线
                self.log_textbox.insert(ctk.END, "—" * 50 + "\n", "divider")
        else:
            # 没有日志时显示提示
            self.log_textbox.insert(ctk.END, "今天没有记录任何日志。")

        # 配置文本标签样式
        self.log_textbox.tag_config("time", foreground="#2563eb", underline=True)
        self.log_textbox.tag_config("content", foreground="#000000")
        self.log_textbox.tag_config("divider", foreground="#aaaaaa")

        self.log_textbox.configure(state="disabled")  # 禁止编辑

        # 页面切换显示日志页，隐藏其它页
        self.page_input.pack_forget()
        self.page_stats.pack_forget()
        self.page_logs.pack(fill="both", expand=True)

    def show_stats_page(self):
        """统计日志信息并显示"""
        filename = "log.txt"
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            self.display_stats_text("日志文件不存在，无法统计。")
            return

        now = datetime.now()
        year_str = now.strftime("%Y")
        month_str = now.strftime("%Y-%m")
        day_str = now.strftime("%Y-%m-%d")

        count_year = 0
        count_month = 0
        count_day = 0

        timestamps = []

        # 遍历日志行，提取时间并统计
        for line in lines:
            try:
                date_time_str = line.split(" - ")[0]
                dt = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
                timestamps.append(dt)

                if dt.strftime("%Y") == year_str:
                    count_year += 1
                    if dt.strftime("%Y-%m") == month_str:
                        count_month += 1
                    if dt.strftime("%Y-%m-%d") == day_str:
                        count_day += 1
            except Exception:
                continue

        # 计算平均间隔时间（小时）
        avg_interval_hours = "无数据"
        if len(timestamps) > 1:
            timestamps.sort()
            total_diff = (timestamps[-1] - timestamps[0]).total_seconds()
            avg_sec = total_diff / (len(timestamps) - 1)
            avg_interval_hours = f"{avg_sec / 3600:.2f} 小时"

        # 清空旧统计内容
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # 统计结果文字
        stats_text = (
            f"📅 今年记录次数：{count_year} 次\n"
            f"📅 本月记录次数：{count_month} 次\n"
            f"📅 今日记录次数：{count_day} 次\n"
            f"⏳ 平均每次间隔时间：{avg_interval_hours}"
        )

        # 显示统计信息
        label = ctk.CTkLabel(self.stats_frame, text=stats_text, font=ctk.CTkFont("微软雅黑", 16), justify="left")
        label.pack(padx=20, pady=40)

        # 页面切换显示统计页，隐藏其它页
        self.page_input.pack_forget()
        self.page_logs.pack_forget()
        self.page_stats.pack(fill="both", expand=True)

    def display_log_text(self, text):
        """用于显示日志页的提示文本，比如文件不存在"""
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("0.0", ctk.END)
        self.log_textbox.insert(ctk.END, text)
        self.log_textbox.configure(state="disabled")
        # 显示日志页，隐藏其它页
        self.page_input.pack_forget()
        self.page_stats.pack_forget()
        self.page_logs.pack(fill="both", expand=True)

    def display_stats_text(self, text):
        """用于显示统计页的提示文本，比如文件不存在"""
        # 清空统计内容
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        label = ctk.CTkLabel(self.stats_frame, text=text, font=ctk.CTkFont("微软雅黑", 14), justify="left")
        label.pack(padx=20, pady=40)

    def show_input_page(self):
        """切换到输入页面"""
        self.page_logs.pack_forget()
        self.page_stats.pack_forget()
        self.page_input.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = LoggerApp()
    app.mainloop()
