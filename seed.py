import random
from datetime import datetime, timedelta
from database import engine, SessionLocal
import models

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

user = models.User(email="test_user@example.com", password="securepassword123")
db.add(user)
db.commit()
db.refresh(user)

categories_data = ["Salary", "Food", "Rent", "Entertainment", "Utilities"]
categories = []
for name in categories_data:
    cat = models.Category(name=name)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    categories.append(cat)

budget = models.Budget(limit=1500.0, user_id=user.id, category_id=categories[1].id)
db.add(budget)
db.commit()

base_date = datetime(2026, 1, 1)

for i in range(60):
    cat = random.choice(categories)
    txn_type = "income" if cat.name == "Salary" else "expense"
    
    if txn_type == "income":
        amount = round(random.uniform(2000.0, 5000.0), 2)
    else:
        amount = round(random.uniform(10.0, 300.0), 2)
        
    random_days = random.randint(0, 89)
    txn_date = base_date + timedelta(days=random_days)

    txn = models.Transaction(
        amount=amount,
        type=txn_type,
        user_id=user.id,
        category_id=cat.id,
        date=txn_date
    )
    db.add(txn)

db.commit()
print("Database cleanly rebuilt and seeded with a User, Categories, a Budget, and 60 Transactions!")
db.close()
