from __future__ import annotations
from typing import List
from yahoo_fin_api.client import Client
from yahoo_fin_api.models.cashflow import CashFlows
from yahoo_fin_api.models.income_statement import IncomeStatements
from yahoo_fin_api.models.balance_sheet import BalanceSheets
from yahoo_fin_api.models.financial_data import FinancialData
from yahoo_fin_api.models.key_statistics import KeyStatistics
from yahoo_fin_api.models.summary_detail import SummaryDetail
from yahoo_fin_api.models.quote  import Quote
from yahoo_fin_api.models.ticker import Ticker


class YahooFinApi:

	def __init__(self, client: Client) -> None:
		self.client = client

	def get_balance_sheets(self, symbols: list[str])-> List[BalanceSheets] | List:
		res = self.client.get_symbols(symbols)

		return [
			BalanceSheets.from_dict(r) for r in res
		]

	def get_cashflow_statements(self, symbols: list[str])-> List[CashFlows] | List:
		res = self.client.get_symbols(symbols)

		return [
			CashFlows.from_dict(r) for r in res
		]

	def get_income_statements(self, symbols: List[str])-> List[IncomeStatements] | List:
		res = self.client.get_symbols(symbols)

		return [
			IncomeStatements.from_dict(r) for r in res
		]

	def get_financial_data(self, symbols: List[str])-> List[FinancialData] | List:
		res = self.client.get_symbols(symbols)

		return [
			FinancialData.from_dict(r) for r in res 
		]

	def get_summary_detail(self, symbols: List[str])-> List[SummaryDetail] | List:
		res = self.client.get_symbols(symbols)

		return [
			SummaryDetail.from_dict(r) for r in res
		]

	def get_key_statistics(self, symbols: List[str])-> List[KeyStatistics] | List:
		res = self.client.get_symbols(symbols)

		return [
			KeyStatistics.from_dict(r) for r in res
		]

	def get_all(self, symbols: List[str])-> List[Ticker] | List:
		res = self.client.get_symbols(symbols)

		return [
			Ticker.from_dict(r) for r in res
		]

	def get_quote(self, symbol: str, range: str, interval: str)-> List[Quote] | List:
		res = self.client.get_quote(symbol, range, interval)

		quotes = []
		for i, t in enumerate(res["timestamp"]):
			quotes.append(Quote(
				t,
				res["indicators"]["quote"][0]["open"][i],
				res["indicators"]["quote"][0]["close"][i],
				res["indicators"]["quote"][0]["high"][i],
				res["indicators"]["quote"][0]["low"][i],
				res["indicators"]["quote"][0]["volume"][i]
			))

		return quotes