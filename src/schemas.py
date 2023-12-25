from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from enum import StrEnum


# Enum for ExpenseCategory
class ExpenseCategory(StrEnum):
    FOODSTUFF = "Foodstuff"
    UTILITY = "Utility"
    ENTERTAINMENT = "Entertainment"
    TRANSPORT = "Transport"
    OTHER = "Other"


# Enum for IncomeSource
class IncomeSource(StrEnum):
    SALARY = "Salary"
    FREELANCE = "Freelance"
    INVESTMENT = "Investment"
    GIFT = "Gift"
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
    category: Optional[ExpenseCategory] = ExpenseCategory.OTHER


class ExpenseRead(ExpenseBase):
    date: datetime
    id: int


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = 0.0
    description: Optional[str | None] = None
    category: Optional[ExpenseCategory] = ExpenseCategory.OTHER


# Pydantic model for Income
class IncomeBase(BaseModel):
    amount: float
    description: str
    source: Optional[IncomeSource] = IncomeSource.OTHER


class IncomeRead(IncomeBase):
    date: datetime
    id: int


class IncomeUpdate(BaseModel):
    amount: Optional[float] = 0.0
    description: Optional[str | None] = None
    source: Optional[IncomeSource] = IncomeSource.OTHER
