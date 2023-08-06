### Todo
Add time partitioning in `def create_bq_table`
default:
table.partitioning_type = 'DAY'
when query will use `_PARTITIONTIME` when query, it's record UTC date when the data is loaded
            
custom column:
table.partitioning_type = 'DAY'
table.time_partitioning.field = 'ORDER_DATE'

### Changelog
- **Version 2.0.0**:
  - Change all of the API code
  - Allowed to set detailed configuration for schema of a BigQuery table
  - Added more features to work with BigQuery
- **Version 2.0.1**:
  - Changed some methods to become `staticmethod`
- **Version 2.0.2**:
  - Fixed minor error
- **Version 2.0.3**:
  - Added new method `generate_dummy_schema_from_df` to generrate dummy schema from pandas DataFrame
- **Version 2.0.4**:
  - Allowed to create Hive partitions
- **Version 2.0.5**:
  - Unloaded the pyodbc in default connectors
- **Version 2.0.9**:
  - Added a static method to get the full qualified table name
- **Version 2.1.0**:
  - Added a method to update target schema with ease
- **Version 2.1.1**:
  - Added Biglake connection support
    The steps to work with Biglake = 
    - Create an external connection
    - Get the `service account` from the connection and add to IAM
    - Try create a BigLake manually using the command below
    ```sql
    create or replace external table `gap-central-group.ssp_mdc.catalog_product_entity_datetime`
    (
      value_id INTEGER,
      attribute_id INTEGER,
      store_id INTEGER,
      row_id INTEGER,
      value INTEGER
    )
    With connection `nplearn.asia-southeast1.biglake-connection`
    options (
      format='PARQUET',
      uris=['gs://ssp_datasource/ssp_mdc/catalog_product_entity_datetime/*']
    );
    ```
    - now you can use the code to do it `test_create_biglake.py`
- **Version 2.1.2**:
  - Bug Fixed
- **Version 2.1.3**:
  - Bug Fixed
- **Version 2.1.4**:
  - Bug Fixed
- **Version 2.1.5**:
  - Improve readability
- **Version 2.1.6**:
  - Changed log name
- **Version 2.1.7**:
  - Updated log table
- **Version 2.1.8**:
  - Disable log table dependency


  
