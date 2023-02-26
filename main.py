from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Date
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'
    id_author = Column('id_author', Integer, primary_key=True)
    name = Column('name', String(50))

    def __init__(self, id_author, name):
        self.id_author = id_author
        self.name = name

    def __str__(self):
        return f'({self.id_author}) {self.name}'


class Book(Base):
    __tablename__ = 'book'
    id_book = Column('id_book', Integer, primary_key=True)
    title = Column('title', String(50))
    id_author = Column('id_author', Integer, ForeignKey('publisher.id_author'))

    def __str__(self):
        return f'{self.title}'

    def __init__(self, id_book, title, id_author):
        self.id_book = id_book
        self.title = title
        self.id_author = id_author


class Shop(Base):
    __tablename__ = 'shop'
    id_shop = Column('id_shop', Integer, primary_key=True)
    name = Column('name', String(50))

    def __init__(self, id_shop, name):
        self.id_shop = id_shop
        self.name = name

    def __str__(self):
        return f'{self.name}'


class Stock(Base):
    __tablename__ = 'stock'
    id_stock = Column('id_stock', Integer, primary_key=True)
    id_book = Column('id_book', Integer, ForeignKey('book.id_book'))
    id_shop = Column('id_shop', Integer, ForeignKey('shop.id_shop'))
    count = Column('count', Integer)

    def __init__(self, id_stok, id_book, id_shop, count):
        self.id_stock = id_stok
        self.id_book = id_book
        self.id_shop = id_shop
        self.count = count


class Sale(Base):
    __tablename__ = 'sale'
    id_price = Column('id_price', Integer, primary_key=True)
    price = Column('price', Integer)
    date_sale = Column('date_sale', Date)
    id_stock = Column('id_stock', Integer, ForeignKey('stock.id_stock'))
    count = Column('count', Integer)

    def __init__(self, id_price, price, date_sale, id_stock, count):
        self.id_price = id_price
        self.price = price
        self.date_sale = date_sale
        self.id_stock = id_stock
        self.count = count

    def __str__(self):
        return f'{self.price} | {self.date_sale}'



engine = create_engine("postgresql://...:...@localhost:5432/...")
conn = engine.connect()
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

author_1 = Publisher(1,'Пушкин')
author_2 = Publisher(2,'Блок')
author_3 = Publisher(3, 'Толстой')

session.add(author_1)
session.add(author_2)
session.add(author_3)
session.commit()

book_1 = Book(1, 'Капитанская дочка', 1)
book_2 = Book(2, 'Руслан и Людмида', 1)
book_3 = Book(3, 'Война и Мир', 3)
book_4 = Book(4, 'Предчувствую тебя...', 2)
book_5 = Book(5, 'Евгений Онегин', 1)
book_6 = Book(6, 'Жрец. Том 1', 2)

session.add(book_1)
session.add(book_2)
session.add(book_3)
session.add(book_4)
session.add(book_5)
session.add(book_6)
session.commit()

shop_1 = Shop(1, 'Буквоед')
shop_2 = Shop(2, 'Книжный дом')
shop_3 = Shop(3, 'Лабиринт')

session.add(shop_1)
session.add(shop_2)
session.add(shop_3)

session.commit()

stock_1 = Stock(1, 1, 1, 1)
stock_2 = Stock(2, 2, 1, 1)
stock_3 = Stock(3, 3, 2, 1)
stock_4 = Stock(4, 4, 3, 1)
stock_5 = Stock(5, 5, 2, 1)
stock_6 = Stock(6, 6, 3, 1)

session.add(stock_1)
session.add(stock_2)
session.add(stock_3)
session.add(stock_4)
session.add(stock_5)
session.add(stock_6)

session.commit()

sale_1 = Sale(1, 600, '2023-02-03', 1, 1)
sale_2 = Sale(2, 500, '2023-02-12', 2, 1)
sale_3 = Sale(3, 700, '2023-02-14', 3, 1)
sale_4 = Sale(4, 450, '2023-02-18', 4, 1)
sale_5 = Sale(5, 490, '2023-02-20', 5, 1)
sale_6 = Sale(6, 600, '2023-02-23', 6, 1)

session.add(sale_1)
session.add(sale_2)
session.add(sale_3)
session.add(sale_4)
session.add(sale_5)
session.add(sale_6)

session.commit()


author = input("Введите фамилию автора: ")
if author.capitalize() == 'Пушкин' or author.capitalize() == 'Блок' or author.capitalize() == 'Толстой':
    result = session.query(Book, Shop, Sale).filter(Publisher.name == author.capitalize()).\
    filter(Publisher.id_author == Book.id_author).filter(Book.id_book == Stock.id_book).\
    filter(Stock.id_shop == Shop.id_shop).filter(Stock.id_stock == Sale.id_stock).all()
    for r in result:
        print(f'{r[0]} | {r[1]} | {r[2]}')
else:
    print('Книг этого автора нет!')

session.close()
