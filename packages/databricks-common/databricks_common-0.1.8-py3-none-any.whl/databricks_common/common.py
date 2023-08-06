from abc import ABC, abstractmethod
from argparse import ArgumentParser
from typing import Dict, Any
from logging import Logger

from databricks_common.utils.logger_utils import get_logger
from databricks_common.utils.get_spark import spark

_logger = get_logger()


class MetastoreTable:  # TODO: Add tests, add shallow/deep delta clone function
    """
    Class representing a table in the Unity Catalog Metastore. This class is used to reference tables,
    and perform operations on them. It is NOT a DataFrame.
    It offers functionality such as:
    - Checking that the table exists
    - Describing the table
    - Describing the table history
    - Describing the table extended
    - Read the table as a Spark DataFrame
    """

    def __init__(self, name: str, catalog: str, schema: str) -> None:
        self.name = name
        self.catalog = catalog
        self.schema = schema
        self.ref = self._get_ref()
        self.short_ref = self._get_short_ref()
        self.schema_ref = self._get_schema_ref()

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}({self.ref})"

    @classmethod
    def from_string(cls, table_ref: str) -> "MetastoreTable":
        """
        Alternative constructor to initialise a TableReference object from a string.
        """
        cat, schema, name = table_ref.split(".")
        return cls(name=name, catalog=cat, schema=schema)

    def check_exists_depr(self) -> bool:
        MetastoreCatalog(self.catalog).set()
        return spark.catalog.tableExists(self.short_ref)

    def check_exists(self) -> bool:
        try:
            spark.sql(f"DESC TABLE {self.ref}")
            return True
        except Exception as e:
            return False

    def drop(self) -> None:
        spark.sql(f"DROP TABLE {self.ref}")

    def drop_if_exists(self) -> None:
        if self.check_exists():
            self.drop()

    def _create_basic_table(self, comment: str = "") -> None:
        """
        Function to create a basic table at self.ref
        """
        spark.sql(
            f"""
        CREATE TABLE {self.ref}  
            (id INT, name STRING, value DOUBLE);  
        """
        )

        spark.sql(
            f"""
        INSERT INTO {self.ref}
            VALUES (1, "Yve", 1.0), 
                (2, "Omar", 2.5), 
                (3, "Elia", 3.3)
        """
        )

    def _create(self, comment: str = "") -> None:
        """
        Function to create a table in the catalog. Not intended to be used other than to create a table with the name.
        Most of the time you'll be creating tables directly in your code and won't need this function.
        """
        spark.sql(
            f"""
            CREATE TABLE {self.ref}
            USING DELTA
            COMMENT '{comment}'
            """
        )

    def create_parents_if_not_exists(self) -> None:
        MetastoreCatalog(self.catalog).create_if_not_exists()
        MetastoreSchema.from_string(self.schema_ref).create_if_not_exists()

    def describe(self) -> None:
        spark.sql(f"DESC TABLE {self.ref}").display()

    def describe_extended(self) -> None:
        spark.sql(f"DESC EXTENDED {self.ref}").display()

    def describe_history(self) -> None:
        spark.sql(f"DESC HISTORY {self.ref}").display()

    def read(self):  # noqa
        return spark.read.table(self.ref)

    def _get_ref(self) -> str:
        return f"{self.catalog}.{self.schema}.{self.name}"

    def _get_short_ref(self) -> str:
        return f"{self.schema}.{self.name}"

    def _get_schema_ref(self) -> str:
        return f"{self.catalog}.{self.schema}"

    def _get_checkpoint_location(
        self,
    ) -> (
        str
    ):  # TODO: Still in dev. Need to understand if a table has metadata about it's checkpoint location.
        try:
            return self.checkpoint_location
        except AttributeError:
            return f"{self.catalog}.chkpts/{self.schema}/{self.name}"


class MetastoreCatalog:
    """
    Class representing a catalog in the Unity Catalog Metastore. This class is used to reference catalogs
    and perform operations on them. It offers functionality such as:
    - Checking that the catalog exists
    - Creating a catalog
    - Creating a catalog in a managed location
    - Creating a schema in a catalog
    - Describing a catalog
    - Describing a catalog in extended format
    - Dropping a catalog
    - Showing the available schemas in a catalog
    - For demo purposes, creating a catalog in a managed location
    """

    def __init__(self, name) -> None:
        self.name = name

    def check_exists(self) -> bool:
        try:
            spark.sql(f"DESC CATALOG {self.name}")
            return True
        except (
            Exception
        ) as e:  # TODO: Choose specific exception in case there is a specific error
            return False

    def create(self, comment: str = "") -> None:
        spark.sql(f"CREATE CATALOG {self.name} COMMENT '{comment}'")

    def create_if_not_exists(self, comment: str = "") -> None:
        if self.check_exists():
            # Had to include explicit check due to QUOTA_EXCEEDED error.
            pass
        else:
            spark.sql(f"CREATE CATALOG IF NOT EXISTS {self.name} COMMENT '{comment}'")

    def create_schema(self, schema_name: str, comment: str = "") -> None:
        spark.sql(f"CREATE SCHEMA {self.name}.{schema_name} COMMENT '{comment}'")

    def create_catalog_in_managed_location(
        self, location_path: str = None, comment: str = ""
    ) -> None:
        spark.sql(
            f"""
            CREATE CATALOG {self.name}
            MANAGED LOCATION '{location_path}'
            COMMENT '{comment}' 
            """
        )

    def demo_create_managed_external_catalog(self) -> None:  # TODO: Convert to test
        """
        Function for demo purposes.
        """
        self.create_catalog_in_managed_location(
            location_path="abfss://xavierarmitage-container@oneenvadls.dfs.core.windows.net",
            container_dir="lake23",
            comment="Demo comment",
        )

    def describe(self) -> None:
        spark.sql(f"DESC CATALOG {self.name}").display()

    def describe_extended(self) -> None:
        spark.sql(f"DESC CATALOG EXTENDED {self.name}").display()

    def drop(self, cascade=False) -> None:
        if cascade:
            spark.sql(f"DROP CATALOG {self.name} CASCADE")
        else:
            spark.sql(f"DROP CATALOG {self.name}")

    def drop_if_exists(self, cascade=False) -> None:
        if cascade:
            spark.sql(f"DROP CATALOG IF EXISTS {self.name} CASCADE")
        else:
            spark.sql(f"DROP CATALOG IF EXISTS {self.name}")

    def drop_cascade(self) -> None:
        self.drop(cascade=True)

    def drop_schema(self, cascade: bool = False):
        self.set()
        _logger.info(f"Dropping schema '{self.name}'")
        if cascade:
            spark.sql(f"DROP SCHEMA IF EXISTS {self.name} CASCADE")
        else:
            spark.sql(f"DROP SCHEMA IF EXISTS {self.name}")

    def set(self) -> None:
        spark.sql(f"SET CATALOG {self.name}")

    def show_schemas(self) -> None:
        self.set()
        spark.sql("SHOW SCHEMAS").display()


class MetastoreSchema:
    """
    Class to represent a schema in Unity Metastore.
    """

    def __init__(self, name: str, catalog: str | MetastoreCatalog) -> None:
        if isinstance(catalog, MetastoreCatalog):
            self.catalog = catalog.name
        else:
            self.catalog = catalog
        self.name = name
        self.ref = self._get_ref()

    @classmethod
    def from_string(cls, ref: str) -> "MetastoreSchema":
        """
        Alternative constructor to initialise an MetastoreSchema from a string.
        """
        cat, schema = ref.split(".")
        return cls(name=schema, catalog=cat)

    def _set_catalog(self) -> None:
        """
        Function to set the current catalog.
        """
        MetastoreCatalog(self.catalog).set()

    def check_exists(self) -> bool:
        """
        Function to check if a schema exists in Unity Metastore.
        """
        # TODO: There might be a more direct way to do this
        try:
            spark.sql(f"DESC SCHEMA {self.catalog}.{self.name}")
            return True
        except Exception as e:
            # TODO: update to make exception more specific
            return False

    def create(self, comment: str = "") -> None:
        spark.sql(f"CREATE SCHEMA {self.ref} COMMENT '{comment}'")

    def create_if_not_exists(self, comment: str = "") -> None:
        spark.sql(f"CREATE SCHEMA IF NOT EXISTS {self.ref} COMMENT '{comment}'")

    def describe(self) -> None:
        spark.sql(f"DESC SCHEMA {self.ref}").display()

    def describe_extended(self) -> None:
        spark.sql(f"DESC SCHEMA EXTENDED {self.ref}").display()

    def drop(self, cascade: bool = False) -> None:
        if cascade:
            spark.sql(f"DROP SCHEMA {self.ref} CASCADE")
        else:
            spark.sql(f"DROP SCHEMA {self.ref}")

    def drop_if_exists(self, cascade: bool = False) -> None:
        if cascade:
            spark.sql(f"DROP SCHEMA IF EXISTS {self.ref} CASCADE")
        else:
            spark.sql(f"DROP SCHEMA IF EXISTS {self.ref}")

    def show_tables(self) -> None:
        spark.sql(f"SHOW TABLES IN {self.ref}").display()

    def set(self) -> None:
        spark.sql(f"SET SCHEMA {self.ref}")

    def _get_ref(self) -> str:
        return f"{self.catalog}.{self.name}"
