from model.user import User
from schema.user_schema import UserCreate, UserUpdate


def create_user(user: UserCreate, db):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(user: UserUpdate, db):
    db_user = db.query(User).filter(User.id == user.id).first()
    if not db_user:
        return None
    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(user_id: int, db):
    return db.query(User).filter(User.id == user_id).first()
