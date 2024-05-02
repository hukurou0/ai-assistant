from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from fastapi import FastAPI, Depends, HTTPException
from suggest_todo import find_well_todos

# データベース設定
DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@postgres/mydatabase"

# SQLAlchemy用のエンジンを作成
engine = create_async_engine(
  DATABASE_URL, 
  echo=True,
  pool_size=5,          # プール内のコネクション数
  max_overflow=10,      # プールサイズを超えた際の最大数
  pool_timeout=30,      # プールからコネクションを取得する際のタイムアウト秒数
  pool_recycle=-1       # コネクションを再利用するための時間（秒）、デフォルトではリサイクルしない
)

# セッションを作成するためのファクトリーを生成
async_session = sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

# FastAPI アプリケーション
app = FastAPI()

# 依存関係
async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# ルートエンドポイント
@app.get("/")
async def read_root(db: AsyncSession = Depends(get_db_session)):
    async with db.begin():
        result = await db.execute(text("SELECT 'Hello, World!'"))
        hello_world = result.scalar_one()
        print(hello_world)
    return {"message": hello_world}
  
@app.get("/find")
def read_root():
    well_todos = find_well_todos()
    return {"data": well_todos}
