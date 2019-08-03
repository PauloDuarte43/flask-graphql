# Imports
import os
import graphene
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView

basedir = os.path.abspath(os.path.dirname(__file__))
# app initialization
app = Flask(__name__)
app.debug = True

# Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_BINDS'] = {
    'db1': 'sqlite:///' +    os.path.join(basedir, 'data1.sqlite'),
    'db2': 'sqlite:///' +    os.path.join(basedir, 'data2.sqlite')
}
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Modules
db = SQLAlchemy(app)

# Models
class Address(db.Model):
    __bind_key__ = 'db1'
    __tablename__ = 'address'
    uuid = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(256))
    district = db.Column(db.String(256))
    number = db.Column(db.Integer)

    def __repr__(self): 
        return '<Address %r>' % self.street



class Customer(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'customer'
    uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))

    def __repr__(self): 
        return '<Customer %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    posts = db.relationship('Post', backref='author')
    
    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'
    uuid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))
    def __repr__(self):
        return '<Post %r>' % self.title


# Schema Objects
class PostObject(SQLAlchemyObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node, )


class UserObject(SQLAlchemyObjectType):
   class Meta:
       model = User
       interfaces = (graphene.relay.Node, )


class AddressObject(SQLAlchemyObjectType):
   class Meta:
       model = Address
       interfaces = (graphene.relay.Node, )


class CustomerObject(SQLAlchemyObjectType):
   class Meta:
       model = Customer
       interfaces = (graphene.relay.Node, )
       

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_posts = SQLAlchemyConnectionField(PostObject)
    all_users = SQLAlchemyConnectionField(UserObject)
    all_addresses = SQLAlchemyConnectionField(AddressObject)
    all_customers = SQLAlchemyConnectionField(CustomerObject)


schema = graphene.Schema(query=Query)


# Routes
@app.route('/')
def index():
    return '<p> Hello World</p>'


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)


if __name__ == '__main__':
     app.run()