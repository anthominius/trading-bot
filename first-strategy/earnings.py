from openbb_terminal.sdk import openbb
import pandas as pd
import logging

logger = logging.getLogger(__name__)


symbols = openbb.etf.holdings('DIA')
dia_symbols = list(symbols.index.drop(['N/A']))
dia_valuation = openbb.stocks.ca.screener(similar=dia_symbols, data_type='valuation') 
