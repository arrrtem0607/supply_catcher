from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from supply_catcher.db.models import Base
from supply_catcher.config import DB_CONFIG

# Формируем строку подключения из конфигурации
DATABASE_URL = (f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
                f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}")

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
