"""
数据库模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from .database import Base


class BaziRecord(Base):
    """八字计算记录表"""
    __tablename__ = "bazi_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # 用户信息
    user_id = Column(String(100), nullable=True, index=True, comment="用户ID（可选）")
    
    # 出生信息
    birth_year = Column(Integer, nullable=False, comment="出生年份")
    birth_month = Column(Integer, nullable=False, comment="出生月份")
    birth_day = Column(Integer, nullable=False, comment="出生日期")
    birth_hour = Column(Integer, nullable=False, comment="出生小时")
    birth_minute = Column(Integer, nullable=False, default=0, comment="出生分钟")
    timezone = Column(String(50), nullable=False, default="Asia/Shanghai", comment="时区")
    
    # 八字结果
    year_pillar = Column(String(10), nullable=False, comment="年柱")
    month_pillar = Column(String(10), nullable=False, comment="月柱")
    day_pillar = Column(String(10), nullable=False, comment="日柱")
    hour_pillar = Column(String(10), nullable=False, comment="时柱")
    
    # 日主
    rigan = Column(String(5), nullable=False, comment="日主")
    rigan_wuxing = Column(String(5), nullable=False, comment="日主五行")
    
    # 五行分析（JSON格式）
    wuxing_analysis = Column(JSON, nullable=True, comment="五行分析")
    
    # 命理解读
    interpretation = Column(Text, nullable=True, comment="命理解读")
    
    # 完整八字数据（JSON格式）
    full_data = Column(JSON, nullable=True, comment="完整八字数据")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<BaziRecord {self.year_pillar}{self.month_pillar}{self.day_pillar}{self.hour_pillar}>"

