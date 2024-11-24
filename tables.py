from sqlalchemy import Integer, DECIMAL, String, PrimaryKeyConstraint, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Faculty(Base):
    __tablename__ = 'Faculty_T'
    __table_args__ = (
        PrimaryKeyConstraint(["faculty_id"], name="faculty_pk")
    )
    
    faculty_id: Mapped[int] = mapped_column(autoincrement=True)
    faculty_title: Mapped[str] = mapped_column(String(50), nullable=False)
    
    def __repr__(self) -> str:
        return f"<Faculty(faculty_id={self.faculty_id}, faculty_title='{self.faculty_title}')>"

class Department(Base):
    __tablename__ = 'Department_T'
    __table_args__ = (
        PrimaryKeyConstraint(['department_id'], name="department_fk"),
        ForeignKeyConstraint(['department_faculty_id'], refcolumns=['faculty_t.faculty_id'], name="department_faculty_fk")
    )
    
    department_id: Mapped[int] = mapped_column(autoincrement=True)
    department_title: Mapped[str] = mapped_column(String(50), nullable=False)
    department_faculty_id: Mapped[int] = mapped_column(nullable=False)


class Title(Base):
    __tablename__ = 'Title_T'
    __table_args__ = (
        PrimaryKeyConstraint(columns=['title_id'], name='title_pk')
    )
    
    title_id: Mapped[int] = mapped_column(autoincrement=True)
    title_description: Mapped[str] = mapped_column(String(25), nullable=False)

class TeachingStaff(Base):
    __tablename__ = 'Teaching_Staff_T'
    __table_args__ = (
        PrimaryKeyConstraint(['teaching_staff_id'], name="teaching_staff_pk"),
        ForeignKeyConstraint(['teaching_staff_title_id'], refcolumns=['Title_T.title_id'], name="teaching_staff_title_fk"),
        ForeignKeyConstraint(['teaching_staff_department_id'], refcolumns=['Department_T.department_id'], name="teaching_staff_department_fk")
    )

    teaching_staff_id: Mapped[int] = mapped_column(autoincrement=True)
    teaching_staff_first_name: Mapped[str] = mapped_column(String(15), nullable=False)
    teaching_staff_middle_name: Mapped[str] = mapped_column(String(15), nullable=True)
    teaching_staff_last_name: Mapped[str] = mapped_column(String(15), nullable=False)
    teaching_staff_email: Mapped[str] = mapped_column(String(50), nullable=False)
    teaching_staff_title_id: Mapped[int] = mapped_column(nullable=False)
    teaching_staff_department_id: Mapped[int] = mapped_column(nullable=False)
    
class Course(Base):
    __tablename__ = 'Course_T'
    __table_args__ = (
        PrimaryKeyConstraint(['course_id'], name="course_pk"),
        ForeignKeyConstraint(['course_teaching_staff_id'], refcolumns=['Teaching_Staff_T.teaching_staff_id'], name="course_teaching_staff_fk")
    )

    course_id: Mapped[int] = mapped_column(autoincrement=True)
    course_code: Mapped[str] = mapped_column(String(8), nullable=False)
    course_title: Mapped[str] = mapped_column(String(45), nullable=False)
    course_credits: Mapped[int] = mapped_column(nullable=False)
    course_teaching_staff_id: Mapped[int] = mapped_column(nullable=False)

class Student(Base):
    __table__ = 'Student_T'
    __table_args__ = (
        PrimaryKeyConstraint(['student_id'], name="student_pk"),
        ForeignKeyConstraint(['student_department_id'], refcolumns=['Department_T.department_id'], name="student_department_fk"),
        CheckConstraint("`student_gpa` >= 0.00 AND `student_gpa` <= 5.00", name="student_gpa_check")
    )

    student_id: Mapped[int] = mapped_column(autoincrement=True)
    student_first_name: Mapped[str] = mapped_column(String(15), nullable=False)
    student_middle_name: Mapped[str] = mapped_column(String(15), nullable=True)
    student_last_name: Mapped[str] = mapped_column(String(15), nullable=False)
    student_email: Mapped[str] = mapped_column(String(50), nullable=False)
    student_gpa: Mapped[int] = mapped_column(DECIMAL(3, 2), nullable=False)
    student_year_of_enrollment: Mapped[int] = mapped_column(nullable=False)
    student_department_id: Mapped[int] = mapped_column(nullable=False)

class Student_Course(Base):
    __tablename__ = 'Student_Course_JT'
    __table_args__ = (
        PrimaryKeyConstraint(['student_id', 'course_id'], name="student_course_pk"),
        ForeignKeyConstraint(['student_id'], refcolumns=["Student_T.student_id"], name="student_fk"),
        ForeignKeyConstraint(['course_id'], refcolumns=["Course_T.course_id"], name="course_fk")
    )

    student_id: Mapped[int] = mapped_column(nullable=False)
    course_id: Mapped[int] = mapped_column(nullable=False)