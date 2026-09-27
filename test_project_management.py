"""
/********************
Ma sinh vien: 202418863
Ho ten: Nguyen Hai Dang
********************/

Kiem thu bien cho Lab 03-04: Overloading (Employee, SoftwareEngineer,
ProjectTeam). Chay bang: python -m unittest -v
"""

import unittest

from main import Employee, ProjectTeam, SoftwareEngineer


class TestEmployeeValidation(unittest.TestCase):
    """Kiem thu cac bat bien va validation cua Employee."""

    def test_empty_or_whitespace_id_raises_value_error(self):
        with self.assertRaises(ValueError):
            Employee("   ", "Nguyen Van A", 1_000_000)

    def test_empty_or_whitespace_full_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            Employee("E010", "   ", 1_000_000)

    def test_negative_base_salary_raises_value_error(self):
        with self.assertRaises(ValueError):
            Employee("E011", "Nguyen Van B", -500_000)

    def test_increase_salary_with_zero_or_negative_raises_value_error(self):
        emp = Employee("E012", "Nguyen Van C", 5_000_000)
        with self.assertRaises(ValueError):
            emp.increaseSalary(0)
        with self.assertRaises(ValueError):
            emp.increaseSalary(-100_000, True)
        # Luong phai giu nguyen sau khi tang loi.
        self.assertEqual(emp.baseSalary, 5_000_000)

    def test_increase_salary_by_fixed_amount(self):
        emp = Employee("E013", "Nguyen Van D", 5_000_000)
        emp.increaseSalary(1_000_000)
        self.assertEqual(emp.baseSalary, 6_000_000)

    def test_increase_salary_by_percentage(self):
        emp = Employee("E014", "Nguyen Van E", 5_000_000)
        emp.increaseSalary(10, True)
        self.assertAlmostEqual(emp.baseSalary, 5_500_000)

    def test_employee_monthly_cost_equals_base_salary_only(self):
        emp = Employee("E015", "Nguyen Van F", 7_000_000)
        self.assertEqual(emp.calculateMonthlyCost(), 7_000_000)


class TestSoftwareEngineerValidation(unittest.TestCase):
    """Kiem thu cac bat bien va validation cua SoftwareEngineer."""

    def test_empty_primary_language_raises_value_error(self):
        with self.assertRaises(ValueError):
            SoftwareEngineer("SE010", "Nguyen Van G", "   ")

    def test_negative_technical_allowance_raises_value_error(self):
        with self.assertRaises(ValueError):
            SoftwareEngineer(
                "SE011", "Nguyen Van H", 10_000_000, "C++", -200_000
            )

    def test_invalid_argument_count_raises_type_error(self):
        with self.assertRaises(TypeError):
            SoftwareEngineer("SE012", "Nguyen Van I")  # chi 2 tham so

    def test_engineer_monthly_cost_equals_salary_plus_allowance(self):
        eng = SoftwareEngineer(
            "SE013", "Nguyen Van K", 15_000_000, "Go", 2_500_000
        )
        self.assertEqual(eng.calculateMonthlyCost(), 17_500_000)


class TestProjectTeamInvariants(unittest.TestCase):
    """Kiem thu cac bat bien va nghiep vu cua ProjectTeam."""

    def setUp(self):
        # Tao du lieu nhan su moi cho tung test de tranh anh huong chung __del__.
        self.emp_a = Employee("A001", "Thanh vien A", 8_000_000)
        self.emp_b = Employee("A002", "Thanh vien B", 9_000_000)
        self.emp_c = SoftwareEngineer(
            "A003", "Thanh vien C", 12_000_000, "Rust", 1_000_000
        )

    def test_duplicate_id_from_different_objects_not_allowed_in_same_team(self):
        team = ProjectTeam("T001", "Du an test")
        self.assertTrue(team.addMember(self.emp_a))
        duplicate_object = Employee("A001", "Ban sao trung ma", 1_000_000)
        # Doi tuong khac nhung trung ma -> khong duoc them.
        self.assertFalse(team.addMember(duplicate_object))
        # Chi co dung 1 thanh vien mang ma A001 trong nhom.
        count_a001 = sum(1 for m in team._members if m.id == "A001")
        self.assertEqual(count_a001, 1)

    def test_constructor_with_leader_adds_leader_exactly_once(self):
        team = ProjectTeam("T002", "Du an co truong nhom", self.emp_a)
        self.assertEqual(len(team._members), 1)
        self.assertIs(team._leader, self.emp_a)
        self.assertTrue(team.contains("A001"))

    def test_cannot_remove_current_leader(self):
        team = ProjectTeam("T003", "Du an", self.emp_a)
        result = team.removeMember("A001")
        self.assertFalse(result)
        self.assertTrue(team.contains("A001"))

    def test_change_leader_auto_adds_employee_not_yet_in_team(self):
        team = ProjectTeam("T004", "Du an")
        self.assertFalse(team.contains("A002"))
        team.changeLeader(self.emp_b)
        self.assertTrue(team.contains("A002"))
        self.assertIs(team._leader, self.emp_b)

    def test_old_leader_remains_member_after_changing_leader(self):
        team = ProjectTeam("T005", "Du an", self.emp_a)
        team.changeLeader(self.emp_b)
        self.assertTrue(team.contains("A001"))
        self.assertTrue(team.contains("A002"))
        self.assertIs(team._leader, self.emp_b)

    def test_empty_team_total_cost_is_zero(self):
        team = ProjectTeam("T006", "Du an rong")
        self.assertEqual(team.calculateTotalMonthlyCost(), 0)

    def test_leader_cost_counted_exactly_once(self):
        team = ProjectTeam("T007", "Du an", self.emp_a)
        team.addMember(self.emp_b)
        expected = self.emp_a.calculateMonthlyCost() + self.emp_b.calculateMonthlyCost()
        self.assertEqual(team.calculateTotalMonthlyCost(), expected)

    def test_same_employee_can_belong_to_two_different_teams(self):
        team1 = ProjectTeam("T008", "Du an mot")
        team2 = ProjectTeam("T009", "Du an hai")
        self.assertTrue(team1.addMember(self.emp_c))
        self.assertTrue(team2.addMember(self.emp_c))
        self.assertTrue(team1.contains("A003"))
        self.assertTrue(team2.contains("A003"))

    def test_destroying_team_does_not_destroy_employee_still_referenced(self):
        def build_temp_team():
            temp_team = ProjectTeam("T010", "Du an tam thoi", self.emp_a)
            self.assertTrue(temp_team.contains("A001"))

        build_temp_team()
        # emp_a van con duoc bien self.emp_a tham chieu, phai con hop le.
        self.assertEqual(self.emp_a.id, "A001")
        # Khong nem ngoai le khi goi lai phuong thuc cua emp_a.
        try:
            self.emp_a.displayInfo()
        except Exception as exc:  # pragma: no cover - chi de bao ve test
            self.fail(f"emp_a khong con hop le sau khi nhom bi huy: {exc}")


if __name__ == "__main__":
    unittest.main()
