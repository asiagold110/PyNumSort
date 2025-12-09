import tkinter as tk
from tkinter import messagebox

class NumberSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("مرتب‌کننده اعداد")
        self.root.geometry("500x320")
        self.root.resizable(False, False)

        # تنظیم فونت برای پشتیبانی بهتر از زبان فارسی
        self.font_style = ("Tahoma", 11)

        # ایجاد ویجت‌ها
        self.create_widgets()

    def create_widgets(self):
        # فریم اصلی برای چیدمان بهتر
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # برچسب و فیلد ورودی
        input_label = tk.Label(main_frame, text="اعداد را وارد کنید (با - یا فاصله یا کاما جدا کنید):", font=self.font_style)
        input_label.pack(pady=(0, 5), anchor="w")

        self.input_entry = tk.Entry(main_frame, width=60, font=self.font_style)
        self.input_entry.pack(pady=(0, 15), fill="x")
        self.input_entry.focus()

        # --- اتصال میانبرهای صفحه کلید به باکس ورودی ---
        self.input_entry.bind('<Control-c>', self.copy_input)
        self.input_entry.bind('<Control-v>', self.paste_input)
        self.input_entry.bind('<Control-x>', self.cut_input)

        # فریم برای دکمه‌ها
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10, fill="x")

        sort_button = tk.Button(button_frame, text="مرتب کن", command=self.sort_numbers, font=self.font_style, bg="#4CAF50", fg="white")
        sort_button.pack(side="left", padx=(0, 10))

        clear_button = tk.Button(button_frame, text="پاک کردن", command=self.clear_fields, font=self.font_style)
        clear_button.pack(side="left")

        # برچسب و فیلد خروجی
        output_label = tk.Label(main_frame, text="نتیجه:", font=self.font_style)
        output_label.pack(pady=(15, 5), anchor="w")

        self.output_entry = tk.Entry(main_frame, width=60, font=self.font_style, state="readonly")
        self.output_entry.pack(pady=(0, 5), fill="x")

        # --- اتصال میانبر کپی به باکس خروجی ---
        self.output_entry.bind('<Control-c>', self.copy_output)

        # برچسب جدید برای نمایش تعداد اعداد
        self.count_label = tk.Label(main_frame, text="", font=("Tahoma", 10, "bold"), fg="blue")
        self.count_label.pack(pady=(0, 10))

        # دکمه کپی کردن
        copy_button = tk.Button(main_frame, text="کپی کردن نتیجه", command=self.copy_result, font=self.font_style, bg="#2196F3", fg="white")
        copy_button.pack(pady=5)

        # برچسب وضعیت
        self.status_label = tk.Label(main_frame, text="", font=("Tahoma", 9), fg="green")
        self.status_label.pack(pady=5)

    # --- توابع جدید برای مدیریت میانبرها ---
    def copy_input(self, event):
        self.input_entry.event_generate("<<Copy>>")
        return "break" # جلوگیری از اجرای دوباره رویداد پیش‌فرض

    def paste_input(self, event):
        try:
            text = self.root.clipboard_get()
            self.input_entry.insert(tk.INSERT, text)
        except tk.TclError:
            pass # در صورت خالی بودن کلیپ‌بورد اتفاقی نمی‌افتد
        return "break"

    def cut_input(self, event):
        self.input_entry.event_generate("<<Cut>>")
        return "break"

    def copy_output(self, event):
        # ابتدا کل متن را انتخاب کرده، سپس کپی می‌کنیم
        self.output_entry.config(state="normal")
        self.output_entry.select_range(0, tk.END)
        self.output_entry.event_generate("<<Copy>>")
        self.output_entry.config(state="readonly")
        self.output_entry.select_clear() # از حالت انتخاب خارج می‌کنیم
        return "break"

    def sort_numbers(self):
        """اعداد ورودی را گرفته، مرتب کرده و در فیلد خروجی نمایش می‌دهد."""
        input_text = self.input_entry.get()
        if not input_text.strip():
            messagebox.showwarning("ورودی خالی", "لطفاً ابتدا عددی وارد کنید.")
            return

        parts = input_text.replace('-', ' ').replace(',', ' ').split()
        
        numbers = []
        try:
            for part in parts:
                numbers.append(int(part))
        except ValueError:
            messagebox.showerror("خطا", "ورودی نامعتبر است. لطفاً فقط از اعداد و جداکننده‌های معتبر استفاده کنید.")
            return

        numbers.sort()
        
        # به‌روزرسانی برچسب تعداد اعداد
        count = len(numbers)
        self.count_label.config(text=f"{count} عدد")

        sorted_string = "-".join(map(str, numbers))
        
        self.output_entry.config(state="normal")
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, sorted_string)
        self.output_entry.config(state="readonly")

    def clear_fields(self):
        """فیلد‌های ورودی و خروجی را پاک می‌کند."""
        self.input_entry.delete(0, tk.END)
        self.output_entry.config(state="normal")
        self.output_entry.delete(0, tk.END)
        self.output_entry.config(state="readonly")
        # پاک کردن برچسب تعداد اعداد
        self.count_label.config(text="")
        self.status_label.config(text="")
        self.input_entry.focus()

    def copy_result(self):
        """نتیجه را در کلیپ‌بورد کپی می‌کند."""
        result = self.output_entry.get()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.status_label.config(text="نتیجه با موفقیت کپی شد!")
            self.root.after(2000, lambda: self.status_label.config(text=""))
        else:
            messagebox.showinfo("اطلاعات", "نتیجه‌ای برای کپی کردن وجود ندارد.")

# اجرای برنامه
if __name__ == "__main__":
    root = tk.Tk()
    app = NumberSorterApp(root)
    root.mainloop()