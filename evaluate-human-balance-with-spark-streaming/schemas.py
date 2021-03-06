from pyspark.sql.types import StructField, StructType, StringType, BooleanType, ArrayType, DateType, FloatType

radisSchema = StructType([
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

riskEventSchema = StructType([
    StructField("customer", StringType()),
    StructField("score", FloatType()),
    StructField("riskDate", DateType())
])


def get_customer_schema(birth_type='day'):
    if birth_type == 'day':
        return StructType([
            StructField("customerName", StringType()),
            StructField("score", StringType()),
            StructField("email", StringType()),
            StructField("birthDay", StringType())
        ])
    if birth_type == 'year':
        StructType([
            StructField("customerName", StringType()),
            StructField("score", StringType()),
            StructField("email", StringType()),
            StructField("birthYear", StringType())
        ])

    return None
