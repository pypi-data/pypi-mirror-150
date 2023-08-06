from __future__ import annotations
from dataclasses import dataclass
import json
import yahoo_fin_api.utils as U
from yahoo_fin_api.models.base_model import Model


@dataclass
class KeyStatistics(Model):

	symbol: str | None

	title: str | None

	price_hint: int | None

	enterprise_value: int | None

	forward_pe: float | None

	profit_margins: float | None

	float_shares: int | None

	shares_outstanding: int | None

	held_percent_insiders: float | None

	held_percent_institutions: float | None

	book_value: float | None

	price_to_book: float | None

	earnings_quarterly_growth: float | None

	trailing_eps: float | None

	forward_eps: float | None

	peg_ratio: float | None

	enterprise_to_revenue: float | None

	enterprise_to_ebitda: float | None

	last_dividend_value: float | None

	@staticmethod
	def from_input_file(path: str)-> KeyStatistics | None:
		with open(path, "r") as file:
			data = json.loads(file.read())
			return KeyStatistics.from_dict(data)

	@staticmethod
	def from_dict(data: dict)-> KeyStatistics | None:
		symbol = U.extract_key(data, "quoteType", "symbol")
		title = U.extract_key(data, "quoteType", "longName")
		d = U.extract_key(data, "defaultKeyStatistics")
		if d is None or symbol is None:
			return None

		return KeyStatistics(
			symbol,
			title,
			U.extract_key(d, "priceHint", "raw"),
			U.extract_key(d, "enterpriseValue", "raw"),
			U.extract_key(d, "forwardPE", "raw"),
			U.extract_key(d, "profitMargins", "raw"),
			U.extract_key(d, "floatShares", "raw"),
			U.extract_key(d, "sharesOutstanding", "raw"),
			U.extract_key(d, "heldPercentInsiders", "raw"),
			U.extract_key(d, "heldPercentInstitutions", "raw"),
			U.extract_key(d, "bookValue", "raw"),
			U.extract_key(d, "priceToBook", "raw"),
			U.extract_key(d, "earningsQuarterlyGrowth", "raw"),
			U.extract_key(d, "trailingEps", "raw"),
			U.extract_key(d, "forwardEps", "raw"),
			U.extract_key(d, "pegRatio", "raw"),
			U.extract_key(d, "enterpriseToRevenue", "raw"),
			U.extract_key(d, "enterpriseToEbitda", "raw"),
			U.extract_key(d, "lastDividendValue", "raw"),
		)