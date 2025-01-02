from checkers.constants import KICH_THUOC_O, MAU_TRANG, SO_HANG, SO_COT

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
    def getValidMoves(self):
        """Tính các nước đi hợp lệ của quân cờ"""
        moves = [] #Khởi tạo danh sách để lưu các nước đi hợp lệ
        directions = [(-1, -1), (-1, 1)] if self.mau == MAU_TRANG else [(1, -1), (1, 1)]
        # Lặp qua tất cả các hướng di chuyển
        for d in directions:
            new_row = self.hang + d[0] #Tính vị trí mới của quân cờ thay đổi về hàng
            new_col = self.cot + d[1] #Tính vị trí mới của quân cờ thay đổi về cột
            # Kiểm tra vị trí mới có nằm trong phạm vi bàn cờ hay không
            if 0 <= new_row < SO_HANG and 0 <= new_col < SO_COT:
                moves.append((new_row, new_col))
        return moves
    
    def is_regular_piece(self):
            """
            Kiểm tra xem quân cờ có phải là quân cờ thường không.
            Quân cờ thường là quân cờ chưa thăng chức thành vua.
            """
            return not self.taoVua()
    
    #Lấy thông tin quân cờ đưới dạng chuỗi
    def __repr__(self):
        return f"Quân ({self.hang}, {self.cot}, {self.mau})"
    
