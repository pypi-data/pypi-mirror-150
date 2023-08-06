from npgbq.core.helper_phone_number_th import format_phone
from datetime import datetime
import os
import platform
from google.cloud import bigquery
import pandas as pd
import numpy as np
import decimal
import re
import uuid
import decimal


class np_gbq(object):
    def __init__(self, gbq_service_account_path):
        self.path_json_key = gbq_service_account_path
        # var default
        self.__log_dataset = "log_npgbq"
        self.__log_table = "etl_log"
        self.job_uuid = None
        self.dataset_name = None
        self.table_name = None
        # update env
        self.__add_environment()
        self.bqclient = self.__get_bq_client()

    def __add_environment(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.path_json_key

    def __get_bq_client(self):
        client = bigquery.Client()
        return client

    # ====================================== Private method ======================================
    @classmethod
    def __get_valid_colname(cls, text):
        val = re.sub("[^A-Za-z0-9_]+", "", text)
        if re.search("^\d", val):
            val = f"_{val}"
        return val

    @staticmethod
    def get_valid_colname(text):
        return np_gbq.__get_valid_colname(text)

    def format_deciaml_cols(self, df, col_decimal):
        for col in col_decimal:
            df[col] = df[col].astype(str).map(decimal.Decimal)
        return df

    def __validate_col_type(self, text):
        valid_col_type = [
            "ARRAY",
            "BIGNUMERIC",
            "BOOL",
            "BYTES",
            "DATE",
            "FLOAT64",
            "FLOAT",
            "GEOGRAPHY",
            "INT64",
            "INTERVAL",
            "NUMERIC",
            "STRING",
            "TIME",
            "TIMESTAMP",
            "INTEGER",
            "BOOLEAN",
        ]
        if text not in valid_col_type:
            raise ValueError(f"the input column datatype {text} is not valid")
        # do type mapping if needed
        return text

    def __get_full_qualified_table_name(self, dataset_name, table_id):
        full_qualified_id = f"{self.bqclient.project}.{dataset_name}.{table_id}"
        return full_qualified_id

    def __get_db_connection(
        self,
        db_hostname_or_ip,
        db_port_number,
        db_database_name,
        db_username,
        db_password,
        engine="postgres",
    ):
        self.log2bq(
            message=f"making connection to database: {db_database_name}"
        )
        conn = None
        if engine == "postgres":
            conn = self._get_postgres(
                db_hostname_or_ip,
                db_port_number,
                db_database_name,
                db_username,
                db_password,
            )
        elif engine == "mssql":
            conn = self._get_mssql(
                db_hostname_or_ip,
                db_port_number,
                db_database_name,
                db_username,
                db_password,
            )
        else:
            raise NotImplementedError(
                f"your engine {engine} is invalid please contact the administrator"
            )
        self.log2bq(message=f"connection is ready: {db_database_name}")
        return conn

    def _get_postgres(
        self,
        db_hostname_or_ip,
        db_port_number,
        db_database_name,
        db_username,
        db_password,
    ):
        conn = psycopg2.connect(
            database=db_database_name,
            user=db_username,
            password=db_password,
            host=db_hostname_or_ip,
            port=db_port_number,
            connect_timeout=5,
        )
        return conn

    def _get_mssql(
        self,
        db_hostname_or_ip,
        db_port_number,
        db_database_name,
        db_username,
        db_password,
    ):
        protocal = "tcp"
        driver = "ODBC Driver 17 for SQL Server"
        server_name = f"{protocal}:{db_hostname_or_ip},{db_port_number}"
        connection_string = f"DRIVER={driver};SERVER={server_name};DATABASE={db_database_name};UID={db_username};PWD={db_password};"
        conn = pyodbc.connect(connection_string)
        return conn

    # ====================================== Public method ======================================
    def create_bq_dataset(self, dataset_name):
        try:
            dataset_id = f"{self.bqclient.project}.{dataset_name}"
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = "asia-southeast1"
            dataset = self.bqclient.create_dataset(dataset, timeout=30)
        except Exception as e:
            print(f"Can not create the dataset: {e}")
        else:
            print(f"Created dataset name {dataset_name}")

    def create_bq_table(self, dataset_name, table_id, schema):
        try:
            full_qualified_id = self.__get_full_qualified_table_name(
                dataset_name, table_id
            )
            table = bigquery.Table(full_qualified_id, schema=schema)
            table = self.bqclient.create_table(table)
        except Exception as e:
            print(f"Can not create table: {e}")
        else:
            print(f"Created the table name {table_id}")

    def create_log_table(self):
        schema_dict = {
            "hostname": "STRING",
            "job_uuid": "STRING",
            "dataset_name": "STRING",
            "table_name": "STRING",
            "message": "STRING",
            "is_error": "INT64",
            "create_timestamp": "TIMESTAMP",
        }
        schema = self.generate_bq_schema_from_dict(schema_dict)
        self.create_bq_dataset(self.__log_dataset)
        self.create_bq_table(
            self.__log_dataset, table_id=self.__log_table, schema=schema
        )

    def generate_bq_schema_from_dict(
        self, schema_dict, add_etl_cols=False, add_etl_filename=False
    ):
        schema = []
        for k, v in schema_dict.items():
            col_name = self.__get_valid_colname(k)
            col_type = self.__validate_col_type(v)
            # TODO[2021-11-17 17:00]: add option for null/notnull
            col_mode = "NULLABLE"
            schema.append(
                bigquery.SchemaField(col_name, col_type, mode=col_mode)
            )
        if add_etl_cols:
            if add_etl_filename:
                schema.append(
                    bigquery.SchemaField(
                        "etl_sourcefilename", "STRING", mode="REQUIRED"
                    )
                )
            schema.append(
                bigquery.SchemaField(
                    "etl_updatetime", "TIMESTAMP", mode="REQUIRED"
                )
            )
            schema.append(
                bigquery.SchemaField(
                    "etl_updatemode", "STRING", mode="REQUIRED"
                )
            )
        return schema

    def delete_bq_table(self, dataset_name, table_id):
        """
        Remove the target table from your dataset
        """
        full_qualified_id = self.__get_full_qualified_table_name(
            dataset_name, table_id
        )
        try:
            self.bqclient.delete_table(full_qualified_id, not_found_ok=True)
        except Exception as e:
            print(
                f"Failed to delete the table {full_qualified_id} with error {e}"
            )
        else:
            print(
                f"Deleted the table {table_id} from the dataset {dataset_name}"
            )

    def fix_none_null_value(self, df):
        df = df.where(pd.notnull(df), None)
        return df

    def get_mode_bq(self, mode):
        if mode in ("append", "incremental"):
            return "WRITE_APPEND"
        elif mode in ("truncate", "initial"):
            return "WRITE_TRUNCATE"
        else:
            raise ValueError(
                f"Invalid mode for inserting data to BigQuery: {mode}"
            )

    def insert_row(self, rows, dataset_name, table_name):
        full_qualified_id = self.__get_full_qualified_table_name(
            dataset_name, table_name
        )
        table = self.bqclient.get_table(full_qualified_id)
        errors = self.bqclient.insert_rows(table, rows)
        if errors:
            print(f"failed to insert the input row: {errors}")

    def __update_instance(self, dataset_name, table_id):
        self.dataset_name = dataset_name
        self.table_name = table_id
        self.job_uuid = str(uuid.uuid4())

    def log2bq(self, message="no input message", is_error=0):
        if self.job_uuid is None:
            self.__update_instance(
                dataset_name="no_dataset_name", table_id="no_table_name"
            )
        value = {
            "hostname": platform.uname().node,
            "job_uuid": self.job_uuid,
            "dataset_name": self.dataset_name,
            "table_name": self.table_name,
            "message": message,
            "is_error": is_error,
            "create_timestamp": datetime.now(),
        }
        value = [value]
        self.insert_row(value, self.__log_dataset, self.__log_table)

    def insert_dataframe_to_bq_table(
        self, df, dataset_name, table_id, schema, mode, update_instance=True
    ):
        """
        Insert the whole dataframe into BigQuery with proper schema

        mode['append','truncate']
        'append' = append data to the table
        'truncate' = remove all data from the table and write
        """
        # update value to the instace
        if update_instance:
            self.__update_instance(dataset_name, table_id)
        # ensure the data is good for bigquery
        df = self.fix_none_null_value(df)
        mode_bq = self.get_mode_bq(mode)
        full_qualified_id = self.__get_full_qualified_table_name(
            dataset_name, table_id
        )
        self.log2bq(
            message="loading data from input dataframe to the target table"
        )
        try:
            job_config = bigquery.LoadJobConfig(
                schema=schema, write_disposition=mode_bq
            )
            print(f"Inserting data to the table {full_qualified_id}")
            job = self.bqclient.load_table_from_dataframe(
                df, full_qualified_id, job_config=job_config
            )
            job.result()
        except Exception as e:
            raise ValueError(f"failed to insert data: {e}")
        else:
            print(f"successfully insert data to {full_qualified_id}")
            self.log2bq(
                message=f"successfully insert data to {full_qualified_id}"
            )
            return True

    def prepare_sql_query(self, sql, schema_name_src, table_name_src):
        if sql is None:
            sql = f"SELECT * FROM {schema_name_src}.{table_name_src}"
        print(f"Using the SQL command below")
        print(sql)
        return sql

    def clean_thai_phone(self, df: pd.DataFrame, col_phone):
        df.reset_index(drop=True, inplace=True)
        if col_phone:
            for c in col_phone:
                val = df[c].apply(format_phone).to_list()
                val = pd.DataFrame(val, columns=["phone_type", "phone_number"])
                df.loc[:, c] = val["phone_number"]
        return df

    def __getcsize(self, num):
        if num is None:
            return 100000
        else:
            return num

    def load_table_from_db(
        self,
        schema_name_src,
        table_name_src,
        dataset_name,
        table_name,
        schema_dict,
        loading_mode,
        db_engine,
        db_hostname_or_ip,
        db_port_number,
        db_database_name,
        db_username,
        db_password,
        sql=None,
        add_etl_cols=False,
        rename_dict=None,
        col_phone=None,
        csize=None,
    ):
        self.__update_instance(dataset_name, table_name)
        self.db = self.__get_db_connection(
            db_hostname_or_ip,
            db_port_number,
            db_database_name,
            db_username,
            db_password,
            engine=db_engine,
        )
        if loading_mode.lower() == "truncate":
            self.clear_table(dataset_name, table_name)
        sql = self.prepare_sql_query(sql, schema_name_src, table_name_src)
        self.log2bq(message="making a request to the target database")
        self.log2bq(message=sql)
        schema = self.generate_bq_schema_from_dict(
            schema_dict, add_etl_cols=add_etl_cols, add_etl_filename=False
        )
        dbcsize = self.__getcsize(csize)
        chunk_count = 0
        for df in pd.read_sql(sql, self.db, chunksize=dbcsize):
            df = self.remove_nulls(df)
            msg = f"found records of requested data: {df.shape[0]} for the chunk [{chunk_count}]"
            print(msg)
            self.log2bq(message=msg)
            if add_etl_cols:
                df["etl_updatetime"] = datetime.now()
                df["etl_updatemode"] = "INSERT"
                msg = f"added `etl_updatetime`, `etl_updatemode` to df"
                self.log2bq(message=msg)
            df = self.rename_columns(df, rename_col=rename_dict)
            dtype_config = self.generate_dtype_from_schema(schema_dict)
            df = self.clean_thai_phone(df, col_phone)
            df = self.convert_dtype(df, dtype_config)
            self.insert_dataframe_to_bq_table(
                df,
                dataset_name,
                table_name,
                schema,
                mode="append",
                update_instance=False,
            )
            chunk_count += 1

    def remove_nulls(self, df):
        df.fillna(np.nan, inplace=True)
        return df

    def load_table_from_postgres(
        self,
        schema_name_src,
        table_name_src,
        dataset_name,
        table_name,
        schema,
        loading_mode,
        db_hostname_or_ip,
        db_port_number,
        db_database_name,
        db_username,
        db_password,
        sql=None,
        add_etl_cols=False,
    ):
        self.__update_instance(dataset_name, table_name)
        self.db = self.__get_db_connection(
            db_hostname_or_ip,
            db_port_number,
            db_database_name,
            db_username,
            db_password,
            engine="postgres",
        )
        if sql is None:
            sql = f"SELECT * FROM {schema_name_src}.{table_name_src}"
        self.log2bq(message="making a request to the target database")
        self.log2bq(message=sql)
        df = pd.read_sql(sql, self.db)
        print(f"found records of requested data: {df.shape[0]}")
        self.log2bq(message=f"found records of requested data: {df.shape[0]}")
        if add_etl_cols:
            df["etl_updatetime"] = datetime.now()
            df["etl_updatemode"] = "INSERT"
            self.log2bq(
                message=f"added 2 etl_updatetime, etl_updatemode to the data"
            )
        print(df.head())
        self.insert_dataframe_to_bq_table(
            df,
            dataset_name,
            table_name,
            schema,
            loading_mode,
            update_instance=False,
        )

    def rename_columns(
        self, df: pd.DataFrame, lowercase_flag=False, rename_col=None
    ):
        if rename_col:
            df.rename(columns=rename_col, inplace=True)
        if lowercase_flag:
            df.columns = [c.lower() for c in df.columns]
        return df

    def load_table_from_s3(
        self,
        access_key,
        secret_key,
        bucket_name,
        dataset_name,
        table_name,
        schema_dict,
        s3_prefix,
        loading_mode,
        add_etl_cols,
        add_etl_filename,
        lower_colname=True,
        rename_col=None,
    ):
        self.__update_instance(dataset_name, table_name)
        schema = self.generate_bq_schema_from_dict(
            schema_dict,
            add_etl_cols=add_etl_cols,
            add_etl_filename=add_etl_filename,
        )
        self.create_bq_dataset(dataset_name)
        self.create_bq_table(dataset_name, table_id=table_name, schema=schema)
        self.s3 = self.get_s3_object(access_key, secret_key, bucket_name)
        s3_files = self.s3.list_file(s3_prefix)
        for s3_file in s3_files:
            df = self.read_data_from_s3(s3_filepath=s3_file)
            df = self.rename_columns(df, lower_colname, rename_col)
            df = self.manage_etl_columns(
                df, s3_file, add_etl_cols, add_etl_filename
            )
            dtype_config = self.generate_dtype_from_schema(schema_dict)
            df = self.convert_dtype(df, dtype_config)
            self.insert_dataframe_to_bq_table(
                df,
                dataset_name,
                table_name,
                schema,
                loading_mode,
                update_instance=False,
            )

    def manage_etl_columns(
        self, df, s3_file=None, add_etl_cols=True, add_etl_filename=False
    ):
        if add_etl_cols:
            if add_etl_filename:
                if s3_file is not None:
                    df["etl_sourcefilename"] = s3_file
                else:
                    raise ValueError(f"There is no input filename")
            df["etl_updatetime"] = datetime.now()
            df["etl_updatemode"] = "INSERT"
        return df

    def generate_dtype_from_schema(self, schema_dict):
        config = {
            "col_str": [],
            "col_bool": [],
            "col_ts": [],
            "col_dt": [],
            "col_int": [],
            "col_decimal": [],
            "col_float": [],
            "col_time": [],
        }
        for k, v in schema_dict.items():
            if v in ["STRING"]:
                config["col_str"].append(k)
            elif v in ["DATE"]:
                config["col_dt"].append(k)
            elif v in ["TIMESTAMP"]:
                config["col_ts"].append(k)
            elif v in ["INTEGER", "INT64"]:
                config["col_int"].append(k)
            elif v in ["NUMERIC", "DECIMAL"]:
                config["col_decimal"].append(k)
            elif v in ["BOOLEAN", "BOOL"]:
                config["col_bool"].append(k)
            elif v in ["FLOAT64", "FLOAT"]:
                config["col_float"].append(k)
            elif v in ["TIME"]:
                config["col_time"].append(k)
            else:
                raise NotImplementedError(
                    f"the value [{v}] is not implemented yet"
                )
        return config

    def convert_time(self, val):
        if pd.isna(val):
            return None
        else:
            return val

    def convert_dtype(self, df: pd.DataFrame, dtype_config):
        col_str = dtype_config.get("col_str")
        col_ts = dtype_config.get("col_ts")
        col_dt = dtype_config.get("col_dt")
        col_int = dtype_config.get("col_int")
        col_decimal = dtype_config.get("col_decimal")
        col_bool = dtype_config.get("col_bool")
        col_float = dtype_config.get("col_float")
        col_time = dtype_config.get("col_time")
        if col_str:
            for c in col_str:
                print(f"converting {c}")
                df[c] = df[c].astype(str)
        if col_ts:
            for c in col_ts:
                print(f"converting {c}")
                df[c] = pd.to_datetime(df[c], errors="coerce")
        if col_dt:
            for c in col_dt:
                print(f"converting {c}")
                df[c] = pd.to_datetime(df[c], errors="coerce").dt.date
        if col_int:
            for c in col_int:
                print(f"converting {c}")
                df[c] = df[c].astype("float")
                df[c] = df[c].astype("Int64")
        if col_decimal:
            for c in col_decimal:
                print(f"converting {c}")
                df[c] = df[c].astype(str).map(decimal.Decimal)
        if col_time:
            for c in col_time:
                print(f"converting {c}")
                df[c] = df[c].apply(self.convert_time)
        if col_bool:
            df = self.convert_boolean_cols(df, col_bool)
        if col_float:
            df = self.convert_float_cols(df, col_float)
        df.replace({"nan": np.nan, "NaN": np.nan}, inplace=True)
        return df

    def convert_boolean_cols(self, df, cols):
        for c in cols:
            try:
                df[c] = df[c].astype(int)
            except Exception as e:
                pass
            df[c] = df[c].astype("bool")
        return df

    def convert_float_cols(self, df, cols):
        for c in cols:
            try:
                df[c] = df[c].astype(float)
            except Exception as e:
                pass
        return df

    def read_data_from_s3(self, s3_filepath):
        _temp_file_path = f"./{uuid.uuid4().hex}.tempfile"
        self.s3.download_file(s3_filepath, _temp_file_path)
        if s3_filepath.endswith(".csv"):
            df = pd.read_csv(_temp_file_path, dtype=str)
        elif s3_filepath.endswith(".xlsx"):
            df = pd.read_excel(_temp_file_path, dtype=str, engine="openpyxl")
        else:
            raise NotImplementedError(
                f"the input file is not supported yet: {s3_filepath}"
            )
        os.remove(_temp_file_path)
        print(f"data size {df.shape}")
        return df

    def run_sql(self, sql):
        query_job = self.bqclient.query(sql)
        results = query_job.result()
        return results

    def clear_table(self, dataset_name, table_id):
        """remove all records from the table, the target table must exists to run this

        Args:
            dataset_name (str): schema_name/dataset_id
            table_id (str): table_name/table_id
        """
        full_qualified_id = self.__get_full_qualified_table_name(
            dataset_name, table_id
        )
        sql = f"TRUNCATE TABLE {full_qualified_id}"
        self.run_sql(sql)
