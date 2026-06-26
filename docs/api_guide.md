# Hướng dẫn Triển khai và Sử dụng API Dịch vụ Vietnamese Embedding

Dịch vụ cung cấp API sinh Vector Embedding cho tiếng Việt sử dụng mô hình **AITeamVN/Vietnamese_Embedding** (1024 chiều) trên nền tảng **FastAPI** và thư viện **sentence-transformers**. Dự án được cấu hình tối ưu để chạy trên môi trường CPU-only.

---

## 1. Cấu hình hệ thống (`config.yaml`)

Cấu hình máy chủ và mô hình được quản lý tập trung trong file `config.yaml` tại thư mục gốc:

```yaml
app:
  host: "0.0.0.0"       # 0.0.0.0 cho phép container nhận kết nối từ ngoài vào
  port: 8080             # Cổng dịch vụ lắng nghe
  debug: False          # Chế độ debug của FastAPI

model:
  embedding_name: "AITeamVN/Vietnamese_Embedding" # Mô hình embedding sử dụng
```

---

## 2. Cài đặt và Khởi chạy Cục bộ (Local)

### Bước 1: Thiết lập môi trường ảo
Dự án yêu cầu **Python 3.12+**. Nên sử dụng môi trường ảo để cô lập thư viện:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Bước 2: Cài đặt thư viện phụ thuộc
Để tối ưu dung lượng đĩa và tài nguyên CPU (không sử dụng GPU), cài đặt phiên bản PyTorch CPU-only trước:

```bash
pip install --upgrade pip
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

### Bước 3: Khởi chạy dịch vụ
Chạy lệnh sau tại thư mục gốc của dự án để chạy server:

```bash
python main.py
```
*Dịch vụ sẽ sẵn sàng tại địa chỉ `http://localhost:8080`.*

---

## 3. Triển khai bằng Docker và Docker Compose


* **Khởi chạy ở chế độ chạy ngầm (detatched mode):**
  ```bash
  docker compose up -d
  ```
* **Xem logs hoạt động theo thời gian thực:**
  ```bash
  docker compose logs -f
  ```
* **Dừng và giải phóng tài nguyên:**
  ```bash
  docker compose down
  ```



---

## 4. Danh sách API Endpoints

### A. Kiểm tra trạng thái dịch vụ (Health Check)
* **Endpoint:** `GET /health`
* **Response mẫu (Thành công):**
  ```json
  {
    "status": "ok"
  }
  ```
* **Response mẫu (Lỗi tải mô hình):**
  ```json
  {
    "status": "unhealthy",
    "error": "Embedding service model failed to load"
  }
  ```

### B. Sinh Vector Embedding
* **Endpoint:** `POST /embedding`
* **Request Header:** `Content-Type: application/json`
* **Request Body:** Định dạng JSON đối tượng chứa danh sách chuỗi văn bản:
  ```json
  {
    "texts": [
      "Trí tuệ nhân tạo VPI",
      "Học máy và dữ liệu dầu khí"
    ]
  }
  ```
* **Response mẫu (Thành công):** Trả về mảng các vector embedding, mỗi vector tương ứng có 1024 chiều:
  ```json
  {
    "embedding": [
      [
        -0.010008487850427628,
        0.019622907042503357,
        0.02342621237039566,
        -0.02136118896305561,
        ...
      ],
      [
        -0.0363820381462574,
        0.009401364251971245,
        0.009054536931216717,
        -0.019482621923089027,
        ...
      ]
    ]
  }
  ```

---

## 5. Hướng dẫn Kiểm thử và Gọi API

### Cách 1: Giao diện trực quan Swagger UI
Khi dịch vụ đang chạy, truy cập trực tiếp bằng trình duyệt vào địa chỉ:
```
http://localhost:8080/docs
```
Giao diện Swagger cho phép bạn bấm vào nút **"Try it out"**, nhập trực tiếp JSON request body và kiểm tra kết quả trả về ngay trên Web.

### Cách 2: Sử dụng lệnh `curl` qua Terminal
```bash
curl -X POST http://localhost:8080/embedding \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Thử nghiệm Docker API"]}'
```

### Cách 3: Sử dụng Python `requests`
```python
import requests

url = "http://localhost:8080/embedding"
payload = {
    "texts": [
        "Tôi thích lập trình phần mềm.",
        "Mô hình embedding hoạt động ổn định."
    ]
}

response = requests.post(url, json=payload)
if response.status_code == 200:
    data = response.json()
    embeddings = data["embedding"]
    print(f"Số lượng vector: {len(embeddings)}")
    print(f"Kích thước vector thứ nhất: {len(embeddings[0])} chiều")
else:
    print(f"Lỗi: {response.status_code} - {response.text}")
```
