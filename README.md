# Lab 03–04: Overloading — Quản lý nhóm dự án và nhân sự

**Sinh viên:** Nguyễn Hải Đăng — **MSSV:** 202418863
**Ngôn ngữ:** Python 3 (chỉ dùng thư viện chuẩn: `typing`, `gc`)

## 1. Yêu cầu môi trường

- Python 3.9 trở lên (dùng type hint `Optional`, `List`; có `from __future__ import
  annotations` để tương thích ngược nếu cần).
- Không cần cài đặt package bên ngoài.

## 2. Cấu trúc thư mục

```
project/
|-- main.py                       # 3 lớp Employee, SoftwareEngineer, ProjectTeam + main() (15 bước)
|-- test_project_management.py    # Kiểm thử biên bằng unittest (17 trường hợp)
+-- README.md
```

## 3. Cách chạy

Chạy kịch bản 15 bước:

```bash
python main.py
```

Chạy toàn bộ kiểm thử biên (17 trường hợp):

```bash
python -m unittest -v
```

## 4. Cách Python mô phỏng "nạp chồng" (overloading)

Python không hỗ trợ nạp chồng constructor/phương thức theo chữ ký (số lượng và
kiểu tham số) như Java/C++ — mỗi tên chỉ có một định nghĩa duy nhất tại một
thời điểm. Đề bài yêu cầu mô phỏng lại các cách gọi đó bằng hai kỹ thuật:

1. **Tham số có giá trị mặc định** — dùng khi các "phiên bản nạp chồng" chỉ
   khác nhau ở việc có truyền thêm tham số phía sau hay không:
   - `Employee(id="UNKNOWN", fullName="Unnamed employee", baseSalary=0)` xử lý
     cả ba cách gọi `Employee()`, `Employee(id, fullName)`,
     `Employee(id, fullName, baseSalary)`.
   - `increaseSalary(value, byPercentage=False)` xử lý cả hai cách gọi
     `increaseSalary(value)` và `increaseSalary(value, byPercentage)`.
   - `addMember(employee, makeLeader=False)` và
     `ProjectTeam(projectCode, projectName, leader=None)` áp dụng tương tự.

2. **`*args` kết hợp kiểm tra số lượng tham số** — dùng khi hai "phiên bản nạp
   chồng" có **số lượng tham số bắt buộc khác nhau và không thể phân biệt bằng
   giá trị mặc định** (constructor của `SoftwareEngineer`):
   - Gọi với đúng 3 tham số → hiểu là
     `SoftwareEngineer(id, fullName, primaryLanguage)`, tự đặt
     `baseSalary = 0`, `technicalAllowance = 0`.
   - Gọi với đúng 5 tham số → hiểu là
     `SoftwareEngineer(id, fullName, baseSalary, primaryLanguage,
     technicalAllowance)`.
   - Số lượng tham số khác 3 hoặc 5 → phát sinh `TypeError` với thông báo rõ
     ràng, không âm thầm chấp nhận dữ liệu sai.

Với đa hình (polymorphism), `calculateMonthlyCost()` và `displayInfo()` được
override trong `SoftwareEngineer`; khi `ProjectTeam` gọi các phương thức này
trên từng phần tử trong danh sách `_members` (kiểu khai báo là `Employee`),
Python tự động gọi đúng phiên bản của lớp con tại runtime — đây chính là cách
"đa hình" thay thế cho phần overloading còn lại của đề (không cần kiểm tra
`isinstance` thủ công khi hiển thị hay tính tổng chi phí).

## 5. Lựa chọn thiết kế cho quan hệ "không sở hữu"

Đề cho phép chọn giữa `weakref.ref` hoặc tham chiếu Python thông thường, miễn
là bảo đảm được bất biến "hủy nhóm không hủy nhân sự". Bài làm này **chọn
tham chiếu Python thông thường** (không dùng `weakref`) để mã nguồn đơn giản,
dễ đọc và dễ đối chiếu kết quả. Bất biến được bảo đảm bằng kỷ luật trong code:

- `ProjectTeam.__del__` **chỉ** làm hai việc: in thông báo hủy, và gán lại
  `self._members = []`, `self._leader = None` để dọn cấu trúc liên kết nội
  bộ của nhóm.
- `ProjectTeam.__del__` **không bao giờ** gọi `del`, `__del__`, hay bất kỳ
  thao tác nào trực tiếp lên từng đối tượng `Employee`.
- Vì Python quản lý bộ nhớ bằng đếm tham chiếu (reference counting), một
  `Employee` chỉ thực sự bị hủy (gọi `__del__`) khi **không còn bất kỳ biến
  hay cấu trúc dữ liệu nào khác tham chiếu tới nó** — kể cả khi `ProjectTeam`
  chứa nó đã bị hủy trước đó. Bước 13–15 trong `main.py` minh họa trực tiếp
  điều này: `team2` bị hủy khi ra khỏi hàm cục bộ, nhưng `e1` (được biến bên
  ngoài giữ tham chiếu) vẫn gọi `displayInfo()` bình thường sau đó.

`__del__` của `SoftwareEngineer` không gọi `super().__del__()` để tránh in
trùng thông báo hủy của lớp cha; mỗi lớp tự in một thông báo riêng đặc trưng
cho loại nhân sự của mình. Cả `Employee.__del__` và
`SoftwareEngineer.__del__` dùng `getattr(..., default)` khi đọc thuộc tính,
để không phát sinh lỗi phụ (`AttributeError`) nếu một constructor bị hủy giữa
chừng do ném ngoại lệ hợp lệ (ví dụ `TypeError` khi gọi `SoftwareEngineer`
với số tham số sai).

## 6. Tóm tắt kết quả dự kiến khi chạy

**`python main.py`** — in tuần tự 15 bước, các điểm cần đối chiếu:

- Bước 1–4: hiển thị đúng thông tin và số liệu lương sau khi tăng (cố định và
  theo phần trăm).
- Bước 6–8: thêm hai thành viên thành công (`True`, `True`), thêm trùng mã
  thất bại (`False`) và số lượng thành viên **không tăng** lên 3.
- Bước 9–10: hiển thị đa hình đúng loại từng nhân sự; tổng chi phí bằng tổng
  `calculateMonthlyCost()` của từng thành viên.
- Bước 11: xóa trưởng nhóm hiện tại bị từ chối (`False`).
- Bước 12: sau khi đổi trưởng nhóm, xóa người cũ thành công (`True`).
- Bước 13: một nhân sự (`e1`) xuất hiện hợp lệ ở cả hai nhóm khác nhau.
- Bước 14–15: thông báo `__del__` của nhóm thứ hai xuất hiện ngay khi hàm cục
  bộ kết thúc; sau đó `e1` vẫn gọi `displayInfo()` thành công, chứng minh
  nhân sự không bị ảnh hưởng bởi việc hủy nhóm. Các thông báo `__del__` còn
  lại (của `se1`, `se2`, `team1`, `e1`, `e2`) xuất hiện ở cuối chương trình khi
  chương trình kết thúc.

**`python -m unittest -v`** — 20 kiểm thử (17 trường hợp bắt buộc theo đề, có
một số được tách thành nhiều test method cho rõ ràng, cộng thêm vài test bổ
trợ) đều `ok`, tổng kết `OK` ở cuối, không có `FAIL` hay `ERROR`. Các nhóm
kiểm thử:

- `TestEmployeeValidation`: dữ liệu rỗng/âm, tăng lương sai, tăng lương đúng
  (cố định + phần trăm), chi phí Employee.
- `TestSoftwareEngineerValidation`: ngôn ngữ rỗng, phụ cấp âm, sai số lượng
  tham số constructor, chi phí SoftwareEngineer.
- `TestProjectTeamInvariants`: trùng mã, constructor có trưởng nhóm, không
  xóa được trưởng nhóm, `changeLeader` tự thêm, trưởng nhóm cũ vẫn là thành
  viên, tổng chi phí nhóm rỗng, chi phí trưởng nhóm tính đúng một lần, một
  nhân sự thuộc nhiều nhóm, hủy nhóm không ảnh hưởng nhân sự còn được tham
  chiếu.
