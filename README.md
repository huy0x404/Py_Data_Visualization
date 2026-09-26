# Ecommerce Data Analytics & Visualization Project

Dự án phân tích và trực quan hóa dữ liệu thương mại điện tử chuyên sâu bằng Python, áp dụng toàn diện khung chương trình lý thuyết và thực hành từ **Chương 1 đến Chương 7 (CLO1 – CLO5)**.

---

## 📌 Khung Chương Trình Đã Áp Dụng (Curriculum Mapping)

| Tuần / Chương | Nội dung lý thuyết & thực hành | Triển khai trong Dự án |
| :--- | :--- | :--- |
| **Chương 1, 2** | Nền tảng Python, cú pháp, biến, kiểu dữ liệu, cấu trúc điều khiển, hàm, xử lý file, xử lý ngoại lệ | Xử lý dữ liệu đa nguồn, kiểm soát ngoại lệ tùy chỉnh (`src/core/exceptions.py`), `notebooks/01_...` |
| **Chương 3** | Lập trình hướng đối tượng (OOP): Lớp, Đối tượng, Đóng gói, Kế thừa, Đa hình, Trừu tượng | Kiến trúc trừu tượng `BaseDataLoader` (`src/data_loaders/`), domain models `Customer`, `Product`, `Order` |
| **Chương 4** | Thư viện Python chuẩn và độc lập cho Data Science / AI | Khai thác hệ sinh thái NumPy, Pandas, Scipy, Matplotlib, Seaborn |
| **Chương 5** | Tính toán số với NumPy: mảng đa chiều, vectorization, hàm thống kê, đại số tuyến tính | Chuẩn hóa Z-Score RFM, khoảng cách Euclid tới khách hàng VIP, ma trận tương quan (`src/processing/feature_engineering.py`), `notebooks/02_...` |
| **Chương 6** | Xử lý dữ liệu với Pandas: Series, DataFrame, merge, missing data, time-series, cohort | Làm sạch dữ liệu (`cleaner.py`), denormalization nối 6 bảng (`merger.py`), chuỗi thời gian & cohort retention matrix |
| **Chương 7** | Trực quan hóa với Matplotlib & Seaborn: Line, Multi-line, Scatter, Box, Violin, Donut, Bar, Swarm, Catplot, Pairplot, Heatmap | Hệ thống đồ thị 13 biểu đồ 300 DPI (`src/visualization/`), `reports/figures/`, `notebooks/04_...` |
| **Capstone** | Ôn tập, tích hợp pipeline hoàn chỉnh và báo cáo kết quả | CLI `main.py`, `src/pipeline.py`, `reports/executive_summary.md`, `notebooks/05_...` |

---

## 🚀 Hướng Dẫn Cài Đặt & Sử Dụng

### 1. Cài đặt môi trường
Đảm bảo đã cài đặt Python 3.10+ (khuyên dùng Python 3.12):
```bash
pip install -r requirements.txt
```

### 2. Chạy Pipeline phân tích dữ liệu & xuất toàn bộ biểu đồ
Chạy tự động toàn bộ quy trình từ dữ liệu CSV:
```bash
python main.py --source csv
```

Chạy từ cơ sở dữ liệu SQLite:
```bash
python main.py --source sqlite
```

### 3. Chạy kiểm thử tự động (Unit Tests)
```bash
pytest tests/ -v
```

### 4. Hệ thống Jupyter Notebooks (`notebooks/`)
- `01_python_fundamentals_oop.ipynb`: Nền tảng Python và lập trình hướng đối tượng.
- `02_numpy_computations.ipynb`: Tính toán số học vector hóa và khoảng cách RFM với NumPy.
- `03_pandas_data_processing.ipynb`: Xử lý, nối ghép bảng và phân tích chuỗi thời gian với Pandas.
- `04_matplotlib_seaborn_visualization.ipynb`: Trực quan hóa dữ liệu cơ bản và nâng cao.
- `05_ecommerce_capstone_analytics.ipynb`: Dự án tổng hợp và dashboard điều hành.

---

## 📊 Kết Quả Đầu Ra (Deliverables)

- **Dữ liệu đã xử lý (`data/processed/`)**:
  - `clean_master_orders.csv`: 100,000 giao dịch denormalized đầy đủ thông tin khách hàng, doanh thu thuần và hoàn tiền.
  - `customer_rfm_metrics.csv`: 19,868 khách hàng kèm chỉ số RFM, chuẩn hóa Z-score và phân khúc.
  - `monthly_financial_trends.csv`: Chuỗi thời gian doanh thu, hoàn tiền, AOV và trung bình động 3 tháng.
  - `cohort_retention_matrix.csv`: Ma trận tỷ lệ giữ chân khách hàng qua từng tháng.
- **Thư viện đồ thị (`reports/figures/`)**: 13 biểu đồ độ phân giải cao (300 DPI).
- **Báo cáo chuyên sâu**: `reports/executive_summary.md`.
