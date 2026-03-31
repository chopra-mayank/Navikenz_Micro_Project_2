from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TransactionCreate(BaseModel):
    amount: float
    type: str # income or expense
    user_id: int
    category_id: int

class BudgetCreate(BaseModel):
    limit: float
    user_id: int
    category_id: int
