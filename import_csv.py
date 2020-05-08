import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(("postgres://tpkqhqnetayrsu:23c139d1b303cb7ddf334cce450d0bef1e0a77aa5fbf00995569b0d9416f90fd@ec2-3-223-21-106.compute-1.amazonaws.com:5432/dk1prhbsjkpq9"))
#engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

'''
def main():
    f = open("books.csv")
    print(type(f))
    reader = csv.reader(f)
    print(type(reader))
    for isbn, title, author, year in reader[1:]:
   	    db.execute("INSERT INTO books(isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn": isbn, "title": title, "author": author, "year": year})
   	    db.commit()

if __name__ == "__main__":
	main()
'''






def main():
    #db.execute("CREATE TABLE books (isbn VARCHAR PRIMARY KEY, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year VARCHAR NOT NULL) ")

    f = open("books.csv")
    reader = csv.reader(f)
    next(reader)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO BOOKS (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", 
        {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added ISBN: {isbn}, title: {title}, author {author} and year {year} to the database")
        db.commit()

if __name__ == "__main__":
    main()
