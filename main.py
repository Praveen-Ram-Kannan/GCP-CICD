from google.cloud import bigquery

bq_client = bigquery.Client()

def ingest_from_github(data, context):
  print('Start!!!!')
  
  bucket_name = data['bucket']
  file_name = data['name']
  table = "dataanalysis-330007.EmployeeDetails.Employee"

  job_config = bigquery.LoadJobConfig(
      schema=[
          bigquery.SchemaField("ID", "INTEGER"),
          bigquery.SchemaField("Prefix", "STRING"),
          bigquery.SchemaField("FirstName", "STRING"),
          bigquery.SchemaField("MiddleName", "STRING"),
          bigquery.SchemaField("LastName", "STRING"),
          bigquery.SchemaField("Gender", "STRING"),
          bigquery.SchemaField("EMail", "STRING"),
      ],
      skip_leading_rows=1,
      source_format=bigquery.SourceFormat.CSV,
  )
  uri = f"gs://{bucket_name}/{file_name}"

  load_job = bq_client.load_table_from_uri(
      uri, table, job_config=job_config
  )

  load_job.result()  # Waits for the job to complete.

  destination_table = bq_client.get_table(table)  # Make an API request.
  print("Loaded {} rows.".format(destination_table.num_rows))
