import pandas as pd
from app.core.parser import XLSXParser

parser = XLSXParser()

file_path = "data/input/자동화.xls"

df = parser.read_xlsx(file_path=file_path)