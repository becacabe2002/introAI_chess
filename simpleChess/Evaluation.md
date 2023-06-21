
> *Vì sao cần có `Tempo Bonus` ?*

* Để tránh sự dao động của điểm số dựa trên độ chẵn lẻ của độ sâu tìm kiếm, chương trình cung cấp một điểm cộng cho người chơi có quyền đi quân.
  * Điều này có lợi trong giai đoạn Opening và Midgame, nhưng có thể phản tác dụng ở Endgame.

> *Vì sao cần 'to scale the endgame evaluation score down.' ?*

* Vật chất (raw material) trở nên quan trọng hơn ở Endgame:
  * Trong Opening và Midgame, các yếu tố như cấu trúc quân tốt, sự an toàn của vua ..,
  * Nhưng khi vào Endgame, số lượng quân còn lại ít, giá trị vật chất có xu hướng tăng.
  * Việc giảm tỷ lệ điểm đánh giá giúp nhấn mạnh tầm quan trọng của vật chất.

* Đơn giản hóa hàm đánh giá:
  * Cho phép tính toán hiệu quả và tối ưu hơn, nhất là khi số lượng quân cờ còn lại bị giới hạn

* Tránh những sự phức tạp không cần thiết:
    * Giảm sự phức tạp từ các yếu tố khác, giảm biến động tiềm năng
    * Tăng tính ổn định của phép đánh giá

* Đồng nhất trong quá trình đánh giá:
  * bằng việc áp dụng một scaling factor đồng nhất trong suốt ván đấu, hàm đánh giá sẽ giữ được sự tiếp cận nhất quán tới định lượng các yếu tố khác nhau ở các stage khác nhau của game.