import sqlite3
import datetime
import bcrypt

DATABASE_NAME = "database.db"


class BaseModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get(cls, **kwargs):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        conditions = " AND ".join(["{} = ?".format(key) for key in kwargs])
        sql = """
        SELECT *
        FROM {}
        WHERE {}
        """.format(cls.__name__, conditions)
        cursor.execute(sql, tuple(kwargs.values()))

        row = cursor.fetchone()

        if row:
            instance = cls(**{cursor.description[i][0]: value for i, value in enumerate(row)})  # noqa: E501
        else:
            instance = None

        connection.close()

        return instance

    def save(self):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        table_exists = cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (self.__class__.__name__,)
        ).fetchone() is not None

        if not table_exists:
            columns = ', '.join([f'{key} {value.to_sql()}' for key, value in self.__class__.__dict__.items() if isinstance(value, Field)])  # noqa: E501
            create_table_sql = f"CREATE TABLE {self.__class__.__name__} ({columns})"  # noqa: E501
            cursor.execute(create_table_sql)

        columns = ', '.join(self.__dict__.keys())
        placeholders = ', '.join(['?'] * len(self.__dict__.values()))
        insert_sql = f"INSERT INTO {self.__class__.__name__} ({columns}) VALUES ({placeholders})"  # noqa: E501
        cursor.execute(insert_sql, tuple(self.__dict__.values()))

        connection.commit()
        connection.close()

    def delete(self):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        sql = """
        DELETE FROM {}
        WHERE name = ?
        """.format(self.__class__.__name__)
        cursor.execute(sql, (self.name,))

        connection.commit()
        connection.close()

    def update(self, **kwargs):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        for key, value in kwargs.items():
            sql = """
            UPDATE {}
            SET {} = ?
            WHERE name = ?
            """.format(self.__class__.__name__, key)
            cursor.execute(sql, (value, self.name))

        connection.commit()
        connection.close()

    def filter(self, **kwargs):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        conditions = ' AND '.join(["{} = ?".format(key) for key in kwargs])
        sql = """
        SELECT *
        FROM {}
        WHERE {}
        """.format(self.__class__.__name__, conditions)
        cursor.execute(sql, tuple(kwargs.values()))

        results = []
        for row in cursor.fetchall():
            instance = self.__class__(**{cursor.description[i][0]: value for i, value in enumerate(row)})  # noqa: E501
            results.append(instance)

        connection.close()

        return results

    def print_create_table_sql(self):
        columns = []
        for key, value in self.__class__.__dict__.items():
            if isinstance(value, Field):
                column = f"{key} {value.to_sql()}"
                columns.append(column)
        columns_sql = ", ".join(columns)
        create_table_sql = f"CREATE TABLE {self.__class__.__name__} ({columns_sql})"  # noqa: E501
        print(create_table_sql)


# < Field Type >


class Field:
    def __init__(
        self,
        max_length=None,
        null=None,
        default=None,
        primary_key=False,
        unique=False,
        auto_increment=False,
        on_delete=None,
        on_update=None,
    ):
        self.null = null
        self.default = default
        self.primary_key = primary_key
        self.unique = unique
        self.auto_increment = auto_increment
        self.on_delete = on_delete
        self.on_update = on_update

    def to_sql(self):
        sql = ""
        if self.null is not None:
            sql += "NULL"
        if self.default is not None:
            sql += f" DEFAULT '{self.default}'"
        if self.primary_key:
            sql += " PRIMARY KEY"
        if self.unique:
            sql += " UNIQUE "
        if self.on_delete is not None:
            sql += f" ON DELETE {self.on_delete}"
        if self.on_update is not None:
            sql += f" ON UPDATE {self.on_update}"
        return sql.strip()


class CharField(Field):
    def __init__(self, max_length, **kwargs):
        super().__init__(**kwargs)
        self.max_length = max_length

    def to_sql(self):
        sql = f"VARCHAR({self.max_length}) "
        sql += super().to_sql()
        return sql.strip()


class IntegerField(Field):
    def to_sql(self):
        sql = "INTEGER"
        if self.auto_increment:
            if self.primary_key:
                sql += " PRIMARY KEY AUTOINCREMENT"
            else:
                raise ValueError("AUTOINCREMENT can only be used with PRIMARY KEY")  # noqa: E501
        return sql.strip()


class ForeignKey(Field):
    def __init__(self, to, on_delete='CASCADE', **kwargs):
        super().__init__(**kwargs)
        self.to = to
        self.on_delete = on_delete

    def to_sql(self):
        sql = f"FOREIGN KEY REFERENCES {self.to} ON DELETE {self.on_delete}"
        sql += super().to_sql()
        return sql.strip()


class DateTimeField(Field):
    def __init__(self, auto_now_add=False, **kwargs):
        super().__init__(**kwargs)
        self.auto_now_add = auto_now_add

    def to_sql(self):
        sql = "DATETIME"
        if self.auto_now_add:
            sql = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        sql += super().to_sql()
        return sql.strip()


class DateField(Field):
    def __init__(self, auto_now_add=False, **kwargs):
        super().__init__(**kwargs)
        self.auto_now_add = auto_now_add

    def to_sql(self):
        sql = "DATE"
        sql += super().to_sql()
        return sql.strip()

    def get_current_date(self):
        return datetime.date.today()

    def get_auto_now_add_value(self):
        if self.auto_now_add:
            return self.get_current_date()
        return None


class BooleanField(Field):
    def __init__(self, default=None, **kwargs):
        super().__init__(**kwargs)
        self.default = default

    def to_sql(self):
        sql = "BOOLEAN"
        if self.default is not None:
            default_value = "TRUE" if self.default else "FALSE"
            sql += f" DEFAULT {default_value}"
        return sql.strip()


class PasswordField(Field):
    def __init__(self, max_length, encrypt=True, **kwargs):
        self.max_length = max_length
        super().__init__(**kwargs)
        self.encrypt = encrypt
        self.value = None

    def __set__(self, instance, value):
        if self.encrypt:
            self.value = self.hash_password(value)
        else:
            self.value = value

    def __get__(self, instance, owner):
        return self.value

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode()

    def verify_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def to_sql(self):
        sql = f"VARCHAR({self.max_length})"
        sql += super().to_sql()
        return sql.strip()


class FloatField(Field):
    def to_sql(self):
        sql = "REAL"
        sql += super().to_sql()
        return sql.strip()
