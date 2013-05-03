from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# these imports are for custom SQL constructs
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


# create a custom utcnow function
class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


Base = declarative_base()


class AppMixin(object):
    """
    Provide common attributes to our models
    In this case, lowercase table names, timestamp, and a primary key column
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __mapper_args__ = {'always_refresh': True}

    id = Column(Integer, primary_key=True)
    # the correct function is automatically selected based on the dialect
    timestamp = Column(DateTime, server_default=utcnow())


class Tweets(Base, AppMixin):
    """ tweets """
    username = Column(
        String(50),
        nullable=False,
        unique=False)
    content = Column(
        String(200),
        nullable=False,
        unique=False)
    coordinates = Column(
        String(50),
        nullable=True)
    tweet_id = Column(
        String(20),
        nullable=False,
        unique=True)

    def __init__(self, **kwargs):
        self.username = kwargs.get("username")
        self.content = kwargs.get("content")
        self.tweet_id = kwargs.get("tweet_id")
        if kwargs.get('coordinates'):
            converted = (
                str(crd).encode("utf-8") for crd in kwargs.get("coordinates")['coordinates'][::-1])
            self.coordinates = ", ".join(converted)

    def __repr__(self):
        txt = u"Tweet: %s\nUser: %s\nOn the %s" % (
            self.content,
            self.username,
            self.timestamp.strftime("%d/%m/%Y at %H:%M"))
        return txt.encode("utf8")

    @property
    def permalink(self):
        return "https://twitter.com/%s/status/%s" % (
            self.username,
            self.tweet_id)


def sync():
    """
    Connect to the DB, return a usable session
    """
    # first, bind to or create the db
    engine = create_engine(
        'postgresql://streamer:streamer@localhost/tweetstream',
        encoding="utf8")
    # create the tables by syncing metadata from the models
    # Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
