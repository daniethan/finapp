from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from enum import StrEnum


# Enum for ExpenseCategory
class ExpenseCategory(StrEnum):
    GROCERIES = "Groceries"
    UTILITIES = "Utilities"
    ENTERTAINMENT = "Entertainment"
    TRANSPORT = "Transport"
    OTHER = "Other"


# Enum for IncomeSource
class IncomeSource(StrEnum):
    SALARY = "Salary"
    FREELANCE = "Freelance"
    INVESTMENT = "Investments"
    GIFT = "Gifts"
    OTHER = "Other"


# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


# pydantic model for Users
class UserBase(BaseModel):
    username: str
    fullname: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    disabled: bool
    id: int


# Pydantic model for Expense
class ExpenseBase(BaseModel):
    amount: float
    description: str
    category: Optional[ExpenseCategory] = ExpenseCategory.GROCERIES


class ExpenseRead(ExpenseBase):
    date: datetime
    id: int


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = 0.0
    description: Optional[str | None] = None
    category: Optional[ExpenseCategory] = ExpenseCategory.GROCERIES


# Pydantic model for Income
class IncomeBase(BaseModel):
    amount: float
    description: str
    source: Optional[IncomeSource] = IncomeSource.SALARY


class IncomeRead(IncomeBase):
    date: datetime
    id: int


class IncomeUpdate(BaseModel):
    amount: Optional[float] = 0.0
    description: Optional[str | None] = None
    source: Optional[IncomeSource] = IncomeSource.SALARY
