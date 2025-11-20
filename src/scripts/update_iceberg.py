import os

import pyarrow as pa
from pyiceberg.catalog import load_catalog
from pyiceberg.expressions import EqualTo

os.environ["PYICEBERG_HOME"] = os.getcwd()  # cwd: current working directory
print(os.getenv("PYICEBERG_HOME"))
catalog = load_catalog(name="postgres")
print(catalog.properties)

table = catalog.load_table("siak.dim_room")
print(table.schema())
# query table by id
df = table.scan().to_pandas()
df_sorted = df.sort_values(by=["room_id"])
print(df_sorted)
# new_data_room = pa.Table.from_pylist(
#     [
#         {"room_id": 200, "building": "Rhodos Island", "capacity": 200},
#     ],
#     schema=table.schema().as_arrow(),
# )

# table.append(new_data_room)
# print(table.scan(row_filter=EqualTo("room_id", 200)).to_pandas())

# --- UPDATE DATA ---
# Query for the row to update.
id_200_tbl = table.scan(row_filter=EqualTo("room_id", 2)).to_arrow()

# Determine the index of the value column and retrieve the column's field
value_column_index = id_200_tbl.column_names.index("capacity")
value_column_field = id_200_tbl.field(value_column_index)

# Create an array with the same length as the table
# If you only want to update one specific row, you need to provide values for all matching rows
num_rows = len(id_200_tbl)
new_capacity_values = [6969] * num_rows  # Repeat the value for all matching rows

# Modify the resulting PyArrow table by replacing the value column
id_200_tbl = id_200_tbl.set_column(
    value_column_index,
    value_column_field,
    pa.array(new_capacity_values, type=pa.int32()),  # Ensure the data types align
)

# Update the Iceberg table by overwriting the row
table.overwrite(df=id_200_tbl, overwrite_filter=EqualTo("room_id", 2))
df = table.scan().to_pandas()
df_sorted = df.sort_values(by=["room_id"])
print(df_sorted)

# --- DELETE DATA ---
# table.delete(delete_filter=EqualTo("room_id", 101))
# df = table.scan().to_pandas()
# df_sorted = df.sort_values(by=["room_id"])
# print(df_sorted)
