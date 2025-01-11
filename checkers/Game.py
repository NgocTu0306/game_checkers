import tkinter as tk
from tkinter import messagebox
import math
import sys
sys.path.append('checkers')
from BanCo import *

class Game:
    def __init__(self, window, ai_mode=False, depth=1):
        self.window = window
        self.board = BanCo(self)
        self.turn = MAU_DEN  # Quân đen đi trước
        self.selected = None
        self.validMoves = set()
        self.winner = None
        self.ai_mode = ai_mode
        self.depth = depth
        self.history = [] 
        self.current_player_piece = None
        self.current_opponent_piece = None
        self.update_current_pieces()

        # Thời gian đếm ngược cho mỗi lượt
        self.time_left = THOI_GIAN_LUOT
        self.timer_running = False
        self.time_label = None  # Nhãn hiển thị thời gian
        self.timer_id = None

        # Khung chứa thông tin hiển thị (thời gian, lượt chơi, điểm)
        self.info_frame = tk.Frame(self.window, bg="#EDEDED")
        self.info_frame.pack(side="top", fill="x", pady=5)

        # Nhãn hiển thị thời gian
        self.time_label = tk.Label(self.info_frame, text=f"Thời gian: {self.time_left} giây",
                                   font=("Helvetica", 14), bg="#EDEDED", fg="red")
        self.time_label.pack(anchor="center", pady=5)

        # Nhãn hiển thị lượt chơi
        self.turn_label = tk.Label(self.info_frame, text="Lượt chơi: Quân đen", font=("Helvetica", 14, "bold"),
                                   bg="#EDEDED")
        self.turn_label.pack(anchor="center", pady=10)

        # Nhãn hiển thị điểm quân trắng và quân đen
        self.score_trang_label = tk.Label(self.info_frame, text="Quân trắng: 0", font=("Helvetica", 14), bg="#EDEDED")
        self.score_trang_label.pack(side="left", padx=200)

        self.score_den_label = tk.Label(self.info_frame, text="Quân đen: 0", font=("Helvetica", 14), bg="#EDEDED")
        self.score_den_label.pack(side="right", padx=200)
        # Cập nhật thời gian lượt chơi
        self.start_timer()
        # Cập nhật điểm ngay khi bắt đầu trò chơi
        self.update_score()


    def update_current_pieces(self):
        """Cập nhật quân cờ hiện tại và đối thủ."""
        if self.turn == MAU_DEN:
            self.current_player_piece = MAU_DEN  # Giả sử hàm này trả về quân đen
            self.current_opponent_piece = MAU_TRANG   # Giả sử hàm này trả về quân trắng
        else:
            self.current_player_piece =  MAU_TRANG 
            self.current_opponent_piece = MAU_DEN   # Quân đen

    def update_score(self):
        """Đếm số lượng quân cờ và cập nhật điểm"""
        white_count = 0
        black_count = 0

        # Đếm quân trắng và quân đen trên bàn cờ
        for row in self.board.banCo:
            for piece in row:
                if piece is not None:
                    if piece.mau == MAU_TRANG:
                        white_count += 1
                    elif piece.mau == MAU_DEN:
                        black_count += 1
        
        # Cập nhật điểm vào các Label
        self.score_trang_label.config(text=f"Quân trắng: {white_count}")
        self.score_den_label.config(text=f"Quân đen: {black_count}")

    def start_timer(self):
        """Khởi động đồng hồ đếm ngược khi bắt đầu lượt mới."""
        #Đối tượng self có thuộc tính timer_id
        #Kiểm tra sự tồn tại của timer_id
        if hasattr(self, 'timer_id') and self.timer_id:
            # Hủy sự kiện 'after' cũ nếu có
            self.window.after_cancel(self.timer_id)  
        
        self.time_left = THOI_GIAN_LUOT  # Đặt lại thời gian
        self.timer_running = True
        self.game_over =False
        self.update_timer()

    def update_timer(self):
        """Cập nhật nhãn hiển thị thời gian mỗi giây."""
        #Kiểm tra xem đồng hồ đếm ngược có đang chạy hay không
        #Nếu không chạy
        if not self.timer_running:
            return  #Sẽ dừng update_timer
        # Cập nhật nội dung nhãn
        # Nếu đồng hồ đang chạy, sẽ tiếp tục chạy và tạo label
        self.time_label.config(text=f"Thời gian: {self.time_left} giây")

        # Nếu thời gian còn lại >0
        if self.time_left > 0:
            # Thời gian sẽ giảm dần
            self.time_left -= 1
            # Gọi lại update_timer sau 1s=1000mls
            self.timer_id = self.window.after(1000, self.update_timer)  # Gọi lại sau 1 giây
        else:
            # Nếu thời gian hết
            self.timer_running = True
            # Gọi
            self.end_turn_due_to_timeout()

    def end_turn_due_to_timeout(self):
        """Xử lý khi hết thời gian lượt chơi."""
        # Hủy tất cả các sự kiện 'after' liên quan đến thời gian
        if hasattr(self, 'timer_event') and self.timer_id:
            self.window.after_cancel(self.timer_id)
        # Đặt trạng thái trò chơi là kết thúc
        self.game_over = True
        # Kiểm tra trạng thái trò chơi
        # Kiểm tra thuộc tính winner _ Nếu thắng trả về winner _ Nếu không thì trả về None
        if getattr(self, 'winner', None) is not None:  # Nếu trò chơi đã kết thúc
            return
        if self.turn == MAU_DEN:
            messagebox.showinfo("Hết thời gian", "Quân đen hết thời gian! Quân trắng thắng!")
            self.winner = MAU_TRANG
        else:
            messagebox.showinfo("Hết thời gian", "Quân trắng hết thời gian! Quân đen thắng!")
            self.winner = MAU_DEN

        self.show_winner(self.winner)


    
    def makeMove(self, ai_piece, best_move):
        """Di chuyển quân cờ từ vị trí hiện tại sang vị trí mới."""
    
        # Kiểm tra xem ai_piece có phải là một đối tượng có thuộc tính hang và cot không
        if ai_piece is None or not hasattr(ai_piece, 'hang') or not hasattr(ai_piece, 'cot'):
            print("Không có quân cờ để di chuyển!")
            return 
    
        if best_move is None:
            print("Không có nước đi hợp lệ!")
            return
    
        # Lấy vị trí hiện tại của quân cờ
        current_row, current_col = ai_piece.hang, ai_piece.cot
        # Định nghĩa tọa độ đích (target_row, target_col)
        target_row, target_col = best_move  
    
        # Kiểm tra nếu quân cờ có thể di chuyển đến vị trí hợp lệ không
        if not self.is_valid_move(best_move):
            print("Nước đi không hợp lệ!")
            return
    
        # Kiểm tra nếu nước đi này có phải là một bước nhảy (quân cờ ăn quân đối phương)
        if abs(current_row - target_row) > 1 or abs(current_col - target_col) > 1:
            # Nếu là bước nhảy, kiểm tra ăn quân đối phương
            print(f"Đang xử lý nước đi ăn quân đối phương từ ({current_row}, {current_col}) đến ({target_row}, {target_col})")
        
            # Gọi hàm move_piece để xử lý ăn quân
            if not self.move_piece(current_row, current_col, target_row, target_col):
                print("Nước đi không hợp lệ: Không có quân đối phương để ăn!")
                return  # Nếu không thể ăn quân đối phương, không thực hiện nước đi
    
        else:
            # Nếu không phải là bước nhảy (chỉ di chuyển quân cờ đơn giản)
            #print(f"Di chuyển quân cờ từ ({current_row}, {current_col}) đến ({target_row}, {target_col})")
        
            # Cập nhật bảng cờ: Di chuyển quân cờ
            self.board.set_piece(target_row, target_col, ai_piece)  # Đặt quân cờ tại vị trí mới
            self.board.set_piece(current_row, current_col, None)  # Xóa quân cờ tại vị trí cũ
        
            # Cập nhật lại tọa độ của quân cờ
            ai_piece.hang = target_row
            ai_piece.cot = target_col
        self.history.append({
            'piece': ai_piece,
            'from': (current_row, current_col),
            'to': (target_row, target_col)
        })
        # Cập nhật phong vua nếu có
        self.phongVua(ai_piece)
    
        # Đổi lượt người chơi
        self.changeTurn()

        print(f"Quân cờ {ai_piece.mau} di chuyển từ ({current_row}, {current_col}) đến ({target_row}, {target_col})")

    def is_valid_move(self, move):
        """Kiểm tra nếu nước đi là hợp lệ. Đảm bảo tọa độ nằm trong phạm vi bàn cờ. Cho phép ô đích trống hoặc có quân đối thủ."""
        if not isinstance(move, (tuple, list)) or len(move) != 2:
            return False
        row, col = move
        # Kiểm tra nếu tọa độ là số nguyên
        if not isinstance(row, int) or not isinstance(col, int):
            return False

        # Kiểm tra nếu tọa độ nằm trong phạm vi bàn cờ
        if not (0 <= row < len(self.board.banCo) and 0 <= col < len(self.board.banCo[0])):
            return False

        # Lấy quân cờ tại ô đích
        target_piece = self.board.get_piece(row, col)

        # Kiểm tra ô đích
        if target_piece is None:  # Ô trống
            return True
        elif target_piece.mau != self.turn:  # Quân đối thủ
            return True
        else:
            #print(f"Nước đi không hợp lệ: Vị trí ({row}, {col}) chứa quân cùng màu!")
            return False
        
  
    def ai_move(self):
        """AI thực hiện nước đi tối ưu sử dụng thuật toán Minimax."""
        if self.turn == MAU_TRANG:  # Nếu là lượt của quân trắng (AI)
            # Lấy tất cả quân cờ của AI (quân trắng)
            ai_pieces = [piece for row in self.board.banCo for piece in row if isinstance(piece, QuanCo) and piece.mau == MAU_TRANG]

            if not ai_pieces:
                print("Không tìm thấy quân cờ AI!")
                return None  # Trả về None nếu không có quân cờ hợp lệ

            # Danh sách các nước đi hợp lệ
            valid_moves = []

            for ai_piece in ai_pieces:
                piece_moves = self.getValidMoves(ai_piece)
                valid_moves.extend(piece_moves)  # Thêm các nước đi hợp lệ của quân cờ vào danh sách

            # Nếu không có nước đi hợp lệ, thông báo và dừng
            if not valid_moves:
                print("Không có nước đi hợp lệ!")
                return None  # Trả về None nếu không có nước đi hợp lệ

            # Sử dụng thuật toán Minimax để tìm nước đi tối ưu
            print(f"Giá trị của self.depth: {self.depth}")
            alpha = -math.inf
            beta = math.inf

            # Lấy nước đi tốt nhất từ Minimax
            _, best_move = self.minimax(valid_moves, self.depth, alpha, beta, maximizingPlayer=True)

            if best_move is None:
                print("Không thể di chuyển đến bất kỳ nước đi hợp lệ nào.")
                return None  # Nếu không tìm thấy nước đi hợp lệ

            # Tìm quân cờ và thực hiện di chuyển
            ai_piece_to_move = None
            for ai_piece in ai_pieces:
                # Kiểm tra xem quân cờ có thể di chuyển đến best_move không
                if best_move in self.getValidMoves(ai_piece):
                    ai_piece_to_move = ai_piece
                    break  # Dừng lại khi tìm thấy quân cờ có thể di chuyển đến best_move

            if ai_piece_to_move is not None:
                print(f"{ai_piece_to_move} sẽ di chuyển đến {best_move}")
                self.makeMove(ai_piece_to_move, best_move)# Thực hiện di chuyển
            else:
                print("Không có quân cờ để di chuyển!")

            # Trả về nước đi tốt nhất
            print(f"Nước đi của AI: {best_move}")
            return best_move

    def minimax(self, valid_moves, depth, alpha, beta, maximizingPlayer):
        """
        Minimax với Alpha-Beta Pruning, ưu tiên ăn quân đối thủ.
        """
        # Điều kiện dừng: Nếu đạt được độ sâu tối đa hoặc không còn nước đi hợp lệ
        if depth == 0 or not valid_moves:
            score_trang, score_den, _ = self.evaluateBoard()  # Lấy điểm của quân trắng và quân đen
            return score_trang - score_den if maximizingPlayer else score_den - score_trang, None

        best_move = None

        if maximizingPlayer:  # AI đang chơi
            maxEval = -math.inf
            for move in valid_moves:
                # Kiểm tra xem nước đi này có ăn quân đối thủ không
                if self.isCaptureMove(move):
                    evaluation = self.evaluateMove(move) + 10  # Ưu tiên nước ăn quân
                else:
                    evaluation = self.evaluateMove(move)

                # Tạo nước đi giả lập (giả sử quân cờ đã di chuyển)
                self.makeMove(self.current_player_piece, move)

                # Đệ quy: Gọi minimax cho đối thủ (minimizingPlayer)
                valid_moves_for_opponent = self.getValidMoves(self.current_opponent_piece)  # Truyền đối thủ vào
                opponent_eval, _ = self.minimax(valid_moves_for_opponent, depth - 1, alpha, beta, False)

                # Hoàn tác nước đi
                # Cập nhật alpha-beta pruning
                evaluation -= opponent_eval  # Cộng thêm phần điểm của đối thủ
                if evaluation > maxEval:
                    maxEval = evaluation
                    best_move = move

                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break  # Cắt tỉa (pruning)

            return maxEval, best_move

        else:  # Đối thủ đang chơi
            minEval = math.inf
            for move in valid_moves:
                # Kiểm tra xem nước đi này có ăn quân đối thủ không
                if self.isCaptureMove(move):
                    evaluation = self.evaluateMove(move) + 10  # Ưu tiên nước ăn quân
                else:
                    evaluation = self.evaluateMove(move)

                # Tạo nước đi giả lập (giả sử quân cờ đã di chuyển)
                self.makeMove(self.current_opponent_piece, move)

                # Đệ quy: Gọi minimax cho AI (maximizingPlayer)
                valid_moves_for_ai = self.getValidMoves(self.current_player_piece)  # Truyền AI vào
                ai_eval, _ = self.minimax(valid_moves_for_ai, depth - 1, alpha, beta, True)

                # Cập nhật alpha-beta pruning
                evaluation += ai_eval  # Cộng thêm phần điểm của AI
                if evaluation < minEval:
                    minEval = evaluation
                    best_move = move

                beta = min(beta, evaluation)
                if beta <= alpha:
                    break  # Cắt tỉa (pruning)

            return best_move


    def getCaptureMoves(self, ai_piece):
        """Tìm các nước đi mà quân cờ ai_piece có thể ăn quân đối thủ."""
        capture_moves = []
        directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]  # Các hướng có thể ăn quân đối thủ (di chuyển 2 ô theo chiều chéo)
    
        for dx, dy in directions:
            new_row = ai_piece.hang + dx
            new_col = ai_piece.cot + dy
            mid_row = ai_piece.hang + dx // 2  # Ô giữa (quân đối thủ bị ăn)
            mid_col = ai_piece.cot + dy // 2
        
            # Kiểm tra nếu vị trí di chuyển hợp lệ
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                # Kiểm tra nếu quân đối thủ ở ô giữa và ô đích trống
                if self.board.banCo[mid_row][mid_col] is not None and self.board.banCo[mid_row][mid_col].mau != ai_piece.mau:
                    if self.board.banCo[new_row][new_col] is None:
                        capture_moves.append((ai_piece, (new_row, new_col)))  # Thêm nước đi ăn quân đối thủ vào danh sách
        return capture_moves
    

    def getMoveCloserToOpponent(self, ai_piece):
        """Tìm các nước đi mà quân phong vua có thể tiến lại gần quân đối thủ."""
        move_closer_moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Các hướng di chuyển chéo (lên trái, lên phải, xuống trái, xuống phải)

        for dx, dy in directions:
            new_row = ai_piece.hang + dx
            new_col = ai_piece.cot + dy
        
            # Kiểm tra nếu vị trí di chuyển hợp lệ và ô đó trống
            if 0 <= new_row < 8 and 0 <= new_col < 8 and self.board.banCo[new_row][new_col] is None:
                move_closer_moves.append((ai_piece, (new_row, new_col)))  # Thêm nước đi di chuyển tiến lại gần đối thủ vào danh sách

        return move_closer_moves

    
    def getKingMoves(self, ai_piece):
        """Lấy tất cả các nước đi hợp lệ cho quân phong vua."""
        king_moves = []
        # Giả sử quân phong vua có thể di chuyển bất kỳ nơi nào trong các ô chéo
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Di chuyển theo các hướng chéo
    
        for direction in directions:
            row, col = ai_piece.hang, ai_piece.cot
            while True:
                row += direction[0]
                col += direction[1]
                if 0 <= row < 8 and 0 <= col < 8:  # Kiểm tra nếu vị trí trong bàn cờ
                    target_piece = self.board.get_piece(row, col)
                    if target_piece is None:  # Vị trí trống
                        king_moves.append((row, col))
                    elif target_piece.mau != ai_piece.mau:  # Nếu là quân đối thủ
                        king_moves.append((row, col))  # Có thể ăn quân đối thủ
                        break  # Dừng lại khi ăn quân đối phương
                    else:
                        break  # Nếu gặp quân của mình, dừng lại
                else:
                    break  # Ra ngoài bàn cờ, dừng lại
    
        return king_moves
    

    def evaluateBoard(self):
        """
        Đánh giá bàn cờ và đưa ra nước đi ưu tiên:
        1. Ưu tiên ăn sạch quân đối thủ.
        2. Ưu tiên ăn quân trước mặt.
        3. Tiến lại gần đối thủ.
        4. Phong vua (đưa quân thường đến hàng cuối).
        5. Sử dụng vua để tiến lại gần và chuẩn bị ăn đối thủ.
        """
        score_trang = 0
        score_den = 0
        best_move = None

        # 1. Ưu tiên ăn sạch quân đối thủ
        for row_idx, row in enumerate(self.board.banCo):
            for col_idx, piece in enumerate(row):
                if isinstance(piece, QuanCo):
                    # Cập nhật điểm
                    if piece.mau == MAU_TRANG:
                        score_trang += 1
                    elif piece.mau == MAU_DEN:
                        score_den += 1

                    # Tính các nước đi hợp lệ cho quân cờ này
                    directions = [(-1, -1), (-1, 1)] if piece.mau == MAU_TRANG else [(1, -1), (1, 1)]
                    for d in directions:
                        new_row = row_idx + d[0]  # Tính vị trí mới của quân cờ thay đổi về hàng
                        new_col = col_idx + d[1]  # Tính vị trí mới của quân cờ thay đổi về cột

                        # Kiểm tra nếu vị trí mới nằm trong bàn cờ
                        if 0 <= new_row < SO_HANG and 0 <= new_col < SO_COT:
                            target_piece = self.board.banCo[new_row][new_col]

                            # 1. Ưu tiên ăn sạch quân đối thủ
                            if target_piece and isinstance(target_piece, QuanCo) and target_piece.mau != piece.mau:
                                return score_trang, score_den, (row_idx, col_idx, new_row, new_col)

        # 2. Ưu tiên ăn quân trước mặt
        for row_idx, row in enumerate(self.board.banCo):
            for col_idx, piece in enumerate(row):
                if isinstance(piece, QuanCo):
                    directions = [(-1, -1), (-1, 1)] if piece.mau == MAU_TRANG else [(1, -1), (1, 1)]
                    for d in directions:
                        new_row = row_idx + d[0]  # Tính vị trí mới của quân cờ thay đổi về hàng
                        new_col = col_idx + d[1]  # Tính vị trí mới của quân cờ thay đổi về cột

                        if 0 <= new_row < SO_HANG and 0 <= new_col < SO_COT:
                            target_piece = self.board.banCo[new_row][new_col]
                   
                           # Kiểm tra có quân đối thủ phía trước không để ăn
                            if target_piece and isinstance(target_piece, QuanCo) and target_piece.mau != piece.mau:
                               return score_trang, score_den, (row_idx, col_idx, new_row, new_col)

        # 3. Tiến lại gần đối thủ
        for row_idx, row in enumerate(self.board.banCo):
            for col_idx, piece in enumerate(row):
                if isinstance(piece, QuanCo):
                    directions = [(-1, -1), (-1, 1)] if piece.mau == MAU_TRANG else [(1, -1), (1, 1)]
                    for d in directions:
                        new_row = row_idx + d[0]  # Tính vị trí mới của quân cờ thay đổi về hàng
                        new_col = col_idx + d[1]  # Tính vị trí mới của quân cờ thay đổi về cột

                        # Kiểm tra nếu vị trí mới nằm trong bàn cờ
                        if 0 <= new_row < SO_HANG and 0 <= new_col < SO_COT:
                            target_piece = self.board.banCo[new_row][new_col]

                            # Nếu ô trống, tiến lại gần đối thủ
                            if not target_piece:  # Ô trống
                                distance_to_enemy = self._distance_to_closest_enemy(piece.mau, new_row, new_col)
                                if best_move is None or distance_to_enemy < best_move[4]:
                                    best_move = (row_idx, col_idx, new_row, new_col, distance_to_enemy)

        # 4. Phong vua (đưa quân thường đến hàng cuối)
        for row_idx, row in enumerate(self.board.banCo):
            for col_idx, piece in enumerate(row):
                if isinstance(piece, QuanCo) and not piece.vua:  # Nếu là quân thường
                    if (piece.mau == MAU_TRANG and row_idx == SO_HANG - 1) or (piece.mau == MAU_DEN and row_idx == 0):
                        return score_trang, score_den, (row_idx, col_idx, row_idx, col_idx, "Phong vua")

        # 5. Sử dụng vua để tiến lại gần và chuẩn bị ăn đối thủ
        for row_idx, row in enumerate(self.board.banCo):
            for col_idx, piece in enumerate(row):
                if isinstance(piece, QuanCo) and piece.vua:  # Nếu là quân vua
                    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Vua có thể đi 4 hướng
                    for d in directions:
                        current_row, current_col = row_idx, col_idx
                        while True:
                            new_row = current_row + d[0]  # Tính vị trí mới của quân cờ thay đổi về hàng
                            new_col = current_col + d[1]  # Tính vị trí mới của quân cờ thay đổi về cột

                            # Kiểm tra nếu vị trí mới nằm trong bàn cờ
                            if 0 <= new_row < SO_HANG and 0 <= new_col < SO_COT:
                                target_piece = self.board.banCo[new_row][new_col]

                                # Nếu có quân đối thủ trước mặt, ăn quân đó
                                if target_piece and isinstance(target_piece, QuanCo) and target_piece.mau != piece.mau:
                                    return score_trang, score_den, (current_row, current_col, new_row, new_col)

                                # Nếu ô trống, tiếp tục di chuyển về phía đối thủ
                                if target_piece is None:
                                    current_row, current_col = new_row, new_col
                                else:
                                    break  # Dừng nếu gặp quân đồng minh hoặc có vật cản
                            else:
                                break  # Dừng nếu ra ngoài bàn cờ

        # 6. Nếu không có lựa chọn, thực hiện nước đi bất kỳ hợp lệ
        if not best_move:
            for row_idx, row in enumerate(self.board.banCo):
                for col_idx, piece in enumerate(row):
                    if isinstance(piece, QuanCo):
                        directions = [(-1, -1), (-1, 1)] if piece.mau == MAU_TRANG else [(1, -1), (1, 1)]
                        for d in directions:
                            new_row = row_idx + d[0]
                            new_col = col_idx + d[1]
                            if 0 <= new_row < SO_HANG and 0 <= new_col < SO_COT:
                                target_piece = self.board.banCo[new_row][new_col]
                                if target_piece is None:  # Nếu ô trống
                                    best_move = (row_idx, col_idx, new_row, new_col)
                                    break
                        if best_move:
                            break

        # Trả về điểm và nước đi tốt nhất
        return score_trang, score_den, best_move


    def _distance_to_closest_enemy(self, color, row, col):
        """
        Tính khoảng cách ngắn nhất đến quân đối thủ.
        """
        min_distance = float('inf')
        for r_idx, row_data in enumerate(self.board.banCo):
            for c_idx, piece in enumerate(row_data):
                if isinstance(piece, QuanCo) and piece.mau != color:
                    distance = abs(row - r_idx) + abs(col - c_idx)
                    min_distance = min(min_distance, distance)
        return min_distance
    
    def isCaptureMove(self, move):
        """
        Kiểm tra xem nước đi có ăn quân đối thủ không.
        move: tuple (start, end), mỗi phần tử là tuple (row, col)
        """
        if isinstance(move, tuple) and len(move) == 2:  # Kiểm tra xem move có phải là tuple với 2 phần tử không
            start, end = move  # unpack move thành 2 phần: start và end
            if isinstance(start, tuple) and isinstance(end, tuple):
                start_row, start_col = start
                end_row, end_col = end
            
                # Kiểm tra quân ở ô đích
                target_piece = self.board.banCo[end_row][end_col]
                piece = self.board.banCo[start_row][start_col]
            
                # Kiểm tra ô đích có quân đối thủ không
                if target_piece is not None and isinstance(target_piece, QuanCo):
                    return target_piece.mau != piece.mau
        else:
            print(f"Lỗi: Nước đi không đúng định dạng, move = {move}")
        return False



    def evaluateMove(self, move):
        """
        Khảo sát_Đánh giá nước đi dựa trên các tiêu chí:
        - Ăn quân đối thủ: +10 điểm
        - Tiến gần quân đối thủ: điểm dựa trên khoảng cách
        - Phong vua: +15 điểm
        """
        # Kiểm tra nếu move là tuple chứa start và end
        if isinstance(move, tuple) and len(move) == 2:
            start, end = move  # unpack move thành 2 phần: start và end

            # Kiểm tra start là tuple (row, col)
            if isinstance(start, tuple) and len(start) == 2:
                start_row, start_col = start  # start phải là tuple (row, col)
            else:
                print(f"Invalid start value: {start}")
                return 0  # Trả về điểm 0 nếu start không hợp lệ

            # Kiểm tra end là tuple (row, col)
            if isinstance(end, tuple) and len(end) == 2:
                end_row, end_col = end  # end phải là tuple (row, col)
            else:
                print(f"Invalid end value: {end}")
                return 0  # Trả về điểm 0 nếu end không hợp lệ

            piece = self.board.banCo[start_row][start_col]
            target_piece = self.board.banCo[end_row][end_col]

            score = 0

            # Ưu tiên ăn quân
            if self.isCaptureMove(move):
                score += 10

            # Tiến gần đối thủ
            score -= self._distance_to_closest_enemy(piece.mau, end_row, end_col)

            # Phong vua
            if piece.is_regular_piece() and (
                (piece.mau == MAU_TRANG and end_row == 0) or
                (piece.mau == MAU_DEN and end_row == len(self.board.banCo) - 1)
            ):
                score += 15

            return score
        else:
            print(f"Invalid move format: {move}")
            return 0  # Trả về điểm 0 nếu move không hợp lệ

    def getWalkMoves(self, piece):
        if piece is None:  # Đảm bảo piece không phải là None
            return []

        walkMoves = set([])  # Khởi tạo tập hợp các ô hợp lệ để di chuyển
    
        # Kiểm tra nếu quân cờ đã được phong vua (quân có thể đi cả lên và xuống)
        if piece.vua:  # Giả sử bạn có một thuộc tính `isKing` để kiểm tra nếu quân là vua
            directions = [
            (-1, -1), (-1, 1),  # Di chuyển lên trái, lên phải
            (1, -1), (1, 1),    # Di chuyển xuống trái, xuống phải
        ]
        else:
            # Di chuyển chéo tùy theo màu quân
            if piece.mau == MAU_TRANG:
                directions = [(1, -1), (1, 1)]  # Quân trắng di chuyển chéo xuống
            else:
                directions = [(-1, -1), (-1, 1)]  # Quân đen di chuyển chéo lên
    
        # Kiểm tra các hướng di chuyển
        for direction in directions:
            rowMove = piece.hang + direction[0]
            colMove = piece.cot + direction[1]
    
            # Kiểm tra nếu ô mới hợp lệ (nằm trong bàn cờ và trống)
            if 0 <= rowMove < SO_HANG and 0 <= colMove < SO_COT:
                leftSquare = self.board.banCo[rowMove][colMove]
                if leftSquare is None:  # Ô trống
                    walkMoves.add((rowMove, colMove))
    
        return walkMoves

    def getValidMoves(self, selectedPiece):
        """Xác định các bước đi hợp lệ của quân cờ được chọn gồm di chuyển thông thường và nhảy ăn quân đối thủ"""
        validMoves = set([])  # Khởi tạo tập hợp các ô hợp lệ để di chuyển
        if selectedPiece is None:  # Kiểm tra nếu không có quân cờ được chọn
            return []  # Trả về danh sách rỗng

        # Lấy thông tin của quân cờ được chọn
        piece = selectedPiece

        # Kiểm tra nếu piece là đối tượng thuộc lớp QuanCo
        if not isinstance(piece, QuanCo):
            print(f"Lỗi: Đối tượng tại vị trí không phải là quân cờ hợp lệ.")
            return validMoves  # Trả về danh sách rỗng nếu không phải quân cờ hợp lệ
    
        # Kiểm tra nếu quân cờ không phải là None và thuộc lượt người chơi
        if piece.mau == self.turn:
            # Tính toán các bước đi bộ hợp lệ (di chuyển thông thường)
            walkMoves = self.getWalkMoves(piece)
            validMoves.update(walkMoves)

            # Tính các bước nhảy hợp lệ nếu có
            jumpMoves = self.getJumpMoves(piece)
            validMoves.update(jumpMoves)
    
        # Hiển thị các ô hợp lệ cho quân cờ được chọn
        print(f"Các ô hợp lệ mà {piece.mau} tại ({piece.hang}, {piece.cot}) có thể di chuyển đến: {validMoves}")
        return validMoves


    def getJumpMoves(self, piece):
        # Tính các bước nhảy qua quân đối phương
        jumpMoves = set([]) 
        for direction in piece.huong:
            rowJump = piece.hang + direction[0] * 2
            colJump = piece.cot + direction[1] * 2
            if 0 <= rowJump < SO_HANG and 0 <= colJump < SO_COT:
                leftPiece = self.board.banCo[piece.hang + direction[0]][piece.cot + direction[1]]
                if leftPiece is not None and leftPiece.mau != piece.mau:
                    jumpSquare = self.board.banCo[rowJump][colJump]
                    if jumpSquare is None:
                        jumpMoves.add((rowJump, colJump))
        return jumpMoves

    def phongVua(self, piece):
        # Kiểm tra nếu quân cờ đã tới hàng cuối và phong vua
        if piece.mau == MAU_TRANG and piece.hang == SO_HANG - 1:
            piece.taoVua()  # Phong quân trắng thành vua
        elif piece.mau == MAU_DEN and piece.hang == 0:
            piece.taoVua()  # Phong quân đen thành vua
    
 
    def stop_timer(self):
        """Hủy tất cả các callback đang chạy của đồng hồ đếm ngược."""
        if self.timer_running and self.timer_id is not None:
            try:
                self.window.after_cancel(self.timer_id)  # Hủy callback của đồng hồ đếm ngược
                self.timer_running = False
            except ValueError:
                # Nếu có lỗi xảy ra, có thể là vì timer_id không hợp lệ
                print("Lỗi: timer_id không hợp lệ.")
                self.timer_running = False

    
    def changeTurn(self):
        """Chuyển lượt của người chơi và hiển thị thông báo"""
        self.stop_timer()  # Dừng timer nếu đang chạy
    
        if self.turn == MAU_TRANG:
            self.turn = MAU_DEN
            self.turn_label.config(text="Lượt chơi: Quân đen")  # Cập nhật thông báo
        else:
            self.turn = MAU_TRANG
            self.turn_label.config(text="Lượt chơi: Quân trắng")  # Cập nhật thông báo
            
            if self.ai_mode and self.turn == MAU_TRANG:
                self.ai_move() # AI tự động thực hiện nước đi

        self.update_score()
        # Reset lại thời gian mỗi khi chuyển lượt
        self.time_left = THOI_GIAN_LUOT
        self.timer_running = False  # Đặt lại trạng thái của timer
        self.start_timer()
                 
    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.board.banCo[start_row][start_col]  # Lấy quân cờ đang chọn
    
        # Kiểm tra nếu ô đích có quân cờ hoặc không có quân nào ở vị trí bắt đầu
        if piece is None or self.board.banCo[end_row][end_col] is not None:
            return False
    
        last_direction = None  # Hướng di chuyển cuối cùng (chỉ sử dụng khi ăn quân)
    
        eaten_count = 0  # Đếm số quân cờ đối phương bị ăn trong quá trình di chuyển
    
        # Kiểm tra bước nhảy (có sự chênh lệch lớn giữa vị trí ban đầu và vị trí đích)
        if abs(start_row - end_row) > 1 or abs(start_col - end_col) > 1:
            # Tính toán vị trí quân bị nhảy qua (quân đối phương)
            rowEatenPiece = (start_row + end_row) // 2
            colEatenPiece = (start_col + end_col) // 2
    
            # Kiểm tra xem ô trung gian có quân đối phương không
            eaten_piece = self.board.banCo[rowEatenPiece][colEatenPiece]
            if eaten_piece is not None and eaten_piece.mau != piece.mau:
                print(f"Quân tại ({rowEatenPiece}, {colEatenPiece}) ăn: {eaten_piece}")
                # Xóa quân bị ăn
                self.board.banCo[rowEatenPiece][colEatenPiece] = None
                self.update_score()
                last_direction = (end_row - start_row, end_col - start_col)  # Lưu hướng
                eaten_count += 1  # Tăng số quân ăn được
            else:
                return False  # Không hợp lệ nếu không có quân đối phương bị ăn
    
        # Di chuyển quân cờ đến ô mới
        self.board.banCo[end_row][end_col] = piece
        self.board.banCo[start_row][start_col] = None
    
        # Cập nhật vị trí của quân cờ
        piece.hang, piece.cot = end_row, end_col
    
        # Cập nhật phong vua sau lần di chuyển đầu tiên
        self.phongVua(piece)
    
        moved = True  # Biến kiểm tra xem quân cờ đã di chuyển chưa
    
        # Kiểm tra và tiếp tục ăn thêm quân (nếu có thể)
        while moved:
            directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]  # Các hướng có thể di chuyển chéo
            can_eat_more = False
    
            for dx, dy in directions:
                new_row = end_row + dx
                new_col = end_col + dy
    
                # Kiểm tra nếu có thể ăn quân trong nước đi này
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board.banCo[new_row][new_col] is None:  # Ô đích trống
                        rowEatenPiece = (end_row + new_row) // 2
                        colEatenPiece = (end_col + new_col) // 2
                        eaten_piece = self.board.banCo[rowEatenPiece][colEatenPiece]
                        if (
                            eaten_piece is not None and eaten_piece.mau != piece.mau
                            and (last_direction is None or (dx, dy) == last_direction)
                        ):
                            # Nếu đã ăn ít nhất 1 quân cờ thì mới được ăn tiếp
                            if eaten_count > 0:
                                print(f"Có thể tiếp tục ăn. Ăn quân ({rowEatenPiece}, {colEatenPiece})")
                                # Xóa quân bị ăn
                                self.board.banCo[rowEatenPiece][colEatenPiece] = None
                                self.update_score()
                                # Di chuyển quân cờ
                                self.board.banCo[new_row][new_col] = piece
                                self.board.banCo[end_row][end_col] = None
                                piece.hang, piece.cot = new_row, new_col
                                end_row, end_col = new_row, new_col  # Cập nhật vị trí hiện tại
                                last_direction = (dx, dy)  # Cập nhật hướng
                                can_eat_more = True
                                # Cập nhật phong vua chỉ sau lần ăn thứ hai và nếu quân cờ ở vị trí cuối của bàn cờ
                                if eaten_count == 1:
                                    if (piece.mau == 'white' and new_row == 7) or (piece.mau == 'black' and new_row == 0):
                                        #print(f"King promotion for {piece.mau} piece at position ({new_row}, {new_col})")
                                        self.phongVua(piece)
                                break
    
            # Nếu không thể ăn tiếp, kết thúc
            if not can_eat_more:
                moved = False  # Dừng vòng lặp khi không thể ăn thêm
        return True


    def on_click(self, event):
        # Lấy vị trí của ô người dùng click
        row = event.y // KICH_THUOC_O
        col = event.x // KICH_THUOC_O
    
        print(f"Chọn hàng {row}, cột {col}")  # Debug: In ra vị trí người dùng click
    
        # Kiểm tra nếu chế độ AI và lượt của AI
        if self.ai_mode and self.turn == MAU_TRANG:
            print("Lượt chơi của AI. Không cho phép người chơi chọn.")
            return  # Không cho phép chọn quân khi là lượt của AI
    
        if self.selected:
            # Nếu đã chọn quân, kiểm tra ô đã chọn có hợp lệ không
            if (row, col) in self.validMoves:
                # Di chuyển quân và kiểm tra việc xóa quân nếu cần
                if self.move_piece(self.selected[0], self.selected[1], row, col):
                    # Đổi lượt chơi
                    self.changeTurn()
                    self.selected = None
                    self.validMoves = set()
            else:
                print(f"Không hợp lệ để di chuyển tới: ({row}, {col})")
                # Nếu ô click không hợp lệ, hủy chọn quân
                self.selected = None
                self.validMoves = set()
        
        else:
            # Nếu chưa chọn quân, kiểm tra xem quân đó có phải của mình không
            piece = self.board.banCo[row][col]
            if piece is not None and piece.mau == self.turn:
                # Nếu là quân của mình, chọn quân cờ và tính toán các ô hợp lệ
                self.selected = (row, col)
                self.validMoves = self.getValidMoves(piece)
    
        # Cập nhật và vẽ lại bàn cờ sau mỗi lần di chuyển
        self.board.veBanCo(self.canvas)
        self.updateBoardWithHighlights()
        # Kiểm tra kết thúc trận đấu
        winner = self.board.kiemTraThang()
        if winner:
            self.show_winner(winner)
    
    def highlightCell(self, row, col, color="green", width=3):
        # Chuyển đổi hàng/cột thành tọa độ pixel
        x1 = col * KICH_THUOC_O
        y1 = row * KICH_THUOC_O
        x2 = x1 + KICH_THUOC_O
        y2 = y1 + KICH_THUOC_O
    
        # Vẽ viền xung quanh ô
        self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=width)

    def drawScore(self, canvas, score_trang, score_den):
            """Vẽ điểm của quân trắng và quân đen trên bàn cờ."""
            # Khoảng cách giữa điểm và bàn cờ
            padding = 30  # Khoảng cách để điểm không bị dính vào bàn cờ
    
            # Vẽ điểm của quân trắng ở góc trên trái
            canvas.create_text(50, padding, text=f"Quân trắng: {score_trang}", font=("Helvetica", 14), fill="black")
    
            # Vẽ điểm của quân đen ở góc trên phải
            canvas.create_text(SO_COT * KICH_THUOC_O - 50, padding, text=f"Quân đen: {score_den}", font=("Helvetica", 14), fill="black")

    def updateBoardWithHighlights(self):
        """Cập nhật và làm mới bàn cờ, bao gồm các đường đi và điểm của quân cờ."""
        self.board.veBanCo(self.canvas)  # Vẽ lại bàn cờ và quân cờ

        # Lấy điểm của quân trắng và quân đen, và nước đi tốt nhất
        result = self.evaluateBoard()  # Lấy tổng điểm của quân trắng và quân đen cùng với nước đi tốt nhất

        # Kiểm tra nếu kết quả trả về có 3 phần
        if len(result) == 3:
            score_trang, score_den, best_move = result  # Gán đúng 3 phần
        else:
            score_trang, score_den = result  # Chỉ có 2 phần, điểm quân trắng và quân đen
            best_move = None  # Nếu không có nước đi tốt nhất, gán best_move là None

        # Vẽ điểm tổng của quân trắng và quân đen trên bàn cờ
        """self.drawScore(self.canvas, score_trang, score_den)"""

        # Hiển thị các ô hợp lệ (nếu có) và quân cờ được chọn
        if self.selected:
            self.highlightCell(self.selected[0], self.selected[1], color="blue")  # Ô được chọn

        for move in self.validMoves:
            self.highlightCell(move[0], move[1], color="green")  # Các ô hợp lệ



    def start_game(self):
        # Tạo giao diện trò chơi
        self.canvas = tk.Canvas(self.window, width=KICH_THUOC_O * SO_COT, height=KICH_THUOC_O * SO_HANG)
        self.canvas.pack()

        # Vẽ bàn cờ và quân cờ
        self.board.veBanCo(self.canvas)

        # Gán sự kiện click chuột
        self.canvas.bind("<Button-1>", self.on_click)
        

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

def create_game_window(ai_mode=False, depth=1):
    """Khởi tạo giao diện trò chơi"""
    window = tk.Tk()
    window.title("Cờ Đam")
    window.geometry("600x600")
    
    tk.Label(window, text="Chơi Cờ Đam", font=("Helvetica", 20, "bold"), bg="#EDEDED").pack(pady=20)
    # Khởi tạo trò chơi
    game = Game(window, ai_mode,depth)
    game.start_game()
    window.mainloop()

if __name__ == "__main__":
    create_game_window()