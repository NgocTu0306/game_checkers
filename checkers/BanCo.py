from .QuanCo import*
from .constants import MAU_SANG_BAN_CO, MAU_TOI_BAN_CO, SO_HANG, SO_COT

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
   

