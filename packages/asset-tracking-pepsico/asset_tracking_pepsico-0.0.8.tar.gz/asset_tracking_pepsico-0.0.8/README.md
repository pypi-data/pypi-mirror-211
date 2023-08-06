# audit_logging_pepsico

Under Construction.
A DTO for transforming the data coming from different sources into a single object or schema.
This will be used to write the data to postgres. 

Developed by Jatin Talati

## Examples of How To Use

```python
from asset_tracking_pepsico.asset_tracking_ingest import AssetTrackingIngest
from asset_tracking_pepsico import utilities

blob_conn_str = "<BLOB_CONNECTION_STRING>"
container_name = "<NAME_OF_THE_CONTAINER>"
blob_name = "<NAME_OF_THE_BLOB>"

ast = AssetTrackingIngest()
data = utilities.read_data_from_blob(blob_conn_str, container_name, blob_name)
# Other Code
```

For accessing the schema and parameters use the following code

```python
from asset_tracking_pepsico.dto.PostgresSchema import PostgresSchemaDto

schema = PostgresSchemaDto()
print(schema.__str__())
```

This will print out the values for all the parameters in the class.
For dict you can use
```python
print(schema.__dict__())
```
Explore the package to use other functions and parameters. 
