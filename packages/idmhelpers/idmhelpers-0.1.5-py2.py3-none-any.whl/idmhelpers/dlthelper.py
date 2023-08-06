#from idmhelpers.dlthelper import setDefaultStorage, getDLTTasks
# Delta Live Metadata framework
# To store tables outside the pipeline storage use,
# setDefaultStorage(path)

import dlt
from pyspark.sql.types import StructType
from pyspark.sql.functions import collect_list
global spark

storage = None


def setDefaultStorage(path):
    storage = path


def createNestedFrame(df1, name, keycolumns=[], partitionkeys=[]):
    newcolumns = []
    newcolumns.extend(keycolumns)
    newcolumns.append(name)

    # Do not put key joining columns into nested structures
    nonkeycolumns = list(set(df1.columns)-set(keycolumns)-set(partitionkeys))

    df = df1.withColumn(name, struct(nonkeycolumns)).select(newcolumns)
    df = df.groupby(keycolumns).agg(collect_list(name).alias(name))
    return df


def getDLTTasks(name, sql, type="sql-view", comment="", temporary=True,
                nested=None, spark_conf=None, table_properties=None, path=None,
                partition_cols=None, schema=None):
    kwargs = {}
    # Define a Live Table
    if type == "dlt-table":
        # Create Keyword Args for dlt.table
        if path == None:
            if storage != None:
                path = f'{storage}/{name}'
        if path != None:
            kwargs.update({'path': path})
        if schema != None:
            kwargs.update({'schema': schema})
        if spark_conf != None:
            kwargs.update({'spark_conf': spark_conf})
        if table_properties != None:
            kwargs.update({'table_properties': table_properties})
        if partition_cols != None:
            kwargs.update({'partition_cols': partition_cols})
        kwargs.update({'name': name})
        kwargs.update({'comment': f"SQL:{name}:{comment}"})
        kwargs.update({'temporary': temporary})

        @dlt.table(**kwargs)
        def define_dlt_table():
            print(f'Live table: {name} ({comment}) {path})')
            df = spark.sql(sql)
            return df
    # Define a Live View
    if type == "dlt-view":
        @dlt.view(
            name=f"{name}",
            comment=f"SQL:{name}:{comment}"
        )
        def define_dlt_table():
            print(f'Live view: {name} ({comment})')
            df = spark.sql(sql)
            return df
    # Create a nested table - which folds sale line items into a table with a order,lineitem array.
    if type == "dlt-nest":
        if nested == None:
            raise Exception(
                f'{name} uses dlt-nest but is missing the nested attribute.')

        @dlt.view(
            name=f"{name}",
            comment=f"SQL:Nested:{name}:{comment}"
        )
        def define_nested_table():
            print(f'Live view: {name} ({comment})')
            df = spark.sql(sql)
            df_n = createNestedFrame(
                df, nested['name'], nested['keycolumns'], nested['partitionkeys'])
            return df_n
