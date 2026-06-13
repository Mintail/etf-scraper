# ETF Scraper

A highly configurable and extensible ETF scraping framework built around **JustETF**.

It extracts structured ETF data from ISIN-based pages using a declarative configuration system centered around **DOMPath-based navigation**.

The project is designed with two complementary perspectives:

- **User-friendly mode**: configure `user_config.py` and run a single script.
- **Developer mode**: config-driven architecture where adding a new website only requires defining a configuration.

---

## Key Features

- ISIN-based ETF scraping (JustETF supported).
- Fully declarative DOM-based extraction system (DOMPath core).
- Highly modular multi-site architecture via `SiteConfig`.
- CSV / Excel structured export.

---

## Core Concepts

### 1. User-friendly execution layer

The simplest way to use this project:

- Edit `user_config.py`.
- Define input/output files`.
- Run `run_scraper.py`.

No knowledge of scraping internals is required.

The system handles:
- browser automation,
- page loading,
- extraction,
- formatting,
- export.

---

### 2. Modular architecture

The system is fully driven by configuration.

The core abstraction is `SiteConfig`, which defines how a website is scraped.

To add a new website, you only define a configuration — no engine changes are required.

---

### 3. DOMPath

**DOMPath is the core engine of the scraper.**

It provides a fluent interface to navigate HTML trees (find elements, traverse DOM structure, validate nodes).

Everything in the extraction pipeline is built on top of DOMPath.

---

## Usage

### Quick start

1. Edit `user_config.py`
2. Provide input file in txt/csv/excel (ISIN list)
3. Run:

```bash
python run_scraper.py
```

### Examples

A set of examples is already available in the `examples` folder.
The default settings in `user_config.py` are configured to run the `input_txt` example using the Safari web browser.
Those are the available test scripts:
- `input_txt.txt`,
- `input_csv.csv`,


---

## Input formats

Supported formats:

### TXT
- ISIN list (one ISIN per row).
- Or column list (one column per row) + blank line + ISIN list (one ISIN per row).

### CSV / XLSX
- First column must contain ISINs.
- Optional additional columns supported in the first row.

---

## Output

The output is a structured table.

Each row corresponds to an ISIN and contains financial metrics such as Index, Region, Asset Type, Fund size, TER, Price, Performance (1m, 1y, 5y...), and risk metrics.

The output is formatted as either CSV or XLSX and can preserve formatting from the XLSX input if demanded.

---

## Supported Website

Currently supported:

- www.justetf.com

---

## How to add a new website

To extend the scraper to a new site, create a new configuration:

1. Create a site folder in `config/<site_name>/`

2. Create a `SiteConfig` with:
    - base website,
    - columns to output,
    - sections (DOMPath, extractors, converters),
    - optional normalizers,
    - optional special processing of columns,
    - a checker that verifies the page corresponds to the ISIN,
    - and a checker that verifies that the page is loaded.

3. Add the new `SiteConfig` in `_CONFIGS` inside `config/__init__.py`

---

## Engine overview

Pipeline flow:

```
Input file
→ FileReader
→ WebDriverSoupFactory (Selenium)
→ BeautifulSoup
→ DOMPath
→ Extractors
→ Converters
→ Normalizers
→ Special Adds
→ DataFrame
→ FileWriter
```

---

## Limitations

### 1. DOM sensitivity

The scraper is tightly coupled to the JustETF HTML structure.

Any change in the website DOM may require updates in `config/justetf/paths.py`, as extraction logic depends directly on DOM navigation rules.

---

### 2. Sequential execution (no parallelism)

The scraper processes ISINs sequentially rather than in parallel.

This is an intentional design choice due to JustETF’s tendency to become unstable or temporarily block requests under high load.

As a result, scraping performance is constrained by enforced delays and retry logic. For example, processing ~200 entries can take approximately 30–40 minutes depending on network conditions and retry frequency.

---

### 3. Single-site support

The system currently supports only one active website configuration (JustETF).

Although the architecture is designed to be extensible via `SiteConfig`, multi-site execution is not yet implemented at runtime level.

---

### 4. No data analysis layer

This project is a **pure scraping engine**.

It extracts and structures financial data but does not perform any financial analysis, or interpretation of metrics.

---

## Requirements

- selenium
- beautifulsoup4
- pandas
- openpyxl

---

## Design philosophy

This project is built around three principles:

1. **User simplicity**: run a single script.
2. **Config-driven architecture**: no hardcoded scraping logic.
3. **DOMPath-centric extraction**: all data flows through structured DOM navigation.

