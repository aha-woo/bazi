"""
Pydantic数据模型（用于API请求和响应）
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime


class BaziRequest(BaseModel):
    """八字计算请求"""
    year: int = Field(..., ge=1900, le=2100, description="出生年份")
    month: int = Field(..., ge=1, le=12, description="出生月份")
    day: int = Field(..., ge=1, le=31, description="出生日期")
    hour: int = Field(..., ge=0, le=23, description="出生小时")
    minute: int = Field(0, ge=0, le=59, description="出生分钟")
    timezone: str = Field("Asia/Shanghai", description="时区")
    user_id: Optional[str] = Field(None, description="用户ID（可选）")
    
    @validator('timezone')
    def validate_timezone(cls, v):
        """验证时区"""
        import pytz
        try:
            pytz.timezone(v)
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValueError(f"Invalid timezone: {v}")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "year": 1990,
                "month": 5,
                "day": 15,
                "hour": 14,
                "minute": 30,
                "timezone": "Asia/Shanghai",
                "user_id": "user123"
            }
        }


class SizhuInfo(BaseModel):
    """四柱信息"""
    ganzhi: str = Field(..., description="干支")
    tian: str = Field(..., description="天干")
    di: str = Field(..., description="地支")


class WuxingAnalysis(BaseModel):
    """五行分析"""
    count: Dict[str, int] = Field(..., description="五行计数")
    strongest: str = Field(..., description="最旺的五行")
    weakest: str = Field(..., description="最弱的五行")
    total: int = Field(..., description="总数")


class Interpretation(BaseModel):
    """命理解读"""
    basic: str = Field(..., description="基础解读")
    wuxing_distribution: str = Field(..., description="五行分布")
    wuxing_balance: str = Field(..., description="五行平衡")
    personality: str = Field(..., description="性格特征")
    xiyongshen: str = Field(..., description="喜用神")
    advice: str = Field(..., description="建议")
    full_text: str = Field(..., description="完整解读文本")


class BaziResponse(BaseModel):
    """八字计算响应"""
    id: Optional[int] = Field(None, description="记录ID")
    birth_time: str = Field(..., description="出生时间")
    timezone: str = Field(..., description="时区")
    year_pillar: str = Field(..., description="年柱")
    month_pillar: str = Field(..., description="月柱")
    day_pillar: str = Field(..., description="日柱")
    hour_pillar: str = Field(..., description="时柱")
    rigan: str = Field(..., description="日主")
    rigan_wuxing: str = Field(..., description="日主五行")
    wuxing_analysis: WuxingAnalysis = Field(..., description="五行分析")
    interpretation: Interpretation = Field(..., description="命理解读")
    sizhu: Dict[str, SizhuInfo] = Field(..., description="四柱详细信息")
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "birth_time": "1990-05-15T14:30:00+08:00",
                "timezone": "Asia/Shanghai",
                "year_pillar": "庚午",
                "month_pillar": "辛巳",
                "day_pillar": "甲子",
                "hour_pillar": "辛未",
                "rigan": "甲",
                "rigan_wuxing": "木",
                "wuxing_analysis": {
                    "count": {"木": 1, "火": 2, "土": 1, "金": 2, "水": 2},
                    "strongest": "火",
                    "weakest": "木",
                    "total": 8
                }
            }
        }


class BaziRecordResponse(BaseModel):
    """八字记录响应（从数据库查询）"""
    id: int
    user_id: Optional[str]
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour: int
    birth_minute: int
    timezone: str
    year_pillar: str
    month_pillar: str
    day_pillar: str
    hour_pillar: str
    rigan: str
    rigan_wuxing: str
    wuxing_analysis: Optional[Dict[str, Any]]
    interpretation: Optional[str]
    created_at: datetime
    
    class Config:
        orm_mode = True


class HealthCheckResponse(BaseModel):
    """健康检查响应"""
    status: str = Field(..., description="状态")
    message: str = Field(..., description="消息")
    timestamp: datetime = Field(..., description="时间戳")
    version: str = Field(..., description="版本")

