"""
FastAPI主应用
八字计算API服务
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from datetime import datetime

from . import models, schemas, crud
from .database import engine, get_db, init_db
from .bazi_calculator import calculate_bazi_from_input

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title="八字计算API",
    description="专业的八字命理计算服务，支持跨平台调用（Web、iOS、Android）",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS配置（允许跨域访问）
cors_origins = os.getenv(
    "CORS_ORIGINS", 
    "http://localhost:3000,http://localhost:8080,http://127.0.0.1:5500"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    print("🚀 八字计算API服务启动中...")
    print("📚 API文档地址: http://localhost:8000/docs")
    init_db()
    print("✅ 数据库初始化完成")


@app.get("/", tags=["根路径"])
async def root():
    """根路径欢迎信息"""
    return {
        "message": "欢迎使用八字计算API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=schemas.HealthCheckResponse, tags=["健康检查"])
async def health_check():
    """健康检查接口"""
    return schemas.HealthCheckResponse(
        status="healthy",
        message="服务运行正常",
        timestamp=datetime.now(),
        version="1.0.0"
    )


@app.post("/api/v1/bazi/calculate", response_model=schemas.BaziResponse, tags=["八字计算"])
async def calculate_bazi(
    request: schemas.BaziRequest,
    db: Session = Depends(get_db),
    save_to_db: bool = True
):
    """
    计算八字四柱和命理解读
    
    **参数说明：**
    - year: 出生年份 (1900-2100)
    - month: 出生月份 (1-12)
    - day: 出生日期 (1-31)
    - hour: 出生小时 (0-23)
    - minute: 出生分钟 (0-59)，默认0
    - timezone: 时区，默认 Asia/Shanghai
    - user_id: 用户ID（可选）
    
    **返回：**
    - 四柱（年月日时）
    - 五行分析
    - 命理解读
    - 性格特征
    - 喜用神建议
    - 运势建议
    """
    try:
        # 计算八字
        bazi_data = calculate_bazi_from_input(
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            minute=request.minute,
            timezone_str=request.timezone
        )
        
        # 保存到数据库
        record_id = None
        if save_to_db:
            db_record = crud.create_bazi_record(db, request, bazi_data)
            record_id = db_record.id
        
        # 构建响应
        response_data = {
            "id": record_id,
            **bazi_data
        }
        
        return schemas.BaziResponse(**response_data)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"日期参数错误: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"计算八字时发生错误: {str(e)}"
        )


@app.get("/api/v1/bazi/record/{record_id}", response_model=schemas.BaziRecordResponse, tags=["八字查询"])
async def get_bazi_record(record_id: int, db: Session = Depends(get_db)):
    """
    根据ID查询八字记录
    
    **参数：**
    - record_id: 记录ID
    
    **返回：**
    - 八字记录详情
    """
    record = crud.get_bazi_record(db, record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"未找到ID为{record_id}的记录"
        )
    return record


@app.get("/api/v1/bazi/user/{user_id}", response_model=List[schemas.BaziRecordResponse], tags=["八字查询"])
async def get_user_bazi_records(
    user_id: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    查询用户的八字记录列表
    
    **参数：**
    - user_id: 用户ID
    - skip: 跳过记录数（分页）
    - limit: 返回记录数（分页）
    
    **返回：**
    - 八字记录列表
    """
    records = crud.get_bazi_records_by_user(db, user_id, skip, limit)
    return records


@app.get("/api/v1/bazi/records", response_model=List[schemas.BaziRecordResponse], tags=["八字查询"])
async def get_all_bazi_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    查询所有八字记录
    
    **参数：**
    - skip: 跳过记录数（分页）
    - limit: 返回记录数（分页）
    
    **返回：**
    - 八字记录列表
    """
    records = crud.get_all_records(db, skip, limit)
    return records


@app.delete("/api/v1/bazi/record/{record_id}", tags=["八字管理"])
async def delete_bazi_record(record_id: int, db: Session = Depends(get_db)):
    """
    删除八字记录
    
    **参数：**
    - record_id: 记录ID
    
    **返回：**
    - 删除结果
    """
    success = crud.delete_bazi_record(db, record_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"未找到ID为{record_id}的记录"
        )
    return {"message": f"记录{record_id}已成功删除"}


@app.get("/api/v1/timezones", tags=["工具"])
async def get_timezones():
    """
    获取支持的时区列表
    
    **返回：**
    - 常用时区列表
    """
    import pytz
    
    # 返回常用的中国及亚洲时区
    common_timezones = {
        "中国": {
            "Asia/Shanghai": "北京时间 (UTC+8)",
            "Asia/Urumqi": "乌鲁木齐时间 (UTC+6)"
        },
        "亚洲": {
            "Asia/Hong_Kong": "香港 (UTC+8)",
            "Asia/Taipei": "台北 (UTC+8)",
            "Asia/Tokyo": "东京 (UTC+9)",
            "Asia/Seoul": "首尔 (UTC+9)",
            "Asia/Singapore": "新加坡 (UTC+8)",
            "Asia/Bangkok": "曼谷 (UTC+7)",
            "Asia/Dubai": "迪拜 (UTC+4)"
        },
        "其他": {
            "UTC": "UTC标准时间",
            "America/New_York": "纽约 (UTC-5/-4)",
            "America/Los_Angeles": "洛杉矶 (UTC-8/-7)",
            "Europe/London": "伦敦 (UTC+0/+1)",
            "Australia/Sydney": "悉尼 (UTC+10/+11)"
        }
    }
    
    return {
        "common_timezones": common_timezones,
        "all_timezones": pytz.all_timezones
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "False").lower() == "true"
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload
    )

