"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : dataset_registry.py
Package     : src.etl
Purpose     : Dataset Registry
Author      : ERIP
Version     : 3.0.0

Description
-----------
Central registry that defines every dataset supported by ERIP.

Each dataset specifies:

    • Source type
    • Extractor
    • Transformer
    • Validator
    • Loader

This allows new datasets to be added without modifying the ETL engine.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from pathlib import Path

from src.etl.extract.base_extractor import BaseExtractor
from src.etl.transform.base_transformer import BaseTransformer

from src.etl.validate.customer_validator import CustomerValidator
from src.etl.load.base_loader import BaseLoader

from src.etl.context import ETLContext
from src.etl.pipeline import ETLPipeline

from src.etl.extract.csv_extractor import CSVExtractor
from src.etl.transform.customer_transformer import CustomerTransformer
from src.etl.validate.base_validator import BaseValidator
from src.etl.load.load_customer import CustomerLoader

from src.etl.transform.sales_order_transformer import (
    SalesOrderTransformer,
)
from src.etl.validate.orders_validator import (
    OrdersValidator,
)
from src.etl.load.load_orders import (
    OrdersLoader,
)

from src.etl.transform.product_transformer import (
    ProductTransformer,
)
from src.etl.validate.product_validator import (
    ProductValidator,
)
from src.etl.load.load_product import (
    ProductLoader,
)

from src.etl.transform.seller_transformer import (
    SellerTransformer,
)
from src.etl.validate.seller_validator import (
    SellerValidator,
)
from src.etl.load.load_seller import (
    SellerLoader,
)

from src.etl.transform.order_items_transformer import (
    OrderItemsTransformer,
)
from src.etl.validate.order_items_validator import (
    OrderItemsValidator,
)
from src.etl.load.load_order_items import (
    OrderItemsLoader,
)

from src.etl.transform.payment_transformer import (
    PaymentTransformer,
)
from src.etl.validate.payment_validator import (
    PaymentValidator,
)
from src.etl.load.load_order_payments import (
    OrderPaymentsLoader,
)

from src.etl.transform.review_transformer import (
    ReviewTransformer,
)
from src.etl.validate.review_validator import (
    ReviewValidator,
)
from src.etl.load.load_order_reviews import (
    OrderReviewsLoader,
)

from src.etl.transform.geolocation_transformer import (
    GeolocationTransformer,
)
from src.etl.validate.geolocation_validator import (
    GeolocationValidator,
)
from src.etl.load.load_geolocation import (
    GeolocationLoader,
)

# =============================================================================
# Dataset Definition
# =============================================================================

@dataclass(slots=True)
class DatasetDefinition:
    """
    Enterprise dataset definition.
    """

    name: str

    source_name: str

    source_type: str

    source_path: Path

    target_schema: str

    target_table: str

    extractor: Type[BaseExtractor]

    transformer: Type[BaseTransformer]

    validator: Type[BaseValidator]

    loader: Type[BaseLoader]

    def build_pipeline(self) -> ETLPipeline:
        """
        Build an executable ETL pipeline for this dataset.
        """

        context = ETLContext(

            pipeline_name=f"{self.name} Pipeline",

            source_name=self.source_name,

            source_type=self.source_type,

            source_path=self.source_path,

            target_schema=self.target_schema,

            target_table=self.target_table,

        )

        return ETLPipeline(
            name=self.name,
            context=context,
            extractor=self.extractor(context),
            transformer=self.transformer(context),
            validator=self.validator(context),
            loader=self.loader(context),
        )


# =============================================================================
# Dataset Registry
# =============================================================================

class DatasetRegistry:
    """
    Enterprise Dataset Registry.
    """

    _datasets: dict[str, DatasetDefinition] = {}

    # ---------------------------------------------------------------------

    @classmethod
    def register(
        cls,
        dataset: DatasetDefinition,
    ) -> None:

        cls._datasets[

            dataset.name.lower()

        ] = dataset

    # ---------------------------------------------------------------------

    @classmethod
    def get(
        cls,
        dataset_name: str,
    ) -> DatasetDefinition:

        dataset_name = dataset_name.lower()

        if dataset_name not in cls._datasets:

            raise KeyError(

                f"Dataset '{dataset_name}' is not registered."

            )

        return cls._datasets[dataset_name]

    # ---------------------------------------------------------------------

    @classmethod
    def exists(
        cls,
        dataset_name: str,
    ) -> bool:

        return (

            dataset_name.lower()

            in cls._datasets

        )

    # ---------------------------------------------------------------------

    @classmethod
    def registered_datasets(
        cls,
    ) -> list[str]:
        """
        Return registered datasets in registration order.

        Python dictionaries preserve insertion order, so the
        execution order is defined explicitly by register_all().
        """

        return list(

            cls._datasets.keys()

        )
    #----------------------------------------------------------------------

    @classmethod
    def build_pipeline(
        cls,
        dataset_name: str,
    ) -> ETLPipeline:
        """
        Build an executable pipeline for a registered dataset.
        """

        dataset = cls.get(dataset_name)

        return dataset.build_pipeline()

    #-------------------------------------------------------------------------
    @classmethod
    def register_customer(cls) -> None:
        """
        Register the Customer dataset.
        """

        cls.register(

            DatasetDefinition(

                name="customer",

                source_name="Olist Customers",

                source_type="CSV",

                source_path=Path(
                    "data/raw/olist_customers_dataset.csv"
                ),

                target_schema="staging",

                target_table="customer",

                extractor=CSVExtractor,

                transformer=CustomerTransformer,

                validator=CustomerValidator,

                loader=CustomerLoader,

            )

        )

    #-----------------------------------------------------------------------

    @classmethod
    def register_orders(cls) -> None:
        """
        Register the Orders dataset.
        """

        cls.register(

            DatasetDefinition(

                name="orders",

                source_name="Olist Orders",

                source_type="CSV",

                source_path=Path(
                    "data/raw/olist_orders_dataset.csv"
                ),

                target_schema="staging",

                target_table="orders",

                extractor=CSVExtractor,

                transformer=SalesOrderTransformer,

                validator=OrdersValidator,

                loader=OrdersLoader,

            )

        )

    #----------------------------------------------------------------------

    @classmethod
    def register_product(cls) -> None:
        """
        Register the Product dataset.
        """

        cls.register(

            DatasetDefinition(

                name="product",

                source_name="Olist Products",

                source_type="CSV",

                source_path=Path(
                    "data/raw/olist_products_dataset.csv"
                ),

                    target_schema="staging",

                target_table="product",

                extractor=CSVExtractor,

                transformer=ProductTransformer,

                validator=ProductValidator,

                loader=ProductLoader,

            )

        )
    #--------------------------------------------------------------------

    @classmethod
    def register_seller(cls) -> None:
        """
        Register the Seller dataset.
        """

        cls.register(

            DatasetDefinition(

                name="seller",

                source_name="Olist Sellers",

                source_type="CSV",

                source_path=Path(
                    "data/raw/olist_sellers_dataset.csv"
                ),

                target_schema="staging",

                target_table="seller",

                extractor=CSVExtractor,

                transformer=SellerTransformer,

                validator=SellerValidator,

                loader=SellerLoader,

            )

        )

#-----------------------------------------------------------------------

    @classmethod
    def register_order_payments(cls) -> None:
        """
        Register the Order Payments dataset.
        """

        cls.register(

            DatasetDefinition(

                name="order_payments",

                source_name="Olist Order Payments",

                source_type="CSV",

                source_path=Path(
                    "data/raw/olist_order_payments_dataset.csv"
                ),

                target_schema="staging",

                target_table="order_payments",

                extractor=CSVExtractor,

                transformer=PaymentTransformer,

                validator=PaymentValidator,

                loader=OrderPaymentsLoader,

            )

        )

    #--------------------------------------------------------------------
    @classmethod
    def register_order_items(cls) -> None:
        """
        Register the Order Items dataset.
        """

        cls.register(

            DatasetDefinition(

                name="order_items",

                source_name="Olist Order Items",

                source_type="CSV",

                source_path=Path(
                    "data/raw/olist_order_items_dataset.csv"
                ),

                target_schema="staging",

                target_table="order_items",

                extractor=CSVExtractor,

                transformer=OrderItemsTransformer,

                validator=OrderItemsValidator,

                loader=OrderItemsLoader,

            )

        )

    #---------------------------------------------------------------------

    @classmethod
    def register_order_reviews(cls) -> None:
        """
        Register the Order Reviews dataset.
        """

        cls.register(

            DatasetDefinition(

                name="order_reviews",

                source_name="Olist Order Reviews",

                source_type="CSV",

                source_path=Path(
                    "data/raw/olist_order_reviews_dataset.csv"
                ),

                target_schema="staging",

                target_table="order_reviews",

                extractor=CSVExtractor,

                transformer=ReviewTransformer,

                validator=ReviewValidator,

                loader=OrderReviewsLoader,

            )

        )

    #--------------------------------------------------------------------

    @classmethod
    def register_geolocation(cls) -> None:
        """
        Register the Geolocation dataset.
        """

        cls.register(

            DatasetDefinition(

                name="geolocation",

                source_name="Olist Geolocation",

                source_type="CSV",

                source_path=Path(
                    "data/raw/olist_geolocation_dataset.csv"
                ),

                target_schema="staging",

                target_table="geolocation",

                extractor=CSVExtractor,

                transformer=GeolocationTransformer,

                validator=GeolocationValidator,

                loader=GeolocationLoader,

            )

        )

    #---------------------------------------------------------------------
    @classmethod
    def register_all(cls) -> None:
        """
        Register all supported datasets.
        """

        cls.clear()

        cls.register_customer()

        cls.register_orders()

        cls.register_product()

        cls.register_seller()

        cls.register_order_items()

        cls.register_order_payments()

        cls.register_order_reviews()

        cls.register_geolocation()

    # ---------------------------------------------------------------------

    @classmethod
    def clear(
        cls,
    ) -> None:

        cls._datasets.clear()