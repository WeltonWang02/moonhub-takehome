from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from contextlib import contextmanager

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    inventory = Column(Integer)
    last_modified = Column(BigInteger, default=lambda: int(datetime.now().timestamp())) 

class InventoryDB:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    def __del__(self):
        self.Session.remove()

    @contextmanager
    def session_scope(self):
        """Prevent hanging sessions."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_products(self, filter="", limit=10, sort="name", order="asc"):
        with self.session_scope() as session:
            query = session.query(Product)
            if filter:
                query = query.filter(Product.name.like(f'%{filter}%') | Product.description.like(f'%{filter}%'))
            if sort and order:
                sort_column = getattr(Product, sort, None)
                if sort_column:
                    if order == "desc":
                        query = query.order_by(sort_column.desc())
                    else:
                        query = query.order_by(sort_column)
            products = query.limit(limit).all()
            result = [{column.name: getattr(product, column.name) for column in product.__table__.columns} for product in products]
            return result
        
    def insert_product(self, name, description, inventory):
        # Input validation
        if not name or not description or inventory < 0:
            return False  # Invalid input
        
        with self.session_scope() as session:
            existing_product = session.query(Product).filter_by(name=name).first()
            if existing_product:
                existing_product.description = description
                existing_product.inventory = inventory
                existing_product.last_modified = int(datetime.now().timestamp())
            else:
                new_product = Product(name=name, description=description, inventory=inventory)
                session.add(new_product)
            session.commit()
        return True  # Successful insertion or update
