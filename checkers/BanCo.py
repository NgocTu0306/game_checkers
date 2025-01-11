import tkinter as tk
# Các hằng số
MAU_TRANG = "white"
MAU_DEN = "black"
SO_HANG = 8
SO_COT = 8
KICH_THUOC_O = 60
# Initial values of Alpha and Beta
MAX, MIN = 1000, -1000
# Màu sắc
MAU_SANG_BAN_CO = "wheat" # Màu sáng mới
MAU_TOI_BAN_CO = "saddlebrown"  # Màu tối mới

# Thời gian giới hạn cho mỗi người chơi (giây)
THOI_GIAN_LUOT = 60  # 60 giây cho mỗi lượt
class QuanCo:
    def __init__(self, hang, cot, mau):
        self.hang = hang
        self.cot = cot
        self.mau = mau
        self.vua = False
        if self.mau == MAU_TRANG:
            self.huong = [(1, -1), (1, 1)]  # Quân trắng đi xuống (di chuyển theo đường chéo)
        else:
            self.huong = [(-1, -1), (-1, 1)]  # Quân đen đi lên (di chuyển theo đường chéo)

    def taoVua(self):
        self.vua = True
        self.huong = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Vua có thể đi cả 4 hướng

    def layViTri(self):
        return (self.cot * KICH_THUOC_O + KICH_THUOC_O // 2, self.hang * KICH_THUOC_O + KICH_THUOC_O // 2)

    def veQuanCo(self, canvas):
        xTrungTam, yTrungTam = self.layViTri()
        banKinhQuanCo = KICH_THUOC_O // 3 # Quân cờ có bán kính =1/3 KICH_THUOC_O
        if self.vua:
            canvas.create_oval(xTrungTam - banKinhQuanCo, yTrungTam - banKinhQuanCo,
                               xTrungTam + banKinhQuanCo, yTrungTam + banKinhQuanCo,
                               fill=self.mau, outline="yellow", width=3)  # Highlight quân vua với viền vàng
        else:
            canvas.create_oval(xTrungTam - banKinhQuanCo, yTrungTam - banKinhQuanCo,
                               xTrungTam + banKinhQuanCo, yTrungTam + banKinhQuanCo,
                               fill=self.mau)

    def position(self):
        """Thuộc tính trả về vị trí của quân cờ."""
        return (self.hang, self.cot)
    
    def is_regular_piece(self):
            """
            Kiểm tra xem quân cờ có phải là quân cờ thường không.
            Quân cờ thường là quân cờ chưa thăng chức thành vua.
            """
            return not self.taoVua()
    
    #Lấy thông tin quân cờ đưới dạng chuỗi
    def __repr__(self):
        return f"Quân ({self.hang}, {self.cot}, {self.mau})"
    
class BanCo:
    def __init__(self, game):
        self.banCo = [] #Danh sách 2 chiều lưu trữ trạng thái của các ô trên bàn cờ
        self.khoiTaoBanCo()
        self.game = game #Giúp cho biết trạng thái của trò chơi
    
    def khoiTaoBanCo(self):
        #Lặp qua từng hàng
        for hang in range(SO_HANG):
            hangList = [] #Danh sách để lưu các ô trong hàng hiện tại
            #Lặp qua từng cột
            for cot in range(SO_COT):
                #Quân trắng đặt ở 3 hàng đầu tiên và chỉ số cột lẻ
                if hang < 3 and (hang + cot) % 2 != 0:
                    hangList.append(QuanCo(hang, cot, MAU_TRANG))  # Quân trắng ở 3 hàng đầu
                #Quân đen đặt ở 3 hàng cuối cùng
                elif hang >= SO_HANG - 3 and (hang + cot) % 2 != 0:
                    hangList.append(QuanCo(hang, cot, MAU_DEN))  # Quân đen ở 3 hàng cuối
                #Các ô còn lại không chứa quân cờ
                else:
                    hangList.append(None)  # Các ô trống
            # hangList sẽ được thêm vào danh sách banCo và tạo thành bàn cờ hoành chỉnh
            self.banCo.append(hangList)
    
    def get_piece(self, hang, cot):
        """Trả về quân cờ tại vị trí (hang, cot)."""
        if 0 <= hang < SO_HANG and 0 <= cot < SO_COT:
            return self.banCo[hang][cot]
        return None
   
    def veBanCo(self, canvas):
        # Vẽ bàn cờ
        for hang in range(SO_HANG):
            for cot in range(SO_COT):
                #Nếu tổng của (hang+cot) là số chẵn
                color = MAU_SANG_BAN_CO if (hang + cot) % 2 == 0 else MAU_TOI_BAN_CO
                #Vẽ ô thành hình chữ nhật
                canvas.create_rectangle(cot * KICH_THUOC_O, hang * KICH_THUOC_O,
                                        (cot + 1) * KICH_THUOC_O, (hang + 1) * KICH_THUOC_O,
                                        fill=color, outline="black")
        
        # Vẽ quân cờ
        for hang in range(SO_HANG):
            for cot in range(SO_COT):
                quan = self.banCo[hang][cot]
                #Nếu ô có quan (quân cờ)
                if quan is not None:
                    #Vẽ cờ lên bàn cờ
                    quan.veQuanCo(canvas)
         
    
    def set_piece(self, hang, cot, piece):
        """Đặt quân cờ tại vị trí chỉ định."""
        if 0 <= hang < 8 and 0 <= cot < 8:
            self.banCo[hang][cot] = piece

    def remove_piece(self, hang, cot):
        """Xóa quân cờ tại vị trí cũ."""
        self.banCo[hang][cot] = None

     
    def kiemTraThang(self):
        #Khởi tạo biến khi không còn quân cờ trên bàn cờ
        quan_trang = quan_den = False
        for hang in range(SO_HANG):
            for cot in range(SO_COT):
                #Lấy quan tại vị trí hang,cot trên bàn cờ
                quan = self.banCo[hang][cot]
                #Nếu ô đó có quân
                if quan is not None:
                    if quan.mau == MAU_TRANG:
                        quan_trang = True
                    elif quan.mau == MAU_DEN:
                        quan_den = True
        #Nếu ko còn quân trắng trên bàn cờ
        if not quan_trang:
            return MAU_DEN  # Quân đen thắng
        #Nếu ko còn quân đen trên bàn cờ
        if not quan_den:
            return MAU_TRANG  # Quân trắng thắng
        return None  # Ván chơi chưa kết thúc

class Game:
    def __init__(self):
        # Khởi tạo bất kỳ dữ liệu nào cho game ở đây
        self.state = "game_running"


if __name__ == "__main__":
    # Tạo đối tượng game
    game = Game()
    # Khởi tạo bàn cờ với đối tượng game
    ban_co = BanCo(game)
    # Khởi tạo cửa sổ Tkinter
    root = tk.Tk()
    root.title("Game Cờ Dame")
    # Tạo Canvas để vẽ bàn cờ
    canvas = tk.Canvas(root, width=SO_COT * KICH_THUOC_O, height=SO_HANG * KICH_THUOC_O)
    canvas.pack()
    # Vẽ bàn cờ
    ban_co.veBanCo(canvas)
    # Chạy vòng lặp sự kiện Tkinter
    root.mainloop()


