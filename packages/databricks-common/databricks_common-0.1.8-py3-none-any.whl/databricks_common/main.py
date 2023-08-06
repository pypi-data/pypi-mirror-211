from databricks.connect import DatabricksSession
from databricks.sdk.core import Config


config = Config(profile="aws-e2-demo")
# config = Config(profile="azure-field-eng-east")
spark = DatabricksSession.builder.sdkConfig(config).getOrCreate()
print(spark)
