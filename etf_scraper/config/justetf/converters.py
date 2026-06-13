"""
Label conversion mapping for JustETF.

Maps raw HTML labels extracted from the website
to standardized internal field names used by the scraper.

This layer ensures decoupling between website structure
and internal data schema.
"""

from types import MappingProxyType

header_converter = MappingProxyType({
    "PEA eligible" : "PEA eligible"
})

overview_converter = MappingProxyType({
    "Currency"     : "Currency",
    "Price"        : "Price",
    "Date of Price": "Date of Price",
})

basics_converter = MappingProxyType({
    "Index"              : "Index",
    "Investment focus"   : "Investment focus",
    "Fund size"          : "Fund size",
    "Total expense ratio": "TER",
    "Replication"        : "Replication",
    "Distribution policy": "Dividends",
    "Fund Provider"      : "Fund Provider",
})

performance_converter = MappingProxyType({
    "YTD"      : "Perf Current Year",
    "1 month"  : "Perf 1 month",
    "3 months" : "Perf 3 months",
    "6 months" : "Perf 6 months",
    "1 year"   : "Perf 1 year",
    "3 years"  : "Perf 3 years",
    "5 years"  : "Perf 5 years",
})

risk_converter = MappingProxyType({
    "Volatility 1 year" : "Vol 1 year",
    "Volatility 3 years": "Vol 3 years",
    "Volatility 5 years": "Vol 5 years",
})

stock_exchange_converter = MappingProxyType({
    "Stock exchange": "Stock exchange",
})