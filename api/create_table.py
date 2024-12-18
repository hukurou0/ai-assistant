# create_table.py
from sqlalchemy.ext.asyncio import create_async_engine
from src.models.make_base import Base

# 環境変数のロード
import os
from dotenv import load_dotenv

load_dotenv()

# データベースの接続情報
database_url = os.getenv("DATABASE_URL").replace(
    "postgres://", "postgresql+asyncpg://"
)  # Heroku用の置換

if not database_url:
    raise ValueError("DATABASE_URLが設定されていません。")

# 非同期エンジンの作成
engine = create_async_engine(database_url, echo=True)


async def create_tables():
    """
    データベースのテーブルを全て作成する。
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# テーブルを作成する処理を実行
async def execute_create():
    await create_tables()
