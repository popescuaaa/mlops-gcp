from generator import FakeUserDataGenerator
from config import AppConfig
import pandas as pd
import google.auth
from google.cloud import bigquery
from google.cloud import storage


class App:
    def __init__(self, name: str, config: AppConfig):
        self.name = name
        self.generator = FakeUserDataGenerator()
        self.config = config

        # Retrieve project id from the underlying service account
        if self.config.ENV != "local":
            self.bq_client = bigquery.Client()
            self.storage_client = storage.Client()
            self.credentials, self.project_id = google.auth.default()

    def run(
        self,
    ):
        # Generate a batch of user data samples
        print("Generarting a batch of user data samples")
        num_samples = self.config.SAMPLES
        samples = self.generator.generate_data(num_entries=num_samples)
        samples_df = pd.DataFrame(
            [
                {
                    "user_id": entry.user_id,
                    "name": entry.name,
                    "email": entry.email,
                    "location": entry.location,
                    "purchase_value": entry.purchase_value,
                    "purchase_date": entry.purchase_date,
                }
                for entry in samples
            ]
        )

        # Save data to Docker storage
        samples_df.to_csv("user_samples.csv")
        print(f"Data was generated succesfully: shape {samples_df.shape}")

    def ingest(self):
        # Upload data to gcs
        bucket_name = self.config.BUCKET
        bucket = self.storage_client.bucket(bucket_name=bucket_name)
        destination_blob_name = "users.csv"
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename("./user_samples.csv")

        upload_location = f"gs://{bucket_name}/{destination_blob_name}"

        # Load user data to bq using streaming insert or batch insert
        table_id = f"{self.config.DATASET}.{self.config.TABLE_ID}"

        job_config = bigquery.LoadJobConfig(
            schema=[
                bigquery.SchemaField("user_id", "STRING"),
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("email", "STRING"),
                bigquery.SchemaField("location", "STRING"),
                bigquery.SchemaField("purchase_value", "FLOAT64"),
                bigquery.SchemaField("purchase_date", "TIMESTAMP"),
            ],
            skip_leading_rows=1,
            # The source format defaults to CSV, so the line below is optional.
            source_format=bigquery.SourceFormat.CSV,
        )

        load_job = self.bq_client.load_table_from_uri(
            upload_location, table_id, job_config=job_config
        )  # Make an API request.

        load_job.result()  # Waits for the job to complete.

        destination_table = self.bq_client.get_table(table_id)  # Make an API request.
        print("Loaded {} rows.".format(destination_table.num_rows))


if __name__ == "__main__":
    app_config = AppConfig()
    app = App(name="ingestion_app", config=app_config)

    if app_config.ENV == "local":
        app.run()
    else:
        app.run()
        app.ingest()
