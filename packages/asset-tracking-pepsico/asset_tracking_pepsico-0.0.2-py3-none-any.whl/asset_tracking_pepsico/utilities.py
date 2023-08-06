import traceback
import psycopg2
from azure.storage.blob import BlobServiceClient


def get_block_blob_client(blob_conn_str, container_name, blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(conn_str=blob_conn_str)
        container_client = blob_service_client.get_container_client(container_name)
        block_blob_client = container_client.get_blob_client(blob_name)
        return block_blob_client
    except:
        traceback.print_exc()


def read_data_from_blob(blob_conn_str, container_name, blob_name):
    try:
        blob_client = get_block_blob_client(blob_conn_str, container_name, blob_name)
        file_name = blob_client.download_blob()
        blob_data = file_name.readall()
        return blob_data
    except:
        traceback.print_exc()


def read_file(filename):
    try:
        with open(filename) as f:
            filedata = f.read()
        f.close()
        return filedata
    except:
        traceback.print_exc()


def get_string_from_schema_list(schema_list):
    try:
        str_list = [i.__str__() for i in schema_list]
        return str_list
    except:
        traceback.print_exc()


# Get a connection to a new postgres server using the connection string.
def get_conn(postgre_conn_str):
    try:
        conn = psycopg2.connect(postgre_conn_str)
        cursor = conn.cursor()
        return cursor, conn
    except:
        traceback.print_exc()

# Commit all transactions and close the connection
def close_connection(conn):
    try:
        conn.commit()
        conn.close()
    except:
        traceback.print_exc()


# format the query to form an sql query
def format_query(query):
    try:
        start_pos = query.find("None, '{") + len("None, '{")
        end_pos = query.find("}'")
        substring = query[start_pos:end_pos]
        new_substring = substring.replace("'", '"')
        updated_query = query[:start_pos] + new_substring + query[end_pos:]
        updated_query = updated_query.replace('None', 'NULL')
        return updated_query
    except:
        traceback.print_exc()

# generate an insert query based on the table name and the columns
def generate_insert_query(table_name, schema, columns):
    try:
        query = f'''INSERT INTO {table_name} ({columns}) VALUES ({schema.__str__()})'''
        query = format_query(query)
        print("QUERY === ", query, type(query))
        return query
    except:
        traceback.print_exc()

# write the data to postgres
def write_data(postgre_conn_str, table_name, schema_list, columns):
    try:
        rows_affected = []
        cursor, conn = get_conn(postgre_conn_str)
        for schema in schema_list:
            print('-' * 100 + "\nwriting to postgres === ", schema.__str__() + "\n" + '-' * 100)
            query = generate_insert_query(table_name, schema, columns)
            cursor.execute(query)
            rows_affected.append(cursor.rowcount)
            conn.commit()
        close_connection(conn)
        return rows_affected
    except:
        traceback.print_exc()
