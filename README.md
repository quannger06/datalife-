# DataLife — bài thử cộng tác theo hướng A

Mỗi người code trên nhánh riêng → mở Pull Request vào `main` → CI tự kiểm thử → bạn xem và bấm Merge → CI chạy lại trên `main`.

Đây là bài thử Python 3.12, chưa phải backend nghiệp vụ hoặc server triển khai. Không cần cài thêm thư viện Python.

## 1. Merge bộ khung trước

Mở PR `setup/integration-test` → `main`. Đợi `Repository configuration check` xanh, xem thay đổi, rồi bấm **Merge pull request → Confirm merge**.

Ở bước này, 9 bài kiểm tra chương trình chạy phải đạt; 1 bài integration của hai tính năng được ghi rõ `skipped` vì thành viên chưa thêm module. Đây chỉ là xác nhận bộ khung, chưa phải hoàn thành bài thử hai người.

## 2. Máy A: thêm Hello World

Mở PowerShell/Terminal tại nơi muốn đặt dự án:

```bash
git clone https://github.com/quannger06/datalife-.git
cd datalife-
git switch -c feature/hello
```

Tạo `features/hello.py`:

```python
def hello():
    return "Hello World"
```

Tạo `tests/test_hello.py` (bắt buộc đi cùng tính năng):

```python
import unittest
from features.hello import hello

class HelloTests(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), "Hello World")
```

Chạy và đẩy code:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python main.py
git add features/hello.py tests/test_hello.py
git commit -m "feat: add hello module and tests"
git push -u origin feature/hello
```

Nếu Windows không nhận `python`, dùng `py -3.12` thay `python`. Nếu chưa có Git/Python, cài trước; hai người cần quyền ghi repository.

## 3. Máy B: thêm Xin chào World

Trên máy B, clone repo tương tự nhưng tạo nhánh `feature/xinchao`.

Tạo `features/xinchao.py` (lưu UTF-8):

```python
def xinchao():
    return "Xin chào World"
```

Tạo `tests/test_xinchao.py`:

```python
import unittest
from features.xinchao import xinchao

class XinChaoTests(unittest.TestCase):
    def test_xinchao(self):
        self.assertEqual(xinchao(), "Xin chào World")
```

Chạy test như máy A, rồi:

```bash
git add features/xinchao.py tests/test_xinchao.py
git commit -m "feat: add xinchao module and tests"
git push -u origin feature/xinchao
```

## 4. Mở PR và kiểm tra lỗi thật

Mỗi người mở PR từ nhánh mình vào `main`. CI sẽ chạy tự động.

Để thử lỗi, trên nhánh `feature/hello` đổi kết quả thành `Hello Word` (thiếu chữ l), commit và push. CI phải đỏ và merge bị chặn. Sau đó sửa lại `Hello World`, commit và push trên cùng nhánh; CI phải xanh.

Bạn xem tab **Files changed**, đặc biệt không chấp nhận việc xóa test hoặc sửa CI để né lỗi. Hướng A hiện yêu cầu PR nhưng `required approvals = 0`; việc review do bạn thực hiện thủ công, không phải GitHub bắt buộc một người thứ hai duyệt.

Merge lần lượt hai PR khi CI xanh. Vì ruleset yêu cầu cập nhật với `main`, sau PR thứ nhất, người thứ hai chạy:

```bash
git fetch origin
git merge origin/main
python -m unittest discover -s tests -p "test_*.py" -v
git push
```

Nếu có conflict, giải quyết rồi commit; không force push vào `main`. Chờ CI chạy lại rồi mới merge PR thứ hai.

## 5. Xác nhận hoàn tất

```bash
git switch main
git pull --ff-only origin main
python -m unittest discover -s tests -p "test_*.py" -v
python main.py --require-all
```

Kết quả cuối: **12 tests đạt, không có skipped**, và hai dòng:

```text
Hello World
Xin chào World
```

Mở **Actions → Backend CI → lần chạy trên main → Repository configuration check → Run combined program** để đối chiếu. Unit test của từng tính năng import trực tiếp: xóa module sau khi tích hợp sẽ làm CI lỗi.

## 6. Chuyển sang backend thật

Giữ quy trình branch/PR và required check. Chốt framework, API contract, database/migrations, dependency lock, cách chạy và môi trường triển khai trước khi chia tính năng. Thay bài demo bằng test thật (API, nghiệp vụ, database, tích hợp), cập nhật lệnh CI theo framework. Giữ tên check `Repository configuration check` trừ khi cập nhật ruleset tương ứng.

CI chỉ bảo đảm các kiểm tra được viết; bài Hello World không chứng minh backend thật đã hoàn chỉnh. Deploy cần cấu hình riêng sau này. Không đưa `.env`, khóa API hay dữ liệu riêng tư lên repo công khai.
