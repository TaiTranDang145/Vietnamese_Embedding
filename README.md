# Vietnamese Embedding Service (Hướng dẫn chạy trên macOS)

Dịch vụ sinh Vector Embedding cho tiếng Việt sử dụng mô hình **AITeamVN/Vietnamese_Embedding** (1024 chiều) được tối ưu hóa trên nền tảng **FastAPI** và **sentence-transformers**. 

Tài liệu này hướng dẫn chi tiết cách cài đặt, chạy cục bộ (hỗ trợ tăng tốc phần cứng Apple Silicon) và chạy bằng Docker trên hệ điều hành **macOS**.

---

## 1. Cài đặt Cục bộ trên macOS (Local Development)

### Yêu cầu hệ thống
* Hệ điều hành: macOS Monterey trở lên.
* Trình thông dịch: **Python 3.12** (Khuyên dùng).
* Hỗ trợ chip: Cả Intel Mac và Apple Silicon (M1/M2/M3/M4).

### Bước 1: Khởi tạo Môi trường ảo (Virtual Environment)
Mở Terminal tại thư mục dự án và chạy:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Bước 2: Cài đặt thư viện (Tối ưu cho macOS)
Trên macOS, thay vì cài đặt bản PyTorch CPU-only như Linux, bạn nên cài đặt bản PyTorch mặc định để có thể tận dụng **MPS (Metal Performance Shaders)** giúp tăng tốc sinh embedding bằng GPU của chip Apple Silicon (M1/M2/M3/M4):

```bash
# Nâng cấp pip
pip install --upgrade pip

# Cài đặt PyTorch hỗ trợ tăng tốc MPS trên Apple Silicon
pip install torch

# Cài đặt các thư viện phụ thuộc còn lại
pip install -r requirements.txt
```

### Bước 3: Khởi chạy Dịch vụ
Khởi động FastAPI server bằng lệnh:

```bash
python main.py
```
Ứng dụng sẽ tự động phát hiện phần cứng (MPS hoặc CPU) để khởi chạy. Cổng dịch vụ mặc định là `8080`.

---

## 2. Triển khai bằng Docker trên macOS

Để chạy Docker trên Mac, bạn cần cài đặt trước phần mềm **Docker Desktop cho Mac**.

### Cách 1: Sử dụng Docker Compose (Khuyên dùng)
Docker Desktop trên macOS tự động biên dịch và ảo hóa môi trường rất mượt mà.

* **Khởi chạy container ở chế độ chạy ngầm:**
  ```bash
  docker compose up -d
  ```
* **Xem logs hoạt động thời gian thực:**
  ```bash
  docker compose logs -f
  ```
* **Dừng dịch vụ:**
  ```bash
  docker compose down
  ```


## 3. Các API Endpoints Chính

### A. Health Check
* **Method:** `GET`
* **URL:** `http://localhost:8080/health`
* **Response:** `{"status": "ok"}`

### B. Sinh Vector Embedding
* **Method:** `POST`
* **URL:** `http://localhost:8080/embedding`
* **Headers:** `Content-Type: application/json`
* **Body:**
  ```json
  {
    "texts": [
      "Trí tuệ nhân tạo VPI",
      "Học máy và dữ liệu dầu khí"
    ]
  }
  ```
* **Response:** Trả về đối tượng JSON chứa danh sách vector embedding 1024 chiều.

---

## 4. Kiểm thử dịch vụ nhanh

### Gọi API bằng `curl` qua Terminal của Mac:
```bash
curl -X POST http://localhost:8080/embedding \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Thử nghiệm trên máy Mac"]}'
```

### Sử dụng trình duyệt (Swagger UI):
Truy cập trực tiếp đường dẫn sau để thử nghiệm tương tác:
[http://localhost:8080/docs](http://localhost:8080/docs)
