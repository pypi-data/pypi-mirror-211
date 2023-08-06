from sqlalchemy.dialects import registry
from .base import BaseDialect
from .log import class_logger, mtd_logger


@class_logger
class SnowflakeDBSDialect(BaseDialect):
  name = "snowflake"
  driver = "cdata.snowflake"

  supports_unicode_statements = True
  supports_unicode_binds = True
  postfetch_lastrowid = True

  support_native_decimal = True
  default_paramstyle = "qmark"

  _connection_string_keyword = "connection_String"

  @classmethod
  def dbapi(cls):
    return __import__(cls.driver, fromlist=cls.name)

  @mtd_logger
  def connect(self, *args, **kwargs):
    if self._connection_string_keyword in kwargs:
      connStr = kwargs[self._connection_string_keyword]
      return self.dbapi.connect(connStr)

    raise ValueError("Invalid connection string.")

  @mtd_logger
  def create_connect_args(self, url):
    args = []
    # user
    if hasattr(url, "username") and url.username:
      args.append("user")
      args.append("=")
      args.append(url.username)
      args.append(";")

    # password
    if hasattr(url, "password") and url.password:
      args.append("password")
      args.append("=")
      args.append(url.password)
      args.append(";")

    # server
    if hasattr(url, "host") and url.host:
      args.append("server")
      args.append("=")
      args.append(url.host)
      args.append(";")

    # port
    if hasattr(url, "port") and url.port:
      args.append("port")
      args.append("=")
      args.append(str(url.port))
      args.append(";")

    # database
    if hasattr(url, "database") and url.database:
      args.append("database")
      args.append("=")
      args.append(url.database)
      args.append(";")

    for key in url.query.keys():
      args.append(key)
      args.append("=")
      args.append(url.query[key])
      args.append(";")

    return (), {
      self._connection_string_keyword: "".join(args)
    }

  @mtd_logger
  def is_disconnect(self, e, connection, cursor):
    if isinstance(e, self.dbapi.ProgrammingError):
      return str(e).startswith("Attempt to use a closed")

    return False

  @mtd_logger
  def do_execute(self, cursor, statement, parameters, context=None):
    """Provide an implementation of
    *cursor.execute(statement, parameters)*."""
    if parameters:
      return cursor.execute(statement, parameters)

    return cursor.execute(statement)

  @mtd_logger
  def do_close(self, dbapi_connection):
    dbapi_connection.close()

  @mtd_logger
  def _check_unicode_returns(self, connection):
    return True

  @mtd_logger
  def _check_unicode_description(self, connection):
    return True

