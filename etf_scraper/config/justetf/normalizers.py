"""
Data normalization functions for scraped ETF values.

This module standardizes raw string values into clean formats:
- numeric conversion
- percentage normalization
- text cleanup
- date formatting
"""

def normalize_price( value: str ) -> float:
    return float( value.replace( ",", "" ) )

def normalize_percentage( value: str ) -> float:
    value = value.split( "%" )[ 0 ].replace( ",", "" )
    try:
        return float( value ) / 100
    except ValueError:
        return None

def normalize_fund_size( value: str ) -> str:
    currency, size, unit = value.split()
    return f"{currency} {size.replace( ',', '' )} {unit.upper()}"

def normalize_replication( value: str ) -> str:
    return value.split( "(" )[ 0 ]

def normalize_date_of_price( value: str ) -> str:
    return value.split()[ 0 ]

def normalize_investment_focus( value: str ) -> str:
    areas = [ v.strip() for v in value.split( "," ) ]
    return "\n".join( areas )