from models import User, Announcement, Category
from app import db

db.create_all()
category_1 = Category(uid=1,name='job',homePage='http://job')
user = User(uid=1, name='Ivan')
announcement_1 = Announcement(uid=1,name='cleaner',releaseDate='24.01.2089',local=1,manufacturer=category_1)

db.session.add(category_1)
db.session.add(user)
db.session.add(announcement_1)
db.session.commit()

print(db.session.query(User).all())
print(db.session.query(Announcement).all())
print(db.session.query(Category).all())

db.session.close()
