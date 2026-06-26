# Tài liệu Đặc tả API - Dịch vụ Vietnamese Embedding

Tài liệu này đặc tả chi tiết các API của Dịch vụ Vietnamese Embedding, bao gồm cấu trúc gói tin (Request/Response), mã trạng thái HTTP, quy tắc kiểm tra dữ liệu và các ví dụ tích hợp.

---

## 1. Thông tin chung (General Information)

* **Giao thức:** HTTP/1.1
* **Định dạng dữ liệu:** JSON (`application/json`)
* **Địa chỉ mặc định:** `http://localhost:8080` (hoặc tên miền riêng nếu chạy qua Cloudflare Tunnel)

---

## 2. Đặc tả các Endpoints

### 2.1. GET `/health` - Kiểm tra trạng thái dịch vụ

Kiểm tra xem mô hình embedding đã được tải thành công và dịch vụ đã sẵn sàng nhận yêu cầu hay chưa.

* **Method:** `GET`
* **Path:** `/health`
* **Authentication:** Không yêu cầu.

#### Phản hồi (Responses):

* **Mã trạng thái 200 (Thành công - Dịch vụ hoạt động tốt):**
  * **Content-Type:** `application/json`
  * **Body:**
    ```json
    {
      "status": "ok"
    }
    ```

* **Mã trạng thái 200 (Lỗi tải mô hình - Mô hình chưa sẵn sàng):**
  * **Content-Type:** `application/json`
  * **Body:**
    ```json
    {
      "status": "unhealthy",
      "error": "Embedding service model failed to load"
    }
    ```

---

### 2.2. POST `/embedding` - Sinh Vector Embedding

Nhận vào danh sách văn bản và trả về các vector biểu diễn tương ứng (mỗi vector có kích thước 1024 chiều).

* **Method:** `POST`
* **Path:** `/embedding`
* **Headers:**
  * `Content-Type: application/json`
* **Authentication:** Không yêu cầu.

#### Yêu cầu (Request Body Schema):

Dữ liệu gửi lên là một đối tượng JSON chứa danh sách các chuỗi văn bản cần xử lý:

| Trường (Field) | Kiểu dữ liệu (Type) | Bắt buộc (Required) | Mô tả (Description) | Quy tắc kiểm tra (Validation) |
| :--- | :--- | :--- | :--- | :--- |
| `texts` | `Array [String]` | **Có** | Danh sách các đoạn văn bản tiếng Việt cần sinh embedding. | Không được rỗng, tối thiểu phải có 1 chuỗi. |

*Ví dụ Request Body:*
```json
{
  "texts": [
    "Tôi yêu Việt Nam",
    "Viện Dầu khí Việt Nam VPI"
  ]
}
```

#### Phản hồi (Responses):

* **Mã trạng thái 200 (Thành công):**
  * **Content-Type:** `application/json`
  * **Body:** Trả về đối tượng JSON chứa mảng 2 chiều của các vector số thực (mỗi vector có độ dài 1024).
    ```json
    {
      "embedding": [
        [
          -0.010008487850427628,
          0.019622907042503357,
          0.02342621237039566,
          -0.02136118896305561,
          ... (còn tiếp 1020 phần tử số thực)
        ],
        [
          -0.0363820381462574,
          0.009401364251971245,
          0.009054536931216717,
          -0.019482621923089027,
          ... (còn tiếp 1020 phần tử số thực)
        ]
      ]
    }
    ```

* **Mã trạng thái 400 (Dữ liệu không hợp lệ):**
  * **Lý do:** Danh sách `texts` gửi lên bị rỗng.
  * **Body:**
    ```json
    {
      "detail": "The input list of texts cannot be empty"
    }
    ```

* **Mã trạng thái 422 (Lỗi định dạng dữ liệu đầu vào):**
  * **Lý do:** Thiếu trường `texts` hoặc kiểu dữ liệu truyền vào sai (ví dụ truyền vào một chuỗi thay vì mảng).
  * **Body (FastAPI Validation Error):**
    ```json
    {
      "detail": [
        {
          "loc": ["body", "texts"],
          "msg": "field required",
          "type": "value_error.missing"
        }
      ]
    }
    ```

* **Mã trạng thái 500 (Lỗi hệ thống hoặc lỗi tải mô hình):**
  * **Lý do:** Lỗi trong quá trình tính toán vector của mô hình.
  * **Body:**
    ```json
    {
      "detail": "Failed to generate embeddings: <chi_tiet_loi>"
    }
    ```

---

## 3. Cấu trúc Lỗi chung (Error Structure)

Tất cả các lỗi mức ứng dụng (400, 422, 500) đều tuân theo chuẩn định dạng lỗi của FastAPI:

```json
{
  "detail": "Thông tin chi tiết về lỗi xảy ra"
}
```

---

## 4. Ví dụ gọi API trên các ngôn ngữ khác nhau

### 4.1. cURL (Terminal)
```bash
curl -X POST http://localhost:8080/embedding \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Kiểm tra API"]}'
```

### 4.2. Python (Sử dụng thư viện `requests`)
```python
import requests

def get_vietnamese_embeddings(sentences: list) -> list:
    url = "http://localhost:8080/embedding"
    headers = {"Content-Type": "application/json"}
    payload = {"texts": sentences}
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["embedding"]
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")

# Thử nghiệm
try:
    vectors = get_vietnamese_embeddings(["Học máy ứng dụng", "Dữ liệu lớn"])
    print(f"Số lượng vector: {len(vectors)}")
    print(f"Số chiều: {len(vectors[0])}")
except Exception as e:
    print(e)
```

### 4.3. JavaScript (Sử dụng `fetch` API)
```javascript
const getEmbeddings = async (texts) => {
  const url = 'http://localhost:8080/embedding';
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ texts })
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP error! status: ${response.status}, details: ${errorText}`);
    }
    
    const data = await response.json();
    return data.embedding;
  } catch (error) {
    console.error('Error fetching embeddings:', error);
  }
};

// Thử nghiệm
getEmbeddings(["Dầu khí Việt Nam", "VPI"])
  .then(vectors => console.log(`Nhận được ${vectors.length} vectors.`));
```
