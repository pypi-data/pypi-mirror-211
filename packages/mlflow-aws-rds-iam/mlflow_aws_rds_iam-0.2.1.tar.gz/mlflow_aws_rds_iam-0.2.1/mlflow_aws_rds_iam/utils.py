"""Utility module for database driver support."""
from sqlalchemy.engine import URL

try:
    from enum import StrEnum
except ImportError:  # pragma: no cover (only for Python 3.10 support)
    from strenum import StrEnum  # type: ignore[import,no-redef]


class DatabaseType(StrEnum):
    """Supported drivers."""

    POSTGRESQL = "postgresql"
    MYSQL = "mysql"


DB_DEFAULT_PORT: dict[DatabaseType, int] = {
    DatabaseType.POSTGRESQL: 5432,
    DatabaseType.MYSQL: 3306,
}


def get_db_type(uri: URL) -> DatabaseType:
    """Get the database driver for a URI, raise for unsupported driver."""
    try:
        return DatabaseType(uri.drivername.split("+")[0])
    except ValueError:
        raise ValueError(
            f"Database driver is '{uri.drivername}' but RDS IAM auth plugins for MLflow"
            f" only support drivers: {', '.join(str(dt) for dt in DatabaseType)}."
        )


def get_db_default_port(uri: URL) -> int:
    """Get the default port for supproted database drivers."""
    return DB_DEFAULT_PORT[get_db_type(uri)]
