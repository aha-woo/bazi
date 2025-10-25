"""
数据库CRUD操作
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from . import models, schemas


def create_bazi_record(db: Session, bazi_request: schemas.BaziRequest, bazi_data: dict) -> models.BaziRecord:
    """创建八字记录"""
    db_record = models.BaziRecord(
        user_id=bazi_request.user_id,
        birth_year=bazi_request.year,
        birth_month=bazi_request.month,
        birth_day=bazi_request.day,
        birth_hour=bazi_request.hour,
        birth_minute=bazi_request.minute,
        timezone=bazi_request.timezone,
        year_pillar=bazi_data['year_pillar'],
        month_pillar=bazi_data['month_pillar'],
        day_pillar=bazi_data['day_pillar'],
        hour_pillar=bazi_data['hour_pillar'],
        rigan=bazi_data['rigan'],
        rigan_wuxing=bazi_data['rigan_wuxing'],
        wuxing_analysis=bazi_data['wuxing_analysis'],
        interpretation=bazi_data['interpretation']['full_text'],
        full_data=bazi_data
    )
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_bazi_record(db: Session, record_id: int) -> Optional[models.BaziRecord]:
    """获取单个八字记录"""
    return db.query(models.BaziRecord).filter(models.BaziRecord.id == record_id).first()


def get_bazi_records_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 10) -> List[models.BaziRecord]:
    """获取用户的八字记录列表"""
    return db.query(models.BaziRecord).filter(
        models.BaziRecord.user_id == user_id
    ).order_by(
        models.BaziRecord.created_at.desc()
    ).offset(skip).limit(limit).all()


def get_all_records(db: Session, skip: int = 0, limit: int = 100) -> List[models.BaziRecord]:
    """获取所有八字记录"""
    return db.query(models.BaziRecord).order_by(
        models.BaziRecord.created_at.desc()
    ).offset(skip).limit(limit).all()


def delete_bazi_record(db: Session, record_id: int) -> bool:
    """删除八字记录"""
    record = db.query(models.BaziRecord).filter(models.BaziRecord.id == record_id).first()
    if record:
        db.delete(record)
        db.commit()
        return True
    return False

