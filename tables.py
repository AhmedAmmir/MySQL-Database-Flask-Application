from typing import Optional
from sqlalchemy import DECIMAL, String, Table, Column, ForeignKey, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Faculty(Base):

    __tablename__ = 'Faculty_T'

    faculty_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    faculty_title: Mapped[str] = mapped_column(String(50))
    
    def __init__(self, id: int, title: str) -> None:
        self.faculty_id = id
        self.faculty_title = title
    
    def __repr__(self) -> str:
        return f"<Faculty(faculty_id={self.faculty_id}, faculty_title='{self.faculty_title}')>"


class Department(Base):

    __tablename__ = 'Department_T'

    department_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    department_title: Mapped[str] = mapped_column(String(50))
    department_faculty_id: Mapped[int] = mapped_column(ForeignKey("Faculty_T.faculty_id"))

    department_faculty: Mapped["Faculty"] = relationship()

    def __init__(self, id: int, title: str, faculty_id: int) -> None:
        self.department_id = id
        self.department_title = title
        self.department_faculty_id = faculty_id

    def __repr__(self) -> str:
        return f"<Department(department_id={self.department_id}, department_title='{self.department_title}', department_faculty_id={self.department_faculty_id})>"


class Title(Base):

    __tablename__ = 'Title_T'

    title_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title_description: Mapped[str] = mapped_column(String(25))

    def __init__(self, id: int, description: str) -> None:
        self.title_id = id
        self.title_description = description

    def __repr__(self) -> str:
        return f"<Title(title_id={self.title_id}, title_description='{self.title_description}')>"


class TeachingStaff(Base):

    __tablename__ = 'Teaching_Staff_T'
    
    teaching_staff_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    teaching_staff_first_name: Mapped[str] = mapped_column(String(15))
    teaching_staff_middle_name: Mapped[Optional[str]] = mapped_column(String(15))
    teaching_staff_last_name: Mapped[str] = mapped_column(String(15))
    teaching_staff_email: Mapped[str] = mapped_column(String(50))
    teaching_staff_title_id: Mapped[int] = mapped_column(ForeignKey("Title_T.title_id"))
    teaching_staff_department_id: Mapped[int] = mapped_column(ForeignKey("Department_T.department_id"))

    teaching_staff_title: Mapped["Title"] = relationship()
    teaching_staff_department_id: Mapped["Department"] = relationship()

    def __init__(self, id: int, firstName: str, middleName: str, lastName: str, email: str, titleID: int, departmentID: int) -> None:
        self.teaching_staff_id = id
        self.teaching_staff_first_name = firstName
        self.teaching_staff_middle_name = middleName
        self.teaching_staff_last_name = lastName
        self.teaching_staff_email = email
        self.teaching_staff_title_id = titleID
        self.teaching_staff_department_id = departmentID
        
    def __repr__(self) -> str:
        return f"<TeachingStaff(teaching_staff_id={self.teaching_staff_id}, teaching_staff_first_name='{self.teaching_staff_first_name}', teaching_staff_middle_name='{self.teaching_staff_middle_name}', teaching_staff_last_name='{self.teaching_staff_last_name}', teaching_staff_email='{self.teaching_staff_email}', teaching_staff_title_id={self.teaching_staff_title_id}, teaching_staff_department_id={self.teaching_staff_department_id})>"
    

class Course(Base):

    __tablename__ = 'Course_T'

    course_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course_code: Mapped[str] = mapped_column(String(8))
    course_title: Mapped[str] = mapped_column(String(45))
    course_credits: Mapped[int] = mapped_column()
    course_teaching_staff_id: Mapped[int] = mapped_column(ForeignKey("Teaching_Staff_T.teaching_staff_id"))

    course_teaching_staff: Mapped["TeachingStaff"] = relationship()
    course_student_list: Mapped[list["Student_Course"]] = relationship(back_populates="student")

    def __init__(self, id: int, code: str, title: str, credits: int, teachingStaffID: int) -> None:
       self.course_id = id
       self.course_code = code
       self.course_title = title
       self.course_credits = credits
       self.course_teaching_staff_id = teachingStaffID 

    def __repr__(self) -> str:
        return f"<Course(course_id={self.course_id},course_code='{self.course_code}', course_title='{self.course_title}', course_credits={self.course_credits}, course_teaching_staff_id='{self.course_teaching_staff_id}', teaching_staff_title_id={self.teaching_staff_title_id}, teaching_staff_department_id={self.teaching_staff_department_id})>"


class Student(Base):

    __tablename__ = 'Student_T'

    __table_args__ = (
        CheckConstraint("`student_gpa` >= 0.00 AND `student_gpa` <= 5.00", name="student_gpa_check"),
    )

    student_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_first_name: Mapped[str] = mapped_column(String(15))
    student_middle_name: Mapped[Optional[str]] = mapped_column(String(15))
    student_last_name: Mapped[str] = mapped_column(String(15))
    student_email: Mapped[str] = mapped_column(String(50))
    student_gpa: Mapped[int] = mapped_column(DECIMAL(3, 2))
    student_year_of_enrollment: Mapped[int] = mapped_column()
    student_department_id: Mapped[int] = mapped_column(ForeignKey("Department_T.department_id"))

    student_department: Mapped["Department"] = relationship()
    student_course_list: Mapped[list["Student_Course"]] = relationship(back_populates="course")

    def __init__(self, id: int, firstName: str, middleName: str, lastName: str, email: str, yearOfEnrollment: int, departmentID: int) -> None:
        self.student_id = id
        self.student_first_name = firstName
        self.student_middle_name = middleName
        self.student_last_name = lastName
        self.student_email = email
        self.student_year_of_enrollment = yearOfEnrollment
        self.student_department_id = departmentID
        
    def __repr__(self) -> str:
        return f"<Student(student_id={self.student_id}, student_first_name='{self.student_first_name}', student_middle_name='{self.student_middle_name}', student_last_name='{self.student_last_name}', student_email='{self.student_email}', student_year_of_enrollment={self.student_year_of_enrollment}, student_department_id={self.student_department_id})>"

class Student_Course(Base):

    __tablename__ = 'Student_Course_JT'

    student_id: Mapped[int] = mapped_column(ForeignKey("Student_T.student_id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("Course_T.course_id"), primary_key=True)

    student: Mapped["Student"] = relationship(back_populates="course_student_list")
    course: Mapped["Course"] = relationship(back_populates="student_course_list")

    def __init__(self, student_id: int, course_id: int) -> None:
        self.student_id = student_id
        self.course_id = course_id

    def __repr__(self) -> str:
        return f"<StudentCourses(department_id={self.department_id}, department_title='{self.department_title}', department_faculty_id={self.department_faculty_id})>"