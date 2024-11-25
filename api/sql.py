from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 数据库访问地址
USERNAME='root'
PASSWORD='1317b90'
HOSTNAME='114.132.45.130'
PORT='3306'
DATABASE='kmdb'
CHARSET='utf8mb4'
SQLALCHEMY_DATABASE_URI=('mysql+pymysql://'+
                         USERNAME+':'+PASSWORD+'@'+
                         HOSTNAME+':'+PORT+'/'+
                         DATABASE+
                         '?charset='+CHARSET)

# 启动引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=False,  # echo 设为 True 会打印出实际执行的 sql，调试的时候更方便
    future=True,  # 使用 SQLAlchemy 2.0 API，向后兼容
    pool_size=5, # 连接池的大小默认为 5 个，设置为 0 时表示连接无限制
    pool_recycle=3600, # 设置时间以限制数据库自动断开
)

# 启动会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 数据模型的基类
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
