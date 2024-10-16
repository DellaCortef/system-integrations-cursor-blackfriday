import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

# Load environment variables
load_dotenv()


def sample_run_report(property_id="YOUR-GA4-PROPERTY-ID"):
    """Runs a simple report on a Google Analytics 4 property."""
    # TODO(developer): Uncomment this variable and replace with your
    #  Google Analytics 4 property ID before running the sample.
    # property_id = "YOUR-GA4-PROPERTY-ID"

    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()

    property_id = os.getenv("GA_PROPERTY_ID")
    start_date = os.getenv("GA_START_DATE")

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="date"),
            Dimension(name="city"),
            Dimension(name="country"),
            Dimension(name="deviceCategory"),
            Dimension(name="sessionSource"),
            Dimension(name="sessionMedium"),
        ],
        metrics=[
            Metric(name="totalUsers"),
            Metric(name="newUsers"),
            Metric(name="activeUsers"),
            Metric(name="sessions"),
            Metric(name="engagedSessions"),
            Metric(name="averageSessionDuration"),
            Metric(name="screenPageViews"),
            Metric(name="conversions"),
            Metric(name="totalRevenue"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date="today")],
    )
    response = client.run_report(request)

   # Create lists to store data
    data = []
    header = [dim.name for dim in request.dimensions] + [metric.name for metric in request.metrics]

    # Fill in the data list
    for row in response.rows:
        row_data = [dim_value.value for dim_value in row.dimension_values] + [metric_value.value for metric_value in row.metric_values]
        data.append(row_data)

    # Create a DataFrame with the data
    df = pd.DataFrame(data, columns=header)

    # Configuring the connection to the PostgreSQL database
    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url)

    # Save the DataFrame to the 'google_analytics_data' table in the database
    df.to_sql(name='google_analytics_data', con=engine, if_exists='replace', index=False)

    print("Dados do Google Analytics salvos no banco de dados PostgreSQL.")

if __name__ == "__main__":
    sample_run_report()