# Báo Cáo Phân Tích Dữ Liệu & Trực Quan Hóa Hoạt Động Kinh Doanh (Ecommerce Analytics)

**Học phần**: Trực quan hóa dữ liệu với Python (Python Data Visualization)  
**Tập dữ liệu**: Ecommerce Sales & Returns Dataset (2023 – 2025)  
**Quy mô**: 100,000 đơn hàng | 237,537 chi tiết sản phẩm | 20,000 khách hàng | 105,388 thanh toán | 7,910 hoàn trả  

---

## 1. Tổng Quan Chỉ Số Hiệu Suất Cốt Lõi (Executive KPIs)

| Chỉ số (KPI) | Giá trị thực tế | Ý nghĩa & Đánh giá |
| :--- | :--- | :--- |
| **Tổng số đơn hàng (Orders)** | **100,000** | Quy mô đơn hàng ổn định trong 3 năm |
| **Khách hàng phát sinh mua hàng** | **19,868** | ~99.34% tổng số tài khoản đăng ký đã từng mua |
| **Tổng doanh thu gộp (Gross Sales)** | **$60,483,519.62** | Tổng giá trị hàng bán chưa trừ hoàn trả |
| **Tổng tiền thanh toán thành công** | **$63,458,562.67** | Bao gồm tiền hàng, thuế và phí vận chuyển |
| **Tổng tiền hoàn trả (Refunds)** | **$3,387,902.65** | Số tiền phát sinh từ 7,910 sự kiện hoàn tiền |
| **Doanh thu thuần thực nhận (Net Sales)** | **$60,070,660.02** | Dòng tiền thuần thực tế ghi nhận |
| **Tỷ lệ hoàn tiền (Refund Rate %)** | **5.34%** | Nằm trong ngưỡng an toàn của ngành bán lẻ điện tử |
| **Giá trị trung bình đơn hàng (AOV)** | **$600.71** | Chi tiêu trung bình trên mỗi đơn hàng |
| **Phân khúc khách hàng chủ lực** | **Consumer (Cá nhân)** | Chiếm số lượng đơn và tổng giá trị lớn nhất |
| **Kênh tiếp cận khách hàng hàng đầu** | **Organic Search** | Chiếm tỷ trọng cao nhất trong cơ cấu khách hàng |

---

## 2. Danh Mục 13 Đồ Thị Trực Quan Hóa Đã Xuất Bản (`reports/figures/`)

Tất cả các đồ thị được xuất bản ở định dạng 300 DPI tiêu chuẩn báo cáo:

1. **`01_financial_performance_trends.png`**:
   - *Dạng biểu đồ*: Đồ thị đa đường (Multi-line plot) kết hợp đường trung bình động 3 tháng (3-Month Rolling Average).
   - *Insight*: Doanh thu hàng tháng có xu hướng tăng trưởng bền vững, các đợt hoàn tiền được kiểm soát ở mức biên độ hẹp (~5%).
2. **`02_segment_revenue_growth_multiline.png`**:
   - *Dạng biểu đồ*: Đồ thị đa đường so sánh quỹ đạo doanh thu giữa 3 phân khúc (Consumer, Small Business, Enterprise).
   - *Insight*: Phân khúc Consumer chiếm tỷ trọng doanh thu cao nhất, phân khúc Enterprise có độ ổn định cao hơn về chu kỳ.
3. **`03_order_total_distribution_hist_box.png`**:
   - *Dạng biểu đồ*: Histogram kết hợp đường cong mật độ xác suất KDE và Boxplot lọc theo phân vị 99th percentile.
   - *Insight*: Phân phối giá trị đơn hàng có độ lệch phải (right-skewed), tập trung chủ yếu trong khoảng $200 – $700.
4. **`04_payment_methods_box_violin.png`**:
   - *Dạng biểu đồ*: Box plot và Violin plot so sánh phân bổ giá trị đơn hàng theo phương thức thanh toán (`card`, `paypal`, `bank_transfer`).
   - *Insight*: `bank_transfer` có xu hướng phục vụ các đơn hàng giá trị lớn hơn so với `card` và `paypal`.
5. **`05_refund_reasons_swarm_plot.png`**:
   - *Dạng biểu đồ*: Swarm / Strip plot kèm điểm trung bình (Pointplot) thể hiện giá trị hoàn tiền theo từng lý do hoàn trả.
   - *Insight*: Các khiếu nại về lỗi sản phẩm hoặc giao trễ có giá trị hoàn trả cao nhất.
6. **`06_acquisition_channel_donut.png`**:
   - *Dạng biểu đồ*: Donut / Pie Chart thể hiện thị phần của các kênh tiếp cận khách hàng.
   - *Insight*: Kênh Organic Search và Direct chiếm hơn 50% cơ cấu khách hàng mới.
7. **`07_top_products_revenue_bar.png`**:
   - *Dạng biểu đồ*: Horizontal Bar Chart xếp hạng Top 10 sản phẩm bán chạy nhất kèm nhãn doanh thu và lợi nhuận.
8. **`08_customer_segment_catplot.png`**:
   - *Dạng biểu đồ*: Seaborn Catplot phân tích AOV theo phân khúc khách hàng và phương thức thanh toán.
9. **`09_product_cost_vs_price_scatter.png`**:
   - *Dạng biểu đồ*: Scatter plot giữa Giá vốn (Unit Cost) và Giá niêm yết (List Price) của 1,200 sản phẩm theo danh mục và đường hòa vốn 1:1.
   - *Insight*: Tất cả sản phẩm đều nằm trên đường hòa vốn, nhóm hàng Electronics và Fashion có biên lợi nhuận gộp hấp dẫn nhất.
10. **`10_rfm_multivariate_pairplot.png`**:
    - *Dạng biểu đồ*: Seaborn Pairplot đa biến giữa Recency, Frequency và log-Monetary tô màu theo nhóm phân khúc RFM.
    - *Insight*: Tách biệt rõ nét giữa nhóm Champions/Loyal và nhóm At Risk/Hibernating.
11. **`11_facetgrid_category_segments.png`**:
    - *Dạng biểu đồ*: Seaborn FacetGrid phân bố doanh số chi tiết mặt hàng theo phân khúc khách hàng.
12. **`12_cohort_retention_heatmap.png`**:
    - *Dạng biểu đồ*: Heatmap ma trận tỷ lệ giữ chân khách hàng (Cohort Retention %) hàng tháng qua các chu kỳ.
13. **`13_financial_correlation_heatmap.png`**:
    - *Dạng biểu đồ*: Correlation Heatmap với mặt nạ tam giác trên hiển thị ma trận hệ số tương quan Pearson giữa 7 chỉ số tài chính.

---

## 3. Khuyến Nghị Chiến Lược Kinh Doanh

1. **Kiểm soát và phòng ngừa rủi ro hoàn tiền (Refund Management)**:
   - Với $3.38 triệu tiền hoàn trả, doanh nghiệp cần tập trung vào các nhóm sản phẩm có tần suất hoàn trả cao nhất để tối ưu lại khâu đóng gói, vận chuyển và mô tả sản phẩm.
2. **Chiến lược giữ chân khách hàng (Retention & Loyalty Programs)**:
   - Tỷ lệ giữ chân sau tháng đầu tiên cho thấy phần lớn khách hàng chỉ mua 1 lần. Cần tự động hóa luồng email chăm sóc khách hàng sau 30 ngày (Follow-up sequence) và cung cấp voucher tái mua cho nhóm "Potential Loyalists".
3. **Khai thác tối đa kênh tiếp cận hữu cơ (Organic Acquisition)**:
   - Tiếp tục đầu tư nâng cấp SEO và trải nghiệm giao diện người dùng, đồng thời đẩy mạnh chương trình Referral (giới thiệu bạn bè) nhằm tận dụng lượng khách hàng trung thành sẵn có.
