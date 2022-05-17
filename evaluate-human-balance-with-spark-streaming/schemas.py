from pyspark.sql.types import StructField, StructType, StringType, BooleanType, ArrayType, DateType, FloatType

radisEventSchema = StructType([
    StructField("key", StringType()),
    StructField("existType", StringType()),
    StructField("Ch", BooleanType()),
    StructField("Incr", BooleanType()),
    StructField("zSetEntries", ArrayType(
        StructType([
            StructField("element", StringType()),
            StructField("Score", StringType())
        ])
    ))
])

customerSchema = StructType([
    StructField("customer", StringType()),
    StructField("score", StringType()),
    StructField("email", StringType()),
    StructField("birthYear", StringType())
])

stediEventSchema = StructType([
    StructField("customer", StringType()),
    StructField("score", FloatType()),
    StructField("riskDate", DateType())
])
