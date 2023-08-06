from __future__ import annotations
from typing import List
import pandas as pd # type: ignore

FREETRADE_URL = "https://raw.githubusercontent.com/MihaiBlebea/yahoo_fin_api/master/universe/freetrade.csv"
SP_500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
FTSE_100_URL = "https://en.wikipedia.org/wiki/FTSE_100_Index"

class Universe:

	@staticmethod
	def get_freetrade_universe()-> List[str] | None:
		res = pd.read_csv(FREETRADE_URL, index_col=0)
		if "Symbol" not in res:
			return None

		return [r for r in res["Symbol"]]

	@staticmethod
	def get_sp_500_universe()-> List[str]:
		res = pd.read_html(SP_500_URL)

		return [r for r in res[0]["Symbol"]]

	@staticmethod
	def get_ftse_100_universe()-> List[str]:
		res = pd.read_html(FTSE_100_URL)

		return [r for r in res[3]["EPIC"]]
