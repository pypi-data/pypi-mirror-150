from __future__ import annotations
from typing import List, Dict, Any, NoReturn
import requests
from pathlib import Path
from threading import Thread
from yahoo_fin_api.cache import BaseCache


modules = [
	"assetProfile",
	"balanceSheetHistory",
	"balanceSheetHistoryQuarterly",
	"calendarEvents",
	"cashflowStatementHistory",
	"cashflowStatementHistoryQuarterly",
	"defaultKeyStatistics",
	"earnings",
	"earningsHistory",
	"earningsTrend",
	"financialData",
	"fundOwnership",
	"incomeStatementHistory",
	"incomeStatementHistoryQuarterly",
	"indexTrend",
	"industryTrend",
	"insiderHolders",
	"insiderTransactions",
	"institutionOwnership",
	"majorDirectHolders",
	"majorHoldersBreakdown",
	"netSharePurchaseActivity",
	"price",
	"quoteType",
	"recommendationTrend",
	"secFilings",
	"sectorTrend",
	"summaryDetail",
	"summaryProfile",
	"symbol",
	"upgradeDowngradeHistory",
	"fundProfile",
	"topHoldings",
	"fundPerformanc"
]

ranges = [
	"1d",
	"5d",
	"1mo",
	"3mo",
	"6mo",
	"1y",
	"2y",
	"5y",
	"10y",
	"ytd",
	"max"
]

intervals = [
	"1m", 
	"2m", 
	"5m", 
	"15m", 
	"30m", 
	"60m", 
	"90m", 
	"1h", 
	"1d", 
	"5d", 
	"1wk", 
	"1mo", 
	"3mo"
]

headers = {"User-agent": "Mozilla/5.0"}

dir = Path(__file__).parent.resolve()

class Client:

	def __init__(self, symbol_cache: BaseCache = None, quote_cache: BaseCache = None)-> None:
		self.symbol_cache = symbol_cache
		self.quote_cache = quote_cache

	def __get_symbol_async(self, symbol: str, result: dict):
		result[symbol] = self.get_symbol(symbol)

	def __is_valid_response(self, body: dict)-> bool:
		keys = ["financialData", "summaryDetail"]
		return len([k for k in keys if k in body]) > 0

	def clear_cache(self, symbol: str)-> bool:
		if self.symbol_cache is not None:
			self.symbol_cache.clear_cache(symbol)
		
		if self.quote_cache is not None:
			self.quote_cache.clear_cache(symbol)

		return True

	def get_symbol(self, symbol: str)-> dict | None:
		if isinstance(symbol, str) is False:
			raise Exception("symbol is not string")

		symbol = symbol.upper()

		if self.symbol_cache is not None and self.symbol_cache.is_cached(symbol):
			return self.symbol_cache.from_cache(symbol)

		url = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules={modules}"
		res = requests.get(
			url.format(symbol=symbol, modules=",".join(modules)), 
			headers=headers,
		)

		if res.status_code != 200:
			return None

		body = res.json()

		if body["quoteSummary"]["error"] is not None:
			return None

		body = body["quoteSummary"]["result"][0]

		if self.__is_valid_response(body) == False:
			return None

		if self.symbol_cache is not None:
			self.symbol_cache.to_cache(symbol, body)

		return body

	def get_symbols(self, symbols: List[str] = None)-> List[dict]:
		if symbols is None:
			return []

		threads = []
		results: Dict[str, dict] = {}
		for i, symbol in enumerate(symbols, start=1):
			print(f"{i}/{len(symbols)} Processing {symbol}")

			threads.append(
				Thread(target=self.__get_symbol_async, args=(symbol, results,)),
			)
			threads[-1].start()

		for t in threads:
			t.join()

		print(f"Completed {len(results)}/{len(symbols)}")
		return [ ticker for ticker in list(results.values()) if ticker is not None ]

	def get_quote(self, symbol: str, range: str, interval: str)-> Dict[Any, Any] | None:
		if range not in ranges:
			return None

		if interval not in intervals:
			return None

		if isinstance(symbol, str) is False:
			raise Exception("symbol is not string")

		symbol = symbol.upper()

		if self.quote_cache is not None and self.quote_cache.is_cached(symbol):
			return self.quote_cache.from_cache(symbol)

		url = "https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?range={range}&interval={interval}"
		res = requests.get(
			url.format(symbol=symbol, range=range), 
			headers=headers,
		)

		if res.status_code != 200:
			return None

		body = res.json()

		if body["chart"]["error"] is not None:
			return None

		body = body["chart"]["result"][0]

		if self.quote_cache is not None:
			self.quote_cache.to_cache(symbol, body)

		return body