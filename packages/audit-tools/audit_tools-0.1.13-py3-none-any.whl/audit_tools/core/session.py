import sys
from typing import Optional

import pandas as pd
from rich.table import Table

from audit_tools.core.errors import SessionException
from audit_tools.core.utils import get_logger, import_file, export_file
from audit_tools.core.utils.converters import dataframe_to_rich_table

columns_main = ["Counted", "Variance"]


class Session:
    def __init__(self, file_path: Optional[str] = None):
        self.variance_counter = 0
        self.missed_counter = 0
        self.logger = get_logger()

        self.logger.info("Session initialized")

        # Creates a DataFrame based on the Product model
        self.logger.info("Creating DataFrame")

        self.products = pd.DataFrame(columns=columns_main)
        self.products["Counted"] = 0
        self.products["Variance"] = 0

        if file_path:
            try:
                products, self.file_type = import_file(file_path)
                self.products = pd.concat([products, self.products])
                self.products["Counted"] = 0
                self.products["Variance"] = 0
            except SessionException as e:
                self.logger.exception(e)
                sys.exit(1)
        else:
            self.file_type = "csv"

        self.logger.info("Creating alternative data structures")

        if not self.products.empty:
            self.variance_items = self.products[0:0].copy()
            self.missed_items = self.products[0:0].copy()

    def import_data(self, file_path: str):
        self.logger.info(f"Importing data from: {file_path}")

        if self.products.empty:
            try:
                products, self.file_type = import_file(file_path)
                self.products = pd.concat([products, self.products])

                self.products["Counted"] = 0
                self.products["Variance"] = 0

                self.variance_items = self.products[0:0].copy()
                self.missed_items = self.products[0:0].copy()

            except SessionException as e:
                self.logger.exception(e)
        else:
            raise SessionException("Session already has data")

    # Update a products count via user input
    def count_product(self, sku: str, count: int = 0):

        if self.get_product(sku):

            # Grab the product pertaining to the SKU
            try:
                prod = self.products.index[self.products.select_dtypes(object).eq(sku).any(1)]
            except pd.errors.InvalidIndexError as e:
                self.logger.error(f"Product: {sku} not found")
                self.logger.error(e)
                return False

            self.logger.info(f"Setting product count: {sku} to {count}")

            # Set the products count to the updated count
            self.products.loc[prod, "Counted"] = count

            return True
        else:
            self.logger.error(f"Product: {sku} not found")
            raise SessionException(f"Product: {sku} not found")

    def increase_product(self, sku: str, count: int = 0):

        if self.get_product(sku):

            # Grab the product pertaining to the SKU
            try:
                prod = self.products.index[self.products.select_dtypes(object).eq(sku).any(1)]
            except pd.errors.InvalidIndexError as e:
                self.logger.error(f"Product: {sku} not found")
                self.logger.error(e)
                return False

            counted = self.products["Counted"].iloc[prod[0]]

            self.logger.info(f"Increasing product count: {sku} by {count}")

            # Set the products count to the updated count
            self.products.loc[prod, "Counted"] = count + counted

            return True

    # Update the products count via receipt input
    def reduce_product(self, sku: str, count: int = 0):

        if self.get_product(sku):

            # Grabs the product pertaining to the SKU
            try:
                prod = self.products.index[self.products.select_dtypes(object).eq(sku).any(1)]
            except pd.errors.InvalidIndexError as e:
                self.logger.error(f"Product: {sku} not found")
                self.logger.exception(e)
                return

            counted = self.products["Counted"].iloc[prod[0]]

            self.logger.info(f"Reducing product count: {sku} by {count}")

            # Sets the products count to the updated count
            self.products.loc[prod, "Counted"] = counted - count

            return True

    def get_product(self, sku: str):
        self.logger.info(f"Getting product: {sku}")

        prod = self.products[self.products['SKU'] == sku]

        if prod.empty:
            self.logger.error(f"Product: {sku} not found")
            return None

        return prod.all

    def get_table_data(self, table_data: pd.DataFrame = None) -> Optional[Table or str]:
        """
        Returns a Table object with the products in the session and their counts, if no DataFrame is given it will use
        the products DataFrame from the session.

        """
        self.logger.info("Getting table data")
        if table_data is None:
            table_data = self.products

        if table_data.empty:
            self.logger.error("No products found in session")
            return "No products found in session"

        table = Table(show_header=True, header_style="bold magenta")
        table = dataframe_to_rich_table(table_data, table)

        return table

    def parse_session_data(self):
        for index, row in self.products.iterrows():
            variance = row["Counted"] - row["In Stock"]
            self.products.loc[index, "Variance"] = variance
            self.products.loc[index, "Notes"] = f"Variance caught by A.T."
            if variance > 0 or variance < 0:
                self.variance_counter += 1
                self.variance_items = pd.concat([
                    self.variance_items,
                    self.products[self.products['SKU'] == row["SKU"]]
                ],
                    ignore_index=True,
                    verify_integrity=True
                )

            if row["Counted"] == 0:
                self.missed_counter += 1
                self.missed_items = pd.concat([
                    self.missed_items,
                    self.products[self.products['SKU'] == row["SKU"]]
                ],
                    ignore_index=True,
                    verify_integrity=True
                )

    def shutdown(self, file_folder: Optional[str] = None):
        """
        Shuts down the session and saves the data to a file

        :param file_folder: When provided the file will be saved to the given folder
        """

        if self.variance_counter >= 1:
            print(f"{self.variance_counter} products have a variance!")
            self.logger.warning(f"{self.variance_counter} products have a variance!")
            print(f"\n{self.variance_items}")

        try:
            file_name = export_file(
                self.file_type, file_folder,
                self.variance_items.copy() if self.variance_counter >= 1 else self.products.copy()
            )
            print(f"Exported to: {file_name}")

        except SessionException as e:
            self.logger.exception(e)
