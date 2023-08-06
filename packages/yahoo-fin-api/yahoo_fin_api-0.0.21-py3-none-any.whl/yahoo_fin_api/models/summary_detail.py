from __future__ import annotations
from dataclasses import dataclass
import json
import yahoo_fin_api.utils as U
from yahoo_fin_api.models.base_model import Model


@dataclass
class SummaryDetail(Model):

	symbol: str | None

	title: str | None

	price_hint: int | None

	previous_close: float | None

	open: float | None

	day_low: float | None

	day_high: float | None

	regular_market_previous_close: float | None

	regular_market_open: float | None

	regular_market_day_low: float | None

	regular_market_day_high: float | None

	dividend_rate: float | None
	"""
	The dividend rate is an estimate of the dividend-only return of an investment such as on a stock or mutual fund. 
	
	Assuming the dividend amount is not raised or lowered, the rate will rise when the price of the stock falls. 
	
	And conversely, it will fall when the price of the stock rises. 
	
	Because dividend rates change relative to the stock price, it can often look unusually high for stocks that are falling in value quickly.
	"""

	dividend_yield: float | None
	"""
	The dividend yield, expressed as a percentage, is a financial ratio (dividend/price) that shows how much a company pays out in dividends each year relative to its stock price.
	"""

	ex_dividend_date: int | None

	payout_ratio: float | None

	five_year_avg_dividend_yield: float | None

	beta: float | None
	"""
	Beta is a measure of a stock's volatility in relation to the overall market. 
	
	By definition, the market, such as the S&P 500 Index, has a beta of 1.0, and individual stocks are ranked according to how much they deviate from the market.
	
	A stock that swings more than the market over time has a beta above 1.0. 
	
	If a stock moves less than the market, the stock's beta is less than 1.0. 
	
	High-beta stocks are supposed to be riskier but provide higher return potential; low-beta stocks pose less risk but also lower returns.
	"""

	trailing_pe: float | None
	"""
	Trailing price-to-earnings (P/E) is a relative valuation multiple that is based on the last 12 months of actual earnings. 
	
	It is calculated by taking the current stock price and dividing it by the trailing earnings per share (EPS) for the past 12 months.

	When people refer to the P/E ratio generically, they are typically referring to the trailing P/E.
	"""

	forward_pe: float | None
	"""
	Forward price-to-earnings (forward P/E) is a version of the ratio of price-to-earnings (P/E) that uses forecasted earnings for the P/E calculation. 
	
	While the earnings used in this formula are just an estimate and not as reliable as current or historical earnings data, there are still benefits to estimated P/E analysis.
	"""

	volume: int | None

	regular_market_volume: int | None

	average_volume: int | None

	average_volume_10_days: int | None

	average_daily_volume_10_day: int | None

	market_cap: int | None
	"""
	Market capitalization refers to the total dollar market value of a company's outstanding shares of stock. 
	
	Commonly referred to as "market cap," it's calculated by multiplying the total number of a company's outstanding shares by the current market price of one share.
	"""

	fifty_two_week_low: float | None

	fifty_two_week_high: float | None

	@staticmethod
	def from_input_file(path: str)-> SummaryDetail | None:
		with open(path, "r") as file:
			data = json.loads(file.read())
			return SummaryDetail.from_dict(data)

	@staticmethod
	def from_dict(data: dict)-> SummaryDetail | None:
		symbol = U.extract_key(data, "quoteType", "symbol")
		title = U.extract_key(data, "quoteType", "longName")
		d = U.extract_key(data, "summaryDetail")
		if d is None or symbol is None:
			return None

		return SummaryDetail(
			symbol,
			title,
			U.extract_key(d, "priceHint", "raw"),
			U.extract_key(d, "previousClose", "raw"),
			U.extract_key(d, "open", "raw"),
			U.extract_key(d, "dayLow", "raw"),
			U.extract_key(d, "dayHigh", "raw"),
			U.extract_key(d, "regularMarketPreviousClose", "raw"),
			U.extract_key(d, "regularMarketOpen", "raw"),
			U.extract_key(d, "regularMarketDayLow", "raw"),
			U.extract_key(d, "regularMarketDayHigh", "raw"),
			U.extract_key(d, "dividendRate", "raw"),
			U.extract_key(d, "dividendYield", "raw"),
			U.extract_key(d, "exDividendDate", "raw"),
			U.extract_key(d, "payoutRatio", "raw"),
			U.extract_key(d, "fiveYearAvgDividendYield", "raw"),
			U.extract_key(d, "beta", "raw"),
			U.extract_key(d, "trailingPE", "raw"),
			U.extract_key(d, "forwardPE", "raw"),
			U.extract_key(d, "volume", "raw"),
			U.extract_key(d, "regularMarketVolume", "raw"),
			U.extract_key(d, "averageVolume", "raw"),
			U.extract_key(d, "averageVolume10days", "raw"),
			U.extract_key(d, "averageDailyVolume10Day", "raw"),
			U.extract_key(d, "marketCap", "raw"),
			U.extract_key(d, "fiftyTwoWeekLow", "raw"),
			U.extract_key(d, "fiftyTwoWeekHigh", "raw"),
		)