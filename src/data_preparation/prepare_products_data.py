import pandas as pd

from bizintel.utils_logger import get_logger

logger = get_logger(__name__)


def clean_products():
    logger.info("Loading products_data.csv...")
    df = pd.read_csv("data/raw/products_data.csv")

    logger.debug(df.head())

    # Convert numeric columns
    logger.info("Converting UnitPrice and WeightPounds to numeric...")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["WeightPounds"] = pd.to_numeric(df["WeightPounds"], errors="coerce")

    # Standardize Category & Supplier
    logger.info("Standardizing Category and Supplier...")
    df["Category"] = df["Category"].str.strip().str.title()
    df["Supplier"] = df["Supplier"].str.strip().str.title()

    # Save cleaned file
    logger.info("Saving cleaned products data...")
    df.to_csv("data/clean/clean_products.csv", index=False)

    logger.info("Product cleaning complete.")
    return df


if __name__ == "__main__":
    clean_products()
