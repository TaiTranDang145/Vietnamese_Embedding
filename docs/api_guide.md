# Tài liệu Hướng dẫn API Dịch vụ Vietnamese Embedding

Dịch vụ cung cấp API sinh Vector Embedding cho tiếng Việt sử dụng mô hình `AITeamVN/Vietnamese_Embedding` dựa trên thư viện `sentence-transformers` và framework `FastAPI`.

## 1. Cài đặt và Khởi chạy

### Thiết lập môi trường
Dịch vụ chạy trên môi trường ảo Python 3.12+ (hỗ trợ CPU-only để tối ưu hóa tài nguyên).
1. Khởi tạo môi trường ảo:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install --upgrade pip
   pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
   pip install -r requirements.txt
   ```

### Cấu hình ứng dụng (`config.yaml`)
Cấu hình máy chủ và model được quản lý tập trung tại `config.yaml`:
```yaml
app:
  host: "0.0.0.0"
  port: 8080
  debug: False

model:
  embedding_name: "AITeamVN/Vietnamese_Embedding"
```

### Khởi chạy dịch vụ
Chạy lệnh sau tại thư mục gốc của dự án:
```bash
.venv/bin/python main.py
```

---

## 2. Các Endpoint API

### A. Health Check (Kiểm tra trạng thái)
* **Endpoint:** `GET /health`
* **Response mẫu (Thành công):**
  ```json
  {
    "status": "ok"
  }
  ```
* **Response mẫu (Lỗi tải model):**
  ```json
  {
    "status": "unhealthy",
    "error": "Embedding service model failed to load"
  }
  ```

### B. Sinh Vector Embedding
* **Endpoint:** `POST /embedding`
* **Request Header:** `Content-Type: application/json`
* **Request Body:** Định dạng JSON với khóa `texts` chứa danh sách các chuỗi văn bản cần sinh embedding:
  ```json
  {
    "texts": [
      "Xin chào Việt Nam",
      "Trí tuệ nhân tạo VPI"
    ]
  }
  ```
* **Response mẫu:** Trả về một đối tượng chứa mảng các vector embedding (mỗi vector có 1024 chiều đối với model `Vietnamese_Embedding`):
  ```json
  {
    "embedding": [
      [
        -0.0062032840214669704,
        0.013154271990060806,
        -0.03679169341921806,
        ...
      ],
      [
        -0.0819053053855896,
        -0.016337424516677856,
        -0.003705478273332119,
        ...
      ]
    ]
  }
  ```

---

## 3. Chạy bằng Docker

Dịch vụ đã được bọc hoàn toàn bằng Docker để chạy độc lập và ổn định trên cổng 8080.

### Xây dựng Docker Image
```bash
docker build -t vpi-embedding-service .
```
*Lưu ý: Quá trình build sẽ tự động tải trước model `AITeamVN/Vietnamese_Embedding` và lưu vào cache của image. Điều này giúp container khởi động tức thì và có thể chạy offline hoàn toàn.*

### Khởi chạy Docker Container
Chạy container và ánh xạ (map) cổng `8080` ra ngoài máy host:
```bash
docker run -d --name vpi-embedding-app -p 8080:8080 vpi-embedding-service
```

### Kiểm tra logs hoạt động
```bash
docker logs vpi-embedding-app
```
