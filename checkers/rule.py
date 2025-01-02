import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Hàm để đọc nội dung từ file luật chơi
def read_rules_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file luật chơi!")
        return ""
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")
        return ""

# Hàm hiển thị giao diện luật chơi
def show_rules_window(file_path):
    rules_content = read_rules_from_file(file_path)
    if not rules_content:
        return  # Nếu file rỗng hoặc lỗi, không hiển thị gì

    # Tạo cửa sổ mới để hiển thị luật chơi
    rules_window = tk.Toplevel()
    rules_window.title("Luật Chơi")
    rules_window.geometry("600x430")

    # Tải ảnh nền
    try:
        background_image = Image.open("bg.jpg")  # Thay bằng đường dẫn ảnh nếu cần
        background_image = background_image.resize((600, 430), Image.Resampling.LANCZOS)
        background_photo = ImageTk.PhotoImage(background_image)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tải ảnh nền: {e}")
        return

    # Giữ tham chiếu đến ảnh để tránh bị thu hồi
    rules_window.background_photo = background_photo  # Lưu vào thuộc tính của cửa sổ

    # Canvas để chèn ảnh nền
    canvas = tk.Canvas(rules_window, width=600, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")

    # Tiêu đề của cửa sổ
    canvas.create_text(300, 50, text="Luật chơi", font=("Helvetica", 20, "bold"), fill="red")    
    # Hiển thị nội dung luật chơi lên Canvas
    canvas.create_text(
        300, 70,  # Vị trí bắt đầu (giữa canvas)
        text=rules_content,
        font=("Helvetica", 12, "bold"),
        fill="black",  # Màu chữ
        width=500,  # Giới hạn chiều rộng nội dung
        anchor="n"  # Căn giữa theo chiều ngang
    )

    # Nút đóng cửa sổ
    close_button = tk.Button(rules_window, text="Đóng", command=rules_window.destroy, font=("Helvetica", 12))
    canvas.create_window(300, 400, window=close_button, width=100, height=30)


# Tạo cửa sổ chính của Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ chính, nếu không muốn hiển thị cửa sổ chính

    # Gọi hàm để hiển thị cửa sổ luật chơi
    show_rules_window("luatchoi.txt")
    # Bắt đầu vòng lặp chính của Tkinter
    root.mainloop()
