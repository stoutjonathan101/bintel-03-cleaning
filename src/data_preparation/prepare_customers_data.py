import pandas as pd

from bizintel.utils_logger import get_logger

logger = get_logger(__name__)


def clean_customers():
    logger.info("Loading customers_data.csv...")
    df = pd.read_csv("data/raw/customers_data.csv")

    logger.debug(df.head())

    # Remove duplicate CustomerID
    logger.info("Removing duplicate CustomerID entries...")
    df = df.drop_duplicates(subset="CustomerID")

    # Standardize Region
    logger.info("Standardizing Region values...")
    df["Region"] = (
        df["Region"].str.strip().str.lower().str.replace("-", " ").str.title()
    )

    # Standardize GoldMember
    logger.info("Standardizing GoldMember values...")
    df["GoldMember"] = df["GoldMember"].str.upper().str.strip()

    # Convert JoinDate
    logger.info("Converting JoinDate to datetime...")
    df["JoinDate"] = pd.to_datetime(df["JoinDate"], errors="coerce")

    # Save cleaned file
    logger.info("Saving cleaned customers data...")
    df.to_csv("data/clean/clean_customers.csv", index=False)

    logger.info("Customer cleaning complete.")
    return df


if __name__ == "__main__":
    clean_customers()
