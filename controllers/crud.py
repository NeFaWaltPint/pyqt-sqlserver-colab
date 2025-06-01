from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# 📦 CREATE
def create_record(db: Session, model_class, data: dict):
    try:
        record = model_class(**data)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except SQLAlchemyError as e:
        db.rollback()
        raise e

# 📄 READ (uno o todos)
def get_record(db: Session, model_class, record_id):
    return db.query(model_class).get(record_id)

def get_all_records(db: Session, model_class, skip=0, limit=100):
    return db.query(model_class).offset(skip).limit(limit).all()

# ✏️ UPDATE
def update_record(db: Session, model_class, record_id, updates: dict):
    record = db.query(model_class).get(record_id)
    if not record:
        return None
    for key, value in updates.items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record

# ❌ DELETE
def delete_record(db: Session, model_class, record_id):
    record = db.query(model_class).get(record_id)
    if not record:
        return None
    db.delete(record)
    db.commit()
    return record
