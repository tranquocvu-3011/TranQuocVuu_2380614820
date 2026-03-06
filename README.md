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
Dự án Lab 02 xây dựng các thuật toán mã hoá và giải mã cơ bản thông qua web service sử dụng **Flask Framework**.

### 📂 Cấu trúc thư mục Lab 02:

```text
lab-02/
├── api.py                    # Server Flask cung cấp API mã hoá và giải mã
├── requirements.txt          # Các thư viện phụ thuộc
└── cipher/
    ├── caesar/               # Bài 1: Thuật toán mã hoá Caesar
    │   ├── alphabet.py
    │   ├── caesar_cipher.py
    │   └── __init__.py
    └── vigenere/             # Bài 2: Thuật toán mã hoá Vigenère
        ├── vigenere_cipher.py
        └── __init__.py
```

### 🚀 Hướng dấn chạy ứng dụng Lab 02
Tại thư mục gốc của bài lab, chạy server Flask bằng dòng lệnh sau:

```powershell
# Di chuyển vào folder Lab 02
cd lab-02

# Chạy server
python api.py
```

Sau khi chạy thành công, có thể sử dụng **Postman** để test các API:
- `POST /api/caesar/encrypt`
- `POST /api/caesar/decrypt`
- `POST /api/vigenere/encrypt`
- `POST /api/vigenere/decrypt`
