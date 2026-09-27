"""
/********************
Ma sinh vien: 202418863
Ho ten: Nguyen Hai Dang
********************/

Lab 03-04: Overloading - Quan ly nhom du an va nhan su.

File nay chua ba lop bat buoc (Employee, SoftwareEngineer, ProjectTeam) va
ham main() thuc hien kich ban kiem thu 15 buoc theo de bai.

Ghi chu thiet ke:
- Python khong ho tro nap chong constructor/phuong thuc theo chu ky nhu Java/C++.
  Moi truong hop nap chong trong de duoc mo phong bang:
    (1) tham so co gia tri mac dinh (Employee.__init__, increaseSalary, ...)
    (2) *args ket hop kiem tra so luong tham so (SoftwareEngineer.__init__)
- Quan he "khong so huu" giua ProjectTeam va cac Employee duoc trien khai
  bang tham chieu Python thong thuong (khong dung weakref) de don gian hoa
  code. De bao dam bat bien "huy nhom khong huy nhan su", __del__ cua
  ProjectTeam CHI xoa cac danh sach/tham chieu noi bo (self._members,
  self._leader) chu khong goi bat ky thao tac nao len tung doi tuong
  Employee. Vi Python dung dem tham chieu, mot Employee van song neu con
  bien ben ngoai tro toi no, du ProjectTeam chua no da bi huy.
"""

from __future__ import annotations

import gc
from typing import List, Optional


class Employee:
    """Nhan su thong thuong trong don vi.

    Bat bien:
        - id khong rong/chi chua khoang trang, va la thuoc tinh chi doc.
        - fullName khong rong/chi chua khoang trang.
        - baseSalary khong am.
    """

    def __init__(
        self,
        id: str = "UNKNOWN",
        fullName: str = "Unnamed employee",
        baseSalary: float = 0,
    ) -> None:
        """Constructor duy nhat mo phong ba cach goi cua de bai:

        Employee()
        Employee(id, fullName)
        Employee(id, fullName, baseSalary)
        """
        if not isinstance(id, str) or id.strip() == "":
            raise ValueError("id khong duoc rong hoac chi chua khoang trang")
        if not isinstance(fullName, str) or fullName.strip() == "":
            raise ValueError("fullName khong duoc rong hoac chi chua khoang trang")
        if baseSalary < 0:
            raise ValueError("baseSalary khong duoc am")

        self._id = id
        self._full_name = fullName
        self._base_salary = float(baseSalary)

    @property
    def id(self) -> str:
        """Ma nhan su - chi doc de bao toan tinh duy nhat trong nhom."""
        return self._id

    @property
    def fullName(self) -> str:
        """Ho ten nhan su."""
        return self._full_name

    @property
    def baseSalary(self) -> float:
        """Luong co ban hien tai."""
        return self._base_salary

    def increaseSalary(self, value: float, byPercentage: bool = False) -> None:
        """Tang luong, mo phong hai phien ban nap chong:

        increaseSalary(value)
        increaseSalary(value, byPercentage)

        value phai > 0, neu khong phat sinh ValueError va giu nguyen luong.
        """
        if value <= 0:
            raise ValueError("Gia tri tang luong phai lon hon 0")

        if byPercentage:
            self._base_salary = self._base_salary * (1 + value / 100)
        else:
            self._base_salary = self._base_salary + value

    def calculateMonthlyCost(self) -> float:
        """Chi phi hang thang cua nhan su thong thuong = luong co ban."""
        return self._base_salary

    def displayInfo(self) -> None:
        """Hien thi day du thong tin nhan su."""
        print(
            f"[Employee] Ma: {self._id} | Ho ten: {self._full_name} | "
            f"Luong co ban: {self._base_salary:,.0f} | "
            f"Chi phi thang: {self.calculateMonthlyCost():,.0f}"
        )

    def __del__(self) -> None:
        # In thong bao de quan sat vong doi doi tuong Employee. Dung getattr
        # de tranh AttributeError neu constructor bi loi truoc khi gan xong
        # cac thuoc tinh (vi du SoftwareEngineer nem TypeError qua som).
        id_value = getattr(self, "_id", "UNKNOWN")
        name_value = getattr(self, "_full_name", "Unnamed employee")
        print(f"[__del__] Nhan su {id_value} - {name_value} bi huy.")


class SoftwareEngineer(Employee):
    """Ky su phan mem: ke thua Employee, bo sung ngon ngu chinh va phu cap.

    Bat bien bo sung:
        - primaryLanguage khong rong.
        - technicalAllowance khong am.
    """

    def __init__(self, *args) -> None:
        """Mo phong hai cach goi constructor bang *args + kiem tra so luong:

        SoftwareEngineer(id, fullName, primaryLanguage)
        SoftwareEngineer(id, fullName, baseSalary, primaryLanguage, technicalAllowance)
        """
        if len(args) == 3:
            id, fullName, primaryLanguage = args
            baseSalary = 0
            technicalAllowance = 0
        elif len(args) == 5:
            id, fullName, baseSalary, primaryLanguage, technicalAllowance = args
        else:
            raise TypeError(
                "SoftwareEngineer chi nhan 3 tham so (id, fullName, "
                "primaryLanguage) hoac 5 tham so (id, fullName, baseSalary, "
                f"primaryLanguage, technicalAllowance); nhan duoc {len(args)}."
            )

        super().__init__(id, fullName, baseSalary)

        if not isinstance(primaryLanguage, str) or primaryLanguage.strip() == "":
            raise ValueError("primaryLanguage khong duoc rong")
        if technicalAllowance < 0:
            raise ValueError("technicalAllowance khong duoc am")

        self._primary_language = primaryLanguage
        self._technical_allowance = float(technicalAllowance)

    @property
    def primaryLanguage(self) -> str:
        """Ngon ngu lap trinh chinh cua ky su."""
        return self._primary_language

    @property
    def technicalAllowance(self) -> float:
        """Phu cap ky thuat."""
        return self._technical_allowance

    def calculateMonthlyCost(self) -> float:
        """Chi phi hang thang cua ky su = luong co ban + phu cap ky thuat."""
        return self._base_salary + self._technical_allowance

    def displayInfo(self) -> None:
        """Hien thi thong tin ky su, bao gom ngon ngu chinh va phu cap."""
        print(
            f"[SoftwareEngineer] Ma: {self._id} | Ho ten: {self._full_name} | "
            f"Luong co ban: {self._base_salary:,.0f} | "
            f"Ngon ngu chinh: {self._primary_language} | "
            f"Phu cap ky thuat: {self._technical_allowance:,.0f} | "
            f"Chi phi thang: {self.calculateMonthlyCost():,.0f}"
        )

    def __del__(self) -> None:
        # Thong bao rieng cho ky su phan mem (khong goi super().__del__()
        # de tranh in trung lap thong bao cua lop cha). Dung getattr de
        # tranh AttributeError neu constructor nem TypeError truoc khi
        # cac thuoc tinh duoc gan xong.
        id_value = getattr(self, "_id", "UNKNOWN")
        name_value = getattr(self, "_full_name", "Unnamed employee")
        print(f"[__del__] Ky su phan mem {id_value} - {name_value} bi huy.")


class ProjectTeam:
    """Nhom du an: chua tham chieu KHONG SO HUU den truong nhom va thanh vien.

    Bat bien:
        - projectCode, projectName khong rong.
        - Khong co hai thanh vien cung ma trong nhom.
        - Neu co truong nhom thi truong nhom phai thuoc danh sach thanh vien.
        - Khong xoa duoc truong nhom hien tai khi chua chon nguoi thay the.
    """

    def __init__(
        self,
        projectCode: str,
        projectName: str,
        leader: Optional[Employee] = None,
    ) -> None:
        """Mo phong hai cach goi constructor:

        ProjectTeam(projectCode, projectName)
        ProjectTeam(projectCode, projectName, leader)
        """
        if not isinstance(projectCode, str) or projectCode.strip() == "":
            raise ValueError("projectCode khong duoc rong")
        if not isinstance(projectName, str) or projectName.strip() == "":
            raise ValueError("projectName khong duoc rong")

        self._project_code = projectCode
        self._project_name = projectName
        self._members: List[Employee] = []
        self._leader: Optional[Employee] = None

        if leader is not None:
            # addMember dam bao truong nhom duoc dua vao danh sach thanh
            # vien dung mot lan va duoc dat lam truong nhom.
            self.addMember(leader, True)

    @property
    def projectCode(self) -> str:
        """Ma du an."""
        return self._project_code

    @property
    def projectName(self) -> str:
        """Ten du an."""
        return self._project_name

    def addMember(self, employee: Employee, makeLeader: bool = False) -> bool:
        """Them thanh vien, mo phong hai cach goi:

        addMember(employee)
        addMember(employee, makeLeader)

        Tra ve False neu da co thanh vien cung ma (khong thay doi danh sach).
        Tra ve True neu them thanh cong.
        """
        if not isinstance(employee, Employee):
            raise TypeError("employee phai la doi tuong Employee hoac lop con")

        if self.contains(employee.id):
            return False

        self._members.append(employee)
        if makeLeader:
            self._leader = employee
        return True

    def contains(self, employeeId: str) -> bool:
        """Kiem tra nhom co thanh vien cung ma employeeId hay khong."""
        return any(member.id == employeeId for member in self._members)

    def removeMember(self, employeeId: str) -> bool:
        """Xoa thanh vien theo ma.

        Tra ve False neu khong tim thay hoac neu do la truong nhom hien tai.
        Tra ve True khi xoa thanh cong.
        """
        if self._leader is not None and self._leader.id == employeeId:
            return False

        for index, member in enumerate(self._members):
            if member.id == employeeId:
                del self._members[index]
                return True
        return False

    def changeLeader(self, employee: Employee) -> None:
        """Dat employee lam truong nhom.

        Neu employee chua thuoc nhom thi tu dong them truoc khi cap nhat.
        Truong nhom cu van la thanh vien sau khi doi.
        """
        if not isinstance(employee, Employee):
            raise TypeError("employee phai la doi tuong Employee hoac lop con")

        if not self.contains(employee.id):
            self.addMember(employee)
        self._leader = employee

    def calculateTotalMonthlyCost(self) -> float:
        """Tong chi phi hang thang, goi da hinh calculateMonthlyCost() tren
        tung thanh vien, moi nguoi tinh dung mot lan. Nhom rong -> 0."""
        return sum(member.calculateMonthlyCost() for member in self._members)

    def displayTeam(self) -> None:
        """Hien thi ma, ten du an, truong nhom va toan bo thanh vien
        (goi displayInfo() theo kieu da hinh)."""
        print(f"--- Nhom du an: {self._project_code} - {self._project_name} ---")
        if self._leader is not None:
            print("Truong nhom:")
            self._leader.displayInfo()
        else:
            print("Truong nhom: (chua co)")

        print(f"Danh sach thanh vien ({len(self._members)}):")
        if not self._members:
            print("  (khong co thanh vien)")
        for member in self._members:
            member.displayInfo()

    def __del__(self) -> None:
        # Chi don cau truc lien ket noi bo cua nhom, TUYET DOI khong huy
        # cac doi tuong Employee ma nhom dang tham chieu toi.
        print(
            f"[__del__] Nhom du an {self._project_code} - "
            f"{self._project_name} bi huy (khong anh huong toi cac nhan su)."
        )
        self._members = []
        self._leader = None


def main() -> None:
    """Kich ban kiem thu 15 buoc theo dung thu tu trong de bai."""

    print("===== Buoc 1: Tao hai Employee bang hai cach goi constructor =====")
    e1 = Employee("E001", "Nguyen An", 12_000_000)
    e2 = Employee("E002", "Tran Binh")  # dung baseSalary mac dinh = 0
    e1.displayInfo()
    e2.displayInfo()

    print("\n===== Buoc 2: Tao hai SoftwareEngineer bang hai cach goi constructor =====")
    se1 = SoftwareEngineer("SE001", "Le Chi", 18_000_000, "Python", 3_000_000)
    se2 = SoftwareEngineer("SE002", "Pham Dung", "Java")  # dang 3 tham so
    se1.displayInfo()
    se2.displayInfo()

    print("\n===== Buoc 3: Tang luong e2 bang so tien co dinh (2,000,000) =====")
    e2.increaseSalary(2_000_000)
    e2.displayInfo()

    print("\n===== Buoc 4: Tang luong se2 theo phan tram (10%) =====")
    se2.increaseSalary(10, True)
    se2.displayInfo()

    print("\n===== Buoc 5: Tao nhom du an khong co truong nhom =====")
    team1 = ProjectTeam("PRJ001", "He thong quan ly nhan su")
    team1.displayTeam()

    print("\n===== Buoc 6: Them e1 bang addMember(employee) =====")
    result6 = team1.addMember(e1)
    print(f"Ket qua them e1: {result6}")

    print("\n===== Buoc 7: Them se1 bang addMember(employee, True) lam truong nhom =====")
    result7 = team1.addMember(se1, True)
    print(f"Ket qua them se1 lam truong nhom: {result7}")

    print("\n===== Buoc 8: Thu them lai e1 (da ton tai) =====")
    result8 = team1.addMember(e1)
    print(f"Ket qua them lai e1: {result8} (ky vong False)")
    print(f"So luong thanh vien hien tai: {len(team1._members)} (ky vong 2, khong nhan doi)")

    print("\n===== Buoc 9: Hien thi danh sach bang loi goi da hinh =====")
    team1.displayTeam()

    print("\n===== Buoc 10: Tinh va in tong chi phi nhan su hang thang =====")
    total_cost = team1.calculateTotalMonthlyCost()
    print(f"Tong chi phi hang thang cua team1: {total_cost:,.0f}")

    print("\n===== Buoc 11: Thu xoa truong nhom hien tai (se1) =====")
    result11 = team1.removeMember("SE001")
    print(f"Ket qua xoa truong nhom hien tai: {result11} (ky vong False, bi tu choi)")

    print("\n===== Buoc 12: Doi truong nhom thanh e1, sau do xoa se1 =====")
    team1.changeLeader(e1)
    print("Da doi truong nhom thanh e1.")
    result12 = team1.removeMember("SE001")
    print(f"Ket qua xoa se1 (khong con la truong nhom): {result12} (ky vong True)")
    team1.displayTeam()

    print("\n===== Buoc 13: Tao nhom thu hai, them e1 (da co o nhom 1) =====")

    def create_and_use_team2() -> None:
        team2 = ProjectTeam("PRJ002", "Du an di dong", e2)
        result13 = team2.addMember(e1)
        print(f"Ket qua them e1 vao team2: {result13} (ky vong True, e1 thuoc 2 nhom)")
        team2.displayTeam()

        print("\n===== Buoc 14: Huy nhom thu hai (ket thuc pham vi ham cuc bo) =====")
        # team2 se bi huy khi ra khoi ham nay (het pham vi), minh hoa bang
        # gc.collect() ngay ben ngoai ham.

    create_and_use_team2()
    gc.collect()  # chi de minh hoa thong bao __del__ duoc goi ngay lap tuc

    print("\n===== Buoc 15: Chung minh e1 van ton tai sau khi team2 bi huy =====")
    print("Goi lai displayInfo() cua e1 (van con hop le):")
    e1.displayInfo()


if __name__ == "__main__":
    main()
