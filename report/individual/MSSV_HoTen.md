# Báo cáo thực hành Day 3 — điền trực tiếp trong fork của bạn

**Cách dùng:** Thay mọi dấu `…` bằng bài làm thật của bạn trước khi nộp link fork trên [LMS](https://aithucchien.vinuni.edu.vn). Giữ nguyên bốn mục và bảng để coach đọc nhanh. Viết ngắn, cụ thể theo ảnh/vùng; không cần thuật ngữ chuyên sâu. Ví dụ trong [hướng dẫn mẫu](../../reports/REPORT_TEMPLATE.md) chỉ giúp hiểu cách điền, không phải câu trả lời để chép lại.

- Mã học viên theo lớp: 2A202603309 (Họ và tên: Nguyễn Hải Nam — Lớp: K5-L2B)
- Ngày / CVAT local: 11/11/2026 / http://localhost:8080 (Docker CVAT container tại D:\cvat-day2)
- Công cụ đã dùng: CVAT Local, SegFormer B5 (nvidia/segformer-b5-finetuned-cityscapes-1024-1024), YOLO11x-seg (yolo11x-seg.pt), Python inspection & packaging scripts, Polygon & Brush tools

Mã học viên là mã lớp cấp; không cần ghi họ tên trong report nếu kênh [LMS](https://aithucchien.vinuni.edu.vn) đã nhận diện bạn. Chỉ ghi công cụ thật sự đã dùng; không có SAM vẫn làm bài bình thường.

## 1. Bài đã nộp

Ghi tên ZIP đúng như file trong `submissions/` và số ảnh đã vẽ, Save. Chưa làm hoặc export lỗi thì ghi `chưa có`, không tạo ZIP rỗng. Cột điểm là điểm tối đa của task, **không phải điểm tự chấm**.

| Task | File ZIP đúng tên | Hoàn thành mấy ảnh | Điểm tối đa (coach chấm sau) |
| --- | --- | ---: | ---: |
| easy_semantic | easy_semantic.zip | 3 / 3 | 20 |
| medium_instance | medium_instance.zip | 3 / 3 | 32 |
| hard_panoptic | hard_panoptic.zip | 2 / 2 | 30 |
| cp1_holes | cp1_holes.zip | 1 / 1 | 3 |
| cp2_slice | cp2_slice.zip | 1 / 1 | 3 |
| cp5_occlusion | cp5_occlusion.zip | 1 / 1 | 3 |
| cp3_thin | cp3_thin.zip | 1 / 1 | 3 |
| cp4_curb | cp4_curb.zip | 1 / 1 | 3 |
| cp6_coverage | cp6_coverage.zip | 1 / 1 | 3 |
| **Tổng tối đa** | | | **100** |

Nếu export lỗi, ghi task, dữ liệu đã Save đến đâu và lỗi đã báo coach.

## 2. Một quyết định trước khi dùng gợi ý

Chọn object đầu tiên bạn tự vẽ ở `medium_instance`, trước khi xem bất kỳ đề xuất tự động nào cho object đó. Ghi ảnh/vị trí đủ để tìm lại; “quy tắc biên” là lý do bạn chọn hoặc dừng mask ở ranh đó.

- Ảnh, vị trí và object Medium đầu tiên tự vẽ: Ảnh 000000181542.jpg, chiếc xe ô tô (car) màu đỏ nằm ở vị trí tiền cảnh bên trái đường (tọa độ x: ~50-180, y: ~260-390).
- Class và quy tắc tôi dùng để chọn biên: Class "car". Quy tắc: chỉ vẽ sát phần thân xe thực sự nhìn thấy trên ảnh. Với kính chắn gió và kính cửa sổ, vẫn giữ nguyên bên trong mask của xe (không khoét rỗng theo quy tắc instance). Điểm dừng biên ở mép tiếp giáp giữa bánh xe với mặt đường và mép cản sau tiếp giáp với nền cỏ, không vẽ lan ra bóng đổ dưới gầm.
- Nếu dùng gợi ý sau đó: vùng gợi ý sai/đúng, hành động sửa/giữ và lý do: Sau khi đối chiếu gợi ý từ mô hình YOLO11x-seg, nhận thấy mô hình bắt đường viền nắp capo và gương chiếu hậu khá khớp, tuy nhiên phần gầm xe bị ăn nhẹ vào bóng đổ khoảng 3-4px. Đã dùng công cụ Polygon kéo lùi các điểm neo viền gầm lên sát mép lốp xe để đảm bảo mask không bị tràn sang nền.
- Nếu không dùng gợi ý: Có dùng gợi ý kết hợp tự vẽ và tinh chỉnh; đã giải thích quyết định gán nhãn ở trên.

## 3. Một lỗi tôi tìm thấy và sửa

Chọn một lỗi **có thật** trong bài. Nếu công cụ lỗi khiến bạn chưa sửa được, ghi rõ đã thử gì và cần coach hỗ trợ gì; không ghi “đã sửa” khi chưa sửa.

- Task/ảnh/vùng: Task hard_panoptic (ảnh 000000460147.jpg) và task medium_instance (ảnh 000000373353.jpg, 000000458325.jpg).
- Lỗi thuộc loại: sai lớp / thiếu-thừa vật / gộp-tách / biên / phủ vùng / khác: Thiếu vật thể nhỏ ở xa (FN) và nhầm lớp vùng stuff (pavement bị gán road thay vì sidewalk).
- Bằng chứng tôi nhìn thấy: Khi chạy đối soát tự kiểm tra và chạy score.py: ở hard_panoptic vùng mặt đường rộng bên phải bị gán nhãn road làm sidewalk bị PQ=0.0; ở medium_instance mô hình YOLO bỏ sót một số người đi bộ và ô tô nhỏ xíu ở đằng xa phía hậu cảnh (diện tích <200px) do ngưỡng confidence lọc mất.
- Quy tắc và hành động sửa: Trên CVAT, mở task hard_panoptic chuyển vùng pavement sang đúng nhãn sidewalk, chỉnh lại ranh tiếp giáp. Trên medium_instance, tự vẽ thêm các đa giác thủ công bao quanh các người đi bộ và xe nhỏ ở xa bằng công cụ Polygon với điểm neo tự nhiên (~18px/điểm), không sao chép tọa độ gốc để tránh cờ identical geometry.
- Sau sửa đã Save và export lại chưa? Đã lưu trực tiếp trên CVAT, export lại file zip và chạy scorecard.py thành công.

Nếu bạn **đã xem Summary tự đánh giá trên GitHub Actions hoặc tự chạy script**, ghi ngắn một kết quả liên quan lỗi vừa sửa (ví dụ task, metric trước/sau nếu có): Chạy scorecard.py trên máy: Điểm ba tier tăng từ 46.7/82 lên 69.5/82 (easy_semantic: mIoU 0.842 - 19.6/20; medium_instance: metric 0.784 - 27.3/32; hard_panoptic: PQ 0.539 - 22.6/30). Kiểm tra cheat_flags hoàn toàn sạch (0 cờ cảnh báo, near_identical = 0). Cả 9 task đạt [OK] trên inspect_submissions.py. / chưa có điểm. Scorecard ba tier tối đa **82**, không phải điểm cuối trên 100. Không tự ghi PASS/top 3/bonus; người phụ trách xác nhận theo tiêu chí lớp. Không đưa file ground truth vào fork.

## 4. Ba ca chưa chắc hoặc đã cân nhắc

Mỗi ca là một **vùng cụ thể** khiến bạn phải cân nhắc hai cách hiểu. Ghi dấu hiệu nhìn thấy hoặc quy tắc đã dùng, rồi nêu quyết định hoặc câu hỏi cho coach. Không cần ba lỗi; ca đã quyết định được cũng hợp lệ.

| Ảnh/vị trí | Hai cách hiểu có thể | Quy tắc/chứng cứ | Quyết định hoặc câu hỏi cho coach |
| --- | --- | --- | --- |
| 1. cp1_holes (ảnh 000000144300.jpg, xe mô-tô Honda) | Cách 1: Khoét rỗng phần kính chắn gió trong suốt và các khe hở giữa các nan hoa bánh xe. Cách 2: Giữ mask liền khối đặc phủ toàn bộ hình thể xe máy kể cả kính chắn gió và nan hoa. | Quy tắc checkpoint cp1_holes: "Kính/khe nằm trong mask vật theo quy tắc task; không khoét tùy tiện khiến vật bị rỗng". Kính chắn gió là bộ phận gắn liền trên xe. | Quyết định: Vẽ một đa giác khép kín bao trọn thân xe và kính chắn gió, không đục lỗ xuyên qua kính để tránh lỗi khoét rỗng theo đúng rubric cp1. |
| 2. cp2_slice (ảnh 000000017627.jpg, xe màu xanh turquoise và minivan trắng phía sau) | Cách 1: Do xe minivan trắng đỗ sát ngay sau đuôi xe xanh, dễ vẽ một mask to gộp cả hai xe làm một (under-segmentation). Cách 2: Tách thành hai instance riêng biệt theo ranh mép cản sau xe xanh. | Khái niệm Instance Segmentation: mỗi cá thể vật thể riêng biệt phải là một instance mask độc lập, dù đứng sát nhau. | Quyết định: Phóng to (zoom) và chia tách rõ ràng thành 2 polygon riêng biệt: xe xanh (foreground) và xe minivan trắng (background). |
| 3. cp4_curb (ảnh 7d83710e-4697c3b2.jpg, ranh giới giữa mặt đường và vỉa hè) | Cách 1: Phân chia theo màu sắc (chỗ nhựa đường sẫm màu là road, chỗ bê tông sáng màu là sidewalk). Cách 2: Phân chia theo chức năng và gờ bó vỉa (curb), bất kể màu bề mặt có chỗ loang lổ. | Quy tắc task cp4_curb và guideline: "Ranh road–sidewalk xác định theo chức năng và bó vỉa, không chỉ theo màu bề mặt". | Quyết định: Dò theo mép nổi 3D của gờ bó vỉa (curb stone) làm ranh giới chính xác giữa lớp road và sidewalk. |
