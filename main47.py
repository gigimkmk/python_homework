
import time
from datetime import datetime, timezone

from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker

DATABASE_URL = "sqlite:///./student_subjects.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


student_subject = Table(
    "student_subject",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True),
    Column("joined_at", DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False),
)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)

    subjects = relationship(
        "Subject",
        secondary=student_subject,
        back_populates="students",
    )


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    duration = Column(Integer, nullable=False)

    students = relationship(
        "Student",
        secondary=student_subject,
        back_populates="subjects",
    )


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class SubjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    duration: int = Field(..., gt=0)


class StudentCreate(StudentBase):
    pass


class SubjectCreate(SubjectBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    surname: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None


class SubjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    duration: int | None = Field(default=None, gt=0)


class StudentResponse(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SubjectResponse(SubjectBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student and Subject API")


def send_welcome_email(email: str):
    print(f'Sending welcome email to "{email}"', flush=True)
    time.sleep(3)
    print(f'Email sent to "{email}"', flush=True)


@app.get("/")
def home():
    return {"message": "Student and Subject API is running"}


@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student: StudentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    new_student = Student(**student.model_dump())

    db.add(new_student)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Student with this email already exists")

    db.refresh(new_student)

    background_tasks.add_task(send_welcome_email, new_student.email)

    return new_student


@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    data: StudentUpdate,
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(student, key, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Student with this email already exists")

    db.refresh(student)
    return student


@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.subjects.clear()
    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}


@app.post("/subjects", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    new_subject = Subject(**subject.model_dump())

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject


@app.get("/subjects", response_model=list[SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()


@app.get("/subjects/{subject_id}", response_model=SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.get(Subject, subject_id)

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    return subject


@app.put("/subjects/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: int,
    data: SubjectUpdate,
    db: Session = Depends(get_db),
):
    subject = db.get(Subject, subject_id)

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    for key, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(subject, key, value)

    db.commit()
    db.refresh(subject)

    return subject


@app.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.get(Subject, subject_id)

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    subject.students.clear()
    db.delete(subject)
    db.commit()

    return {"message": "Subject deleted successfully"}


@app.post("/students/{student_id}/subjects/{subject_id}")
def enroll_student(
    student_id: int,
    subject_id: int,
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id)
    subject = db.get(Subject, subject_id)

    if not student or not subject:
        raise HTTPException(status_code=404, detail="Student or subject not found")

    if subject in student.subjects:
        raise HTTPException(status_code=400, detail="Student already enrolled")

    student.subjects.append(subject)
    db.commit()

    return {"message": "Student enrolled successfully"}


@app.get("/students/{student_id}/subjects", response_model=list[SubjectResponse])
def get_student_subjects(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student.subjects


@app.get("/subjects/{subject_id}/students", response_model=list[StudentResponse])
def get_subject_students(subject_id: int, db: Session = Depends(get_db)):
    subject = db.get(Subject, subject_id)

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    return subject.students


@app.delete("/students/{student_id}/subjects/{subject_id}")
def remove_enrollment(
    student_id: int,
    subject_id: int,
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id)
    subject = db.get(Subject, subject_id)

    if not student or not subject:
        raise HTTPException(status_code=404, detail="Student or subject not found")

    if subject not in student.subjects:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    student.subjects.remove(subject)
    db.commit()

    return {"message": "Enrollment removed successfully"}
