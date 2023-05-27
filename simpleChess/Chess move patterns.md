* Với **tốt (pawn)**:
    - Các quân tốt có thể đi 1 hoặc 2 bước (nếu không bị chặn) nếu vẫn ở row 2 (quân đen) hoặc row 7 (quân trắng)
    - Quân tốt sau khi rời vị trí ban đầu chỉ có thể tiến thêm 1 bước
    - Quân tốt ko thể tiến lên nếu trước đó có quân khác chặn (cả trắng và đen)
    - Quân tốt ăn chéo 1 ô
    - Quân tốt có thể thực hiện "Bắt tốt qua đường" (en passant):
      - ĐK: quân tốt đối phương vừa đi 2 ô, tới vị trí ngay cạnh quân tốt của mình (theo hàng ngang)
      - Quân tốt tham gia bắt di chuyển chéo lên, ra phía sau của quân bị bắt
    - Quân tốt sau khi đi đến hàng cuối cùng của bàn thờ có thể phong (promotion) thành bất cứ quân cờ nào khác (trừ vua)

* Với **xe (rock)**:
    - Đi hết hàng dọc, ngang
    - Có thể ăn quân đối thủ nếu nằm trên đường đi 

* Với **mã (knight)**:
    - đi theo hình chữ L: vị trí hiện tại (r,c)
    -> Có thể đi tới các ô (r + 2, c + 1), (r + 1, c + 2), ...
    git push origin feature/pawn_move_update
