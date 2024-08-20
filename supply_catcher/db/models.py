from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float

Base = declarative_base()  # Если Base не был определён


class Coefficient(Base):
    __tablename__ = 'coefficients'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    coefficient = Column(Float, nullable=False)
    warehouse_id = Column(Integer, nullable=False)
    warehouse_name = Column(String, nullable=False)
    box_type_name = Column(String, nullable=False)
    box_type_id = Column(Integer, nullable=False)

    def __repr__(self):
        return (f"<Coefficient(date={self.date}, "
                f"coefficient={self.coefficient}, "
                f"warehouse_id={self.warehouse_id}, "
                f"warehouse_name='{self.warehouse_name}', "
                f"box_type_name='{self.box_type_name}', "
                f"box_type_id={self.box_type_id})>")
