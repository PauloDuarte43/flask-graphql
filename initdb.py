from app import db, User, Post, Customer, Address
db.create_all()

# create new user
john = User(username='johndoe')

# create new post
post = Post()
post.title = "Hello World"
post.body = "This is the first post"
post.author = john

# create new Customer
customer = Customer()
customer.name = "Julio"
customer.last_name = "Silva"

customer2 = Customer()
customer2.name = "Maria"
customer2.last_name = "Antonia"

# create new address
address = Address()
address.street = "Rua 1"
address.district = "Distrito 1"
address.number = 100

address2 = Address()
address2.street = "Rua 2"
address2.district = "Distrito 2"
address2.number = 200

address3 = Address()
address3.street = "Rua 3"
address3.district = "Distrito 3"
address3.number = 300

# save new user
db.session.add(john)
# save new post
db.session.add(post)
# save new customer
db.session.add(customer)
db.session.add(customer2)
# save new address
db.session.add(address)
db.session.add(address2)
db.session.add(address3)

# commit
db.session.commit()

print("Users: {0}".format(User.query.all()))
print("Posts: {0}".format(Post.query.all()))
print("Addresses: {0}".format(Address.query.all()))
print("Customers: {0}".format(Customer.query.all()))