import numpy as np
import pandas as pd

from bizintel.utils_logger import get_logger

logger = get_logger(__name__)


def clean_sales():
    logger.info("Loading sales_data.csv...")
    df = pd.read_csv("data/raw/sales_data.csv")

    logger.debug(df.head())

    # Replace "?" with NaN
    logger.info("Replacing '?' with NaN...")
    df = df.replace("?", np.nan)

    # Convert numeric columns
    numeric_cols = ["SaleAmount", "QuantitySold", "CampaignID"]
    for col in numeric_cols:
        logger.info(f"Converting column {col} to numeric...")
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fill missing CampaignID
    logger.info("Filling missing CampaignID with 0...")
    df["CampaignID"] = df["CampaignID"].fillna(0)

    # Fill missing SaleAmount
    logger.info("Filling missing SaleAmount with median...")
    df["SaleAmount"] = df["SaleAmount"].fillna(df["SaleAmount"].median())

    # Drop missing PaymentMethod
    logger.info("Dropping rows missing PaymentMethod...")
    df = df.dropna(subset=["PaymentMethod"])

    # Fix PaymentMethod
    logger.info("Standardizing PaymentMethod values...")
    df["PaymentMethod"] = df["PaymentMethod"].str.strip()
    df["PaymentMethod"] = df["PaymentMethod"].replace({"Credit": "CreditCard"})

    # Remove duplicates
    logger.info("Removing duplicate rows...")
    df = df.drop_duplicates()

    # Convert SaleDate
    logger.info("Converting SaleDate to datetime...")
    df["SaleDate"] = pd.to_datetime(df["SaleDate"], errors="coerce")

    # Outlier handling
    logger.info("Filtering SaleAmount outliers...")
    q1 = df["SaleAmount"].quantile(0.25)
    q3 = df["SaleAmount"].quantile(0.75)
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    df = df[df["SaleAmount"] <= upper]

    # Save cleaned file
    logger.info("Saving cleaned sales data...")
    df.to_csv("data/clean/clean_sales.csv", index=False)

    logger.info("Sales cleaning complete.")
    return df


if __name__ == "__main__":
    clean_sales()
