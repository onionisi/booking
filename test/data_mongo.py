from mongoalchemy.session import Session
from mongoalchemy.document import Document, Index
from mongoalchemy.fields import *

# Subclasses of Document both provide the mapping needed for
# queries as well as the calsses for lading/saving objects.
class User(Document):
    config_collection_name = 'users'

    # Setting the possible values by using fields
    first_name = StringField()
    last_name = StringField()
    age = IntField(min_value=0, required=False)

    # db_field allows a different DB field name than the one on the
    # python object
    email = StringField(db_field='email_address')
    bio = StringField(max_length=1000, required=False)

    # A computed field decorator allows values
    @computed_field(SetField(StringField()), deps=[bio])
    def keywords(obj):
        return set(obj.get('bio', '').split(' '))

    kw_index = Index().ascending('keywords')
    name_index = Index().descending('first_name').ascending('last_name')
    email_index = Index().descending('email').unique()

    def __eq__(self, other):
        return self.email == other.email

    def __repr__(self):
        return 'User(email="%s")' % self.email

me = User(first_name='Jeff', last_name='Jenkins', email='jeff@qcircles.net',
        bio="Jeff is the author of MongoAlchemy")

print "================="
print me.keywords

# This connections to the DB and starts the session
session = Session.connect('mongoalchemy-intro')
session.clear_collection(User) # clear previous runs of this code!

# Insert on a sesion will infer the correct collection and push the object
# into the database
session.insert(me)
set(['author', 'of', 'is', 'Jeff', 'MongoAlchemy', 'the'])
# Get a user wirh me's email addresss and MongoAlchemy in their bio (via
# keywords)
db_user = session.query(User).filter(User.email ==
'jeff@qcircles.net').in_(User.keywords, 'MongoAlchemy').one()
print "================="
print db_user == me

# Using filter_by for simple equality checking is easier
print session.query(User).filter_by(email='jeff@qcircles.net').in_(User.keywords, 'MongoAlchemy').one()
# It's also possible to do raw mongo filtering
print session.query(User).filter({'email':'jeff@qcircles.net'}, {'keywords':{'$in':['MongoAlchemy']}}).one()
