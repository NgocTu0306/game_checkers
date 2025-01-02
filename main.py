import tkinter as tk
from checkers.rule  import show_rules_window
from PIL import Image, ImageTk
from playsound import playsound
from threading import Thread
from checkers.Game import Game
from checkers.constants import MAU_TRANG


def choose_game_mode():
    """Chọn chế độ chơi (người chơi vs người chơi hoặc người chơi vs AI)"""
    window = tk.Toplevel()
    #window.withdraw()  # Ẩn cửa sổ chính ngay khi mở
    window.title("Chọn chế độ chơi")
    window.geometry("600x400")

    # Tải ảnh nền
    background_image = Image.open("bg.jpg")  # Thay bằng đường dẫn ảnh
    background_image = background_image.resize((600, 400), Image.Resampling.LANCZOS)    
    background_photo = ImageTk.PhotoImage(background_image)

    # Giữ tham chiếu đến ảnh để tránh bị thu hồi
    window.background_photo = background_photo  # Lưu vào thuộc tính của cửa sổ

    # Canvas để chèn ảnh nền
    canvas = tk.Canvas(window, width=600, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")

    # Tiêu đề của cửa sổ
    canvas.create_text(300, 50, text="Chọn chế độ chơi", font=("Helvetica", 20, "bold"), fill="red")    

    # Hàm xử lý khi người chơi chọn chế độ
    def start_player_vs_player():
        window.destroy()
        create_game_window(ai_mode=False)  # Mở giao diện trò chơi với chế độ 2 người chơi

    def start_player_vs_ai():
        window.destroy()  # Đóng cửa sổ chọn chế độ
        choose_ai_difficulty(create_game_window)  # Mở giao diện chọn mức độ khó


    # Hàm hiệu ứng hover cho nút
    def on_enter(event, button, color):
        button.config(bg=color)

    def on_leave(event, button, color):
        button.config(bg=color)

    # Nút chọn chế độ chơi Người chơi vs Người chơi
    easy_button = tk.Button(window, text="Người chơi vs Người chơi", font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white", width=20, height=2,
                            command=start_player_vs_player)
    canvas.create_window(300, 150, window=easy_button)

    # Nút chọn chế độ chơi Người chơi vs AI
    medium_button = tk.Button(window, text="Người chơi vs AI", font=("Helvetica", 14, "bold"), bg="#FFA500", fg="white", width=20, height=2,
                              command=start_player_vs_ai)
    canvas.create_window(300, 250, window=medium_button)

    window.mainloop()

def on_choose_mode(parent_window,window=None):
    for widget in window.winfo_children():
        widget.deiconify()

    # Đảm bảo trò chơi được làm mới và quay lại trạng thái ban đầu
    window.deiconify()  # Đóng cửa sổ hiện tại

    # Nếu có cửa sổ cha (parent_window), hiển thị lại cửa sổ chính để người chơi chọn chế độ
    if parent_window:
        parent_window.destroy()  # Hiển thị lại cửa sổ chính

    # Tạo lại giao diện chính cho việc chọn chế độ chơi
    main()

def choose_ai_difficulty(create_game_window):
    """Chọn mức độ chơi khi đấu với AI"""
    difficulty_window = tk.Toplevel()  # Tạo cửa sổ phụ
    difficulty_window.title("Chọn mức độ khó")
    difficulty_window.geometry("600x400")

    # Thử tải ảnh nền
    try:
        background_image = Image.open("bg.jpg")
        background_image = background_image.resize((600, 400), Image.Resampling.LANCZOS)    
        background_photo = ImageTk.PhotoImage(background_image)
        difficulty_window.background_photo = background_photo  # Lưu tham chiếu ảnh
    except FileNotFoundError:
        print("Không tìm thấy ảnh nền! Sử dụng nền mặc định.")
        background_photo = None

    # Tạo canvas và ảnh nền
    canvas = tk.Canvas(difficulty_window, width=600, height=400)
    canvas.pack(fill="both", expand=True)
    if background_photo:
        canvas.create_image(0, 0, image=background_photo, anchor="nw")  # Đặt ảnh nền
    else:
        canvas.config(bg="white")  # Màu nền mặc định

    # Tiêu đề
    canvas.create_text(300, 50, text="Chọn mức độ khó", font=("Helvetica", 20, "bold"), fill="blue")   
    
    def start_game_with_difficulty(level):
        depth = 3  # Mặc định
        if level == "easy":
            depth = 3
        elif level == "medium":
            depth = 6 
        elif level == "hard":
            depth = 10 

        difficulty_window.destroy()  # Đóng cửa sổ chọn mức độ
        create_game_window(ai_mode=True, depth=depth)  # Mở giao diện trò chơi với AI

    # Hàm hiệu ứng hover cho nút
    def on_enter(event, button, hover_color):
        button.config(bg=hover_color)

    def on_leave(event, button, original_color):
        button.config(bg=original_color)

    # Tạo nút cho từng mức độ
    button_config = [
        ("Dễ", "#4CAF50", "#45BF60", "easy", 120),
        ("Vừa", "#FFA500", "#FFB347", "medium", 170),
        ("Khó", "#FF4500", "#FF6347", "hard", 220),
    ]

    for text, color, hover_color, level, y in button_config:
        button = tk.Button(
            difficulty_window, text=text, font=("Helvetica", 14, "bold"),
            bg=color, fg="white", width=5, height=1,
            command=lambda l=level: start_game_with_difficulty(l)
        )
        canvas.create_window(300, y, window=button)
        button.bind("<Enter>", lambda event, b=button, hc=hover_color: on_enter(event, b, hc))
        button.bind("<Leave>", lambda event, b=button, c=color: on_leave(event, b, c))
    difficulty_window.mainloop()

def create_game_window(ai_mode=False, depth=1):
    """Khởi tạo giao diện trò chơi"""
    window = tk.Tk()
    window.title("Cờ Đam")
    window.geometry("600x600")
    
    tk.Label(window, text="Chơi Cờ Đam", font=("Helvetica", 20, "bold"), bg="#EDEDED").pack(pady=20)
    # Khởi tạo trò chơi
    game = Game(window, ai_mode,depth)
    game.start_game()
    back_button = tk.Button(window, text="Chơi lại", font=("Helvetica", 14, "bold"),
                            bg="#FF4500", fg="white", width=20, height=2, command=lambda: reset_game(window))
    back_button.pack(pady=10)    
    if ai_mode:
        game.ai_move()  # AI thực hiện nước đi đầu tiên nếu cần

    window.mainloop()
def show_winner(self, winner):
    result_window = tk.Toplevel(self.window)
    result_window.title("Kết quả trận đấu")
    result_window.geometry("300x200")
    result_window.config(bg="#D3D3D3")
    if winner == MAU_TRANG:
        winner_text = "Quân trắng thắng!"
    else:
        winner_text = "Quân đen thắng!"

        tk.Label(result_window, text=winner_text, font=("Arial", 16, "bold"),
                 fg="green", bg="#D3D3D3").pack(pady=20)
        
        tk.Button(result_window, text="Thoát", command=result_window.destroy,
                  font=("Arial", 14), bg="#FF4500", fg="white").pack(pady=10)

def reset_game(window, parent_window=None):
    """Hàm reset trò chơi, quay lại giao diện chính."""
    # Xóa tất cả các widget hiện tại trong cửa sổ trò chơi
    for widget in window.winfo_children():
        widget.destroy()

    # Đảm bảo trò chơi được làm mới và quay lại trạng thái ban đầu
    window.destroy()  # Đóng cửa sổ hiện tại

    # Nếu có cửa sổ cha (parent_window), hiển thị lại cửa sổ chính để người chơi chọn chế độ
    if parent_window:
        parent_window.deiconify()  # Hiển thị lại cửa sổ chính

    # Tạo lại giao diện chính cho việc chọn chế độ chơi
    choose_game_mode()  # Gọi hàm để quay lại giao diện chọn chế độ chơi

def play_background_music():
    """Phát nhạc nền liên tục."""
    try:
        while True:  # Lặp vô hạn để phát nhạc liên tục
            playsound("music_bg.mp3")  
    except:
        pass  # Dừng phát nhạc nếu có lỗi

def start_music_thread():
    """Khởi động luồng phát nhạc nền."""
    music_thread = Thread(target=play_background_music, daemon=True)
    music_thread.start()


def main():
    """Khởi tạo giao diện trò chơi"""
    window = tk.Tk()
    window.title("Cờ Đam")
    
    background_image = Image.open("bg.jpg")  
    background_image = background_image.resize((600, 400), Image.Resampling.LANCZOS)    
    background_photo = ImageTk.PhotoImage(background_image)
    # Giữ tham chiếu đến ảnh
    window.background_photo = background_photo  # Lưu vào thuộc tính của cửa sổ

    canvas = tk.Canvas(window, width=600, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")  # Đặt ảnh nền

    # Nút để xem luật chơi
    rules_button = tk.Button(window, text="Luật Chơi", font=("Helvetica", 14), bg="#4CAF50", fg="white",
                              command=lambda: show_rules_window("luatchoi.txt"))
    rules_button.pack(pady=20)
    canvas.create_window(300, 100, window=rules_button)

    # Nút chọn chế độ chơi
    choose_button = tk.Button(window, text = "Chế độ chơi", font=("Helvetica", 14), bg="#FF69B4", fg="white", command=lambda:choose_game_mode())
    choose_button.pack(pady=20)
    canvas.create_window(300, 170, window=choose_button)

    # Nút thoát
    exit_button = tk.Button(window, text="Thoát", font=("Helvetica", 14), bg="#FF4500", fg="white", command=window.destroy)
    exit_button.pack(pady=20)
    canvas.create_window(300, 240, window=exit_button)

    start_music_thread()
    window.mainloop()

main()