"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Package:
    Validation

Purpose:
    Enterprise Validation Framework

Description:
    The Validation Framework provides a unified interface for validating
    the Enterprise Revenue Intelligence Platform (ERIP).

Public API
----------
Validators
    • DatabaseValidator
    • SchemaValidator
    • MetadataValidator
    • ReferenceDataValidator
    • StagingValidator
    • ConstraintValidator
    • IndexValidator
    • WarehouseValidator

Framework
    • ValidationRunner
    • ValidationResult
    • ValidationSummary

Author:
    Abodunrin Oketade

Platform:
    Enterprise Revenue Intelligence Platform (ERIP)

Version:
    2.1.0
===============================================================================
"""

from .models import ValidationResult
from .models import ValidationSummary

from .runner import ValidationRunner

from .test_database import DatabaseValidator
from .test_schemas import SchemaValidator
from .test_metadata import MetadataValidator
from .test_reference_data import ReferenceDataValidator
from .test_staging_tables import StagingValidator
from .test_constraints import ConstraintValidator
from .test_indexes import IndexValidator
from .test_warehouse import WarehouseValidator

__all__ = [

    # Framework

    "ValidationRunner",

    "ValidationResult",

    "ValidationSummary",

    # Validators

    "DatabaseValidator",

    "SchemaValidator",

    "MetadataValidator",

    "ReferenceDataValidator",

    "StagingValidator",

    "ConstraintValidator",

    "IndexValidator",

    "WarehouseValidator",

]

__version__ = "2.1.0"