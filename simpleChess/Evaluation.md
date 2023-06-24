### Bản chất của hàm evaluation Stockfish
- Là hàm đánh giá theo hướng tiếp cận heuristically, xác định giá trị liên quan tới thế cờ trong một trường hợp tổng quát, khi không có một sự đánh giá chuyên biệt hoặc tablebase (các thế tàn cuộc). 
- Không đánh giá các thế cờ mà trong đó quân vua của một trong hai bên bị chiếu.
- Kết quả cuối cùng được tạo bởi sự kết hợp của **Đánh giá trung cuộc (Middle game Evaluation)** và **Đánh giá tàn cuộc (End game Evaluation)**.
  - Sử dụng ***Tapered Eval*** để có được sự chuyển giao mượt mà giữa các phase của một ván đấu.
  - Sử dụng **Scale Factor** được sử dụng để giảm thiểu **Đánh giá tàn cuộc**

> _**Tapered Eval** là như thế nào ?_

* Là kĩ thuật được sử dụng để tạo sự chuyển giao mượt mà giữa các phase của một ván cờ bằng việc sử dụng giá trị số cụ thể và chi tiết của phase của game, tính tới các loại quân cờ đã bị chiếm giữ tính tới thời điểm hiện tại.
* Kĩ thuật yêu cầu kết hợp hai giá trị phân biệt của thế cờ, với định lượng ứng với khai cuộc và tàn cuộc.
  * Phase hiện tại của ván đấu được sử dụng để nội suy (interpolate) giữa các giá trị này

**-> Giảm sự gián đoạn giữa các giai đoạn evaluation.**

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