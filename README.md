# Lập trình Python cơ bản - Lab 01

Dự án này chứa các bài tập thực hành lập trình Python cơ bản thuộc chương trình đào tạo.

## 👤 Thông tin sinh viên
- **Họ tên**: Trần Quốc Vũ
- **MSSV**: 2380614820

## 📂 Cấu trúc thư mục
Dự án được tổ chức thành các thư mục bài tập (Exercise):

```text
lab_01/
├── ex01/               # Bài tập thực hành 01
│   └── hello.py        # Chương trình chào mừng đầu tiên
├── ex02/               # Bài tập thực hành 02
│   ├── ex02_01.py      # Nhập tên, tuổi và in lời chào
│   ├── ex02_02.py      # Tính diện tích hình tròn
│   ├── ex02_03.py      # Kiểm tra số chẵn/lẻ
│   ├── ex02_04.py      # Lọc số chia hết cho 7 nhưng không là bội của 5
│   ├── ex02_05.py      # Tính lương nhân viên (có tăng ca)
│   ├── ex02_06.py      # Tạo mảng 2 chiều i*j
│   ├── ex02_07.py      # Chuyển đổi chuỗi nhập vào thành chữ hoa
│   ├── ex02_08.py      # Kiểm tra số nhị phân chia hết cho 5
│   ├── ex02_09.py      # Kiểm tra số nguyên tố
│   └── ex02_10.py      # Đảo ngược chuỗi
└── ex03/               # Bài tập thực hành 03 (List, Tuple, Dictionary)
    ├── ex03_01.py      # Tính tổng các số chẵn trong List
    ├── ex03_02.py      # Đảo ngược vị trí các phần tử trong List
    ├── ex03_03.py      # Tạo Tuple từ List nhập vào
    ├── ex03_04.py      # Truy cập phần tử đầu và cuối trong Tuple
    ├── ex03_05.py      # Đếm số lần xuất hiện của phần tử và lưu vào Dictionary
    └── ex03_06.py      # Xóa phần tử khỏi Dictionary theo key
```

## 🚀 Hướng dẫn chạy chương trình
Để chạy bất kỳ bài tập nào, hãy sử dụng terminal và lệnh `python` theo cú pháp sau:

```powershell
# Chạy bài tập trong ex01
python lab_01/ex01/hello.py

# Chạy bài tập trong ex02
python lab_01/ex02/ex02_01.py

# Chạy bài tập trong ex03
python lab_01/ex03/ex03_01.py
```

## 📝 Danh sách bài tập (Exercise 02)
1. **Câu 01**: Nhập thông tin cá nhân và in lời chào.
2. **Câu 02**: Tính diện tích hình tròn với bán kính nhập từ bàn phím.
3. **Câu 03**: Kiểm tra tính chẵn lẻ của một số nguyên.
4. **Câu 04**: Tìm các số thỏa mãn điều kiện chia hết cho 7 và không là bội của 5 trong khoảng 2000-3200.
5. **Câu 05**: Chương trình tính lương thực lĩnh dựa trên giờ làm việc (hệ số tăng ca 1.5).
6. **Câu 06**: Xây dựng mảng 2 chiều dựa trên chỉ số hàng và cột.
7. **Câu 07**: Nhập nhiều dòng văn bản và chuyển đổi toàn bộ sang chữ in hoa.
8. **Câu 08**: Lọc các số nhị phân chia hết cho 5 từ một chuỗi đầu vào.
9. **Câu 09**: Kiểm tra một số có phải là số nguyên tố hay không.
10. **Câu 10**: Nhận một chuỗi và trả về chuỗi đảo ngược của nó.

## 📝 Danh sách bài tập (Exercise 03)
1. **Câu 01**: Viết hàm tính tổng tất cả các số chẵn trong một `list` số nguyên.
2. **Câu 02**: Viết chương trình đảo ngược vị trí các phần tử trong một `list`.
3. **Câu 03**: Tạo một `tuple` từ `list` số nguyên nhập vào từ bàn phím.
4. **Câu 04**: Truy cập và in ra phần tử đầu tiên và cuối cùng trong một `tuple`.
5. **Câu 05**: Đếm số lần xuất hiện của mỗi phần tử trong `list` và lưu kết quả vào `dict`.
6. **Câu 06**: Xóa một phần tử khỏi `dict` dựa trên `key` được cho trước.

## 📝 Danh sách bài tập (Lab 02 - Mã Hóa Cơ Bản)
Dự án Lab 02 xây dựng các thuật toán mã hoá và giải mã cơ bản thông qua web service sử dụng **Flask Framework**, đồng thời bổ sung giao diện web demo.

### 📂 Cấu trúc thư mục Lab 02:

```text
lab-02/
├── api.py                          # Flask API cho các thuật toán mã hoá/giải mã
├── app.py                          # Flask Web UI (menu + form thao tác thuật toán)
├── requirements.txt                # Các thư viện phụ thuộc
├── templates/
│   ├── index.html                  # Trang menu chọn thuật toán
│   └── cipher_page.html            # Trang nhập liệu encrypt/decrypt
└── cipher/
    ├── caesar/                     # Bài 1: Thuật toán Caesar
    │   ├── alphabet.py
    │   ├── caesar_cipher.py
    │   └── __init__.py
    ├── vigenere/                   # Bài 2: Thuật toán Vigenere
    │   ├── vigenere_cipher.py
    │   └── __init__.py
    ├── railfence/                  # Bài 3: Thuật toán Rail Fence
    │   ├── railfence_cipher.py
    │   └── __init__.py
    ├── playfair/                   # Bài 4: Thuật toán Playfair
    │   ├── playfair_cipher.py
    │   └── __init__.py
    └── transposition/              # Bài 5: Thuật toán Transposition
        ├── transposition_cipher.py
        └── __init__.py
```

### 🚀 Hướng dẫn chạy ứng dụng Lab 02
Tại thư mục gốc của bài lab:

```powershell
# Di chuyển vào thư mục Lab 02
cd lab-02

# Chạy API server (port 5000)
python api.py

# Chạy Web UI server (port 5050)
python app.py
```

### 🔗 Danh sách API hiện có
Sau khi chạy `python api.py`, có thể sử dụng **Postman** để test:

- `POST /api/caesar/encrypt`
- `POST /api/caesar/decrypt`
- `POST /api/vigenere/encrypt`
- `POST /api/vigenere/decrypt`
- `POST /api/railfence/encrypt`
- `POST /api/railfence/decrypt`
- `POST /api/playfair/creatematrix`
- `POST /api/playfair/encrypt`
- `POST /api/playfair/decrypt`
- `POST /api/transposition/encrypt`
- `POST /api/transposition/decrypt`

### 🌐 Giao diện web demo
Sau khi chạy `python app.py`, truy cập:

- `http://127.0.0.1:5050`

Menu web hiện hỗ trợ các thuật toán:

- Caesar
- Vigenere
- Rail Fence
- Playfair
- Transposition

## 📝 Danh sách bài tập (Lab 03 - Lập Trình Giao Diện Ứng Dụng Bảo Mật)
Dự án Lab 03 xây dựng các ứng dụng desktop demo sử dụng **PyQt5** kết hợp **Flask API** cho các thuật toán mã hoá: Caesar, RSA, ECC.

### 📂 Cấu trúc thư mục Lab 03:

```text
lab-03/
├── api.py                          # Flask API cho RSA và ECC
├── app.py                          # Caesar cipher (local, không dùng API)
├── caesar_cipher.py                # Caesar cipher desktop app (gọi API lab-02)
├── rsa_cipher.py                   # RSA cipher desktop app (gọi API lab-03)
├── ecc_cipher.py                   # ECC cipher desktop app (gọi API lab-03)
├── requirements.txt                # PyQt5, requests, Flask, rsa, ecdsa
├── cipher/
│   ├── __init__.py
│   ├── rsa/
│   │   ├── __init__.py
│   │   ├── rsa_cipher.py           # RSACipher class
│   │   └── keys/                   # Chứa privateKey.pem, publicKey.pem
│   └── ecc/
│       ├── __init__.py
│       ├── ecc_cipher.py           # ECCCipher class
│       └── keys/                   # Chứa privateKey.pem, publicKey.pem
├── platforms/                      # Qt platform plugins
└── ui/
    ├── __init__.py
    ├── caesar.ui / caesar.py       # Giao diện Caesar
    ├── rsa.ui / rsa.py             # Giao diện RSA (layout 2 cột)
    └── ecc.ui / ecc.py             # Giao diện ECC
```

### 🚀 Hướng dẫn chạy ứng dụng Lab 03

```powershell
# Di chuyển vào thư mục Lab 03
cd lab-03

# Cài đặt thư viện
pip install -r requirements.txt

# Bài 3.5.1 - Caesar Cipher (dùng API lab-02, cần chạy lab-02/api.py trước)
python caesar_cipher.py

# Bài 3.5.2 & 3.5.3 - RSA & ECC (chạy API lab-03 trước)
python api.py
python rsa_cipher.py
python ecc_cipher.py
```

### 🔗 Danh sách API Lab 03
Sau khi chạy `python api.py` (port 5000):

**RSA:**
- `GET  /api/rsa/generate_keys`
- `POST /api/rsa/encrypt`
- `POST /api/rsa/decrypt`
- `POST /api/rsa/sign`
- `POST /api/rsa/verify`

**ECC:**
- `GET  /api/ecc/generate_keys`
- `POST /api/ecc/sign`
- `POST /api/ecc/verify`

## 📝 Danh sách bài tập (Lab 04 - Mật Mã Học Ứng Dụng)
Dự án Lab 04 tập trung xây dựng các giao thức truyền tin bảo mật trên nền tảng Socket & WebSocket, đồng thời vươn tới chuẩn mực giao diện hiển thị chuyên nghiệp nhất.
> 👨‍💻 **Thiết kế & Thực hiện bởi: Trần Quốc Vũ - MSSV: 2380614820**

### 📂 Cấu trúc thư mục Lab 04:

```text
lab-04/
├── aes_rsa_socket/                 # Bài 4.6.1 + Điểm cộng UI xuất sắc
│   ├── ui_server.py                # Server giao tiếp giao diện Enterprise (pyqtdarktheme)
│   ├── ui_client.py                # Client đàm thoại giao diện Enterprise
│   └── requirements.txt            
├── dh_key_pair/                    # Bài 4.6.2
│   ├── ui_dh.py                    # Giao diện cỗ máy trao đổi khóa Diffie-Hellman
│   └── requirements.txt
├── hash/                           # Bài 4.6.3
│   ├── ui_hash.py                  # Giao diện băm All-In-One (MD5, SHA-256, BLAKE2...)
│   └── requirements.txt
├── websocket/                      # Bài 4.6.4
│   ├── server.py                   # WebSocket Server (Tornado) cơ bản
│   ├── client.py                   # WebSocket Client (Tornado) cơ bản
│   └── requirements.txt
└── websocket_extended/             # Bài 4.7 - Câu 4 (Bài tập phần nâng cao)
    ├── aes_ws_server.py            # WebSocket Server xử lý tự động mã hóa AES
    ├── aes_ws_client.py            # Console Client đa luồng (Multi-thread async)
    └── requirements.txt
```

### 🚀 Điểm nhấn Kỹ thuật (Phần Cộng Điểm)
- Tích hợp chuẩn giao diện **Enterprise UI (qdarktheme)** cho tất cả các Bài 4.6.1, 4.6.2 và 4.6.3. Giao diện trang bị Shadow, Status Bar, Colorized HTML Logs và bố cục QSplitter Responsive.
- Nâng cấp **Bài tập mở rộng 4.7.4**: Trị triệt để lỗi xung đột Thread của Tornado khi nhập I/O Console (`RuntimeError: There is no current event loop`), hoàn thành trọn vẹn 100% đề bài nâng cao.

 
