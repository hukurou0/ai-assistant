from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
import yaml

# データベース設定
DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@postgres/mydatabase"

# SQLAlchemy用のエンジンを作成
engine = create_async_engine(
  DATABASE_URL, 
  #echo=True,
  pool_size=5,          # プール内のコネクション数
  max_overflow=10,      # プールサイズを超えた際の最大数
  pool_timeout=30,      # プールからコネクションを取得する際のタイムアウト秒数
  pool_recycle=-1       # コネクションを再利用するための時間（秒）、デフォルトではリサイクルしない
)

# セッションを作成するためのファクトリーを生成
async_session = sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession,
    autocommit=False
)

# FastAPI アプリケーション
app = FastAPI()

# OpenAPIの仕様をファイルから読み込む
with open("./doc/v1.0.0.yaml", "r") as file:
    openapi_schema = yaml.safe_load(file)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# 依存関係
async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session