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
    primary_key = list(model_class.__table__.primary_key.columns)[0]
    return db.query(model_class).order_by(primary_key).offset(skip).limit(limit).all()

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
def delete_record(db: Session, model_class, record_id=None, record_obj=None):
    if record_obj:
        db.delete(record_obj)
        db.commit()
        return record_obj
    record = db.query(model_class).get(record_id)
    if not record:
        return None
    db.delete(record)
    db.commit()
    return record
