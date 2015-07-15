# pair_product.py
A Q&D Sentinel-1 tool for finding pair products.
Python 2.7 with no dependencies.
***
##usage:
    pair_products.py --username=<user> --password=<pass> --datahub=<datahub> --query=<query>

### example
    pair_products.py --username=xxx --password=xxx --datahub="https://scihub.esa.int/dhus" --query="Rome"
    pair_products.py --username=xxx --password=xxx --datahub "https://scihub.esa.int/dhus" --query "( footprint:\"Intersects(POLYGON((12.431942889421666 41.935618527033114,12.541806170671668 41.93715088765262,12.546612689226354 41.83644770945867,12.431942889421666 41.83644770945867,12.431942889421666 41.935618527033114)))\")"