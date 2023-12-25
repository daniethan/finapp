from datetime import datetime
from src.dbconfig import Base
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Enum,
)
from src.schemas import ExpenseCategory, IncomeSource
from sqlalchemy.orm import relationship

# class ExpenseCategory(Base):
#     __tablename__ = 'expense_categories'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String, unique=True, nullable=False)
#     description = Column(String, nullable=True)


# class IncomeSource(Base):
#     __tablename__ = 'income_sources'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String, unique=True, nullable=False)
#     description = Column(String, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    disabled = Column(Boolean, default=False)
    fullname = Column(String, nullable=False, index=True)
    password = Column(String, nullable=False)

    items = relationship("Expense", back_populates="owner")
    incomes = relationship("Income", back_populates="owner")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    category = Column(Enum(ExpenseCategory), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    # category = relationship("ExpenseCategory", back_populates="expenses")

    owner = relationship("User", back_populates="items")


class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    source = Column(Enum(IncomeSource), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    # source = relationship("IncomeSource", back_populates="incomes")

    owner = relationship("User", back_populates="incomes")


# ExpenseCategory.expenses = relationship("Expense", order_by=Expense.id, back_populates="category")
# IncomeSource.incomes = relationship("Income", order_by=Income.id, back_populates="source")
