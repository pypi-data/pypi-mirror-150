from __future__ import annotations
from dataclasses import dataclass
import json
import yahoo_fin_api.utils as U
from yahoo_fin_api.models.base_model import Model


@dataclass
class FinancialData(Model):

	symbol: str | None

	title: str | None

	current_price: float | None

	target_high_price: float | None
	"""
	A price target is a price at which an analyst believes a stock to be fairly valued relative to its projected and historical earnings.
	"""

	target_low_price: float | None
	"""
	A price target is a price at which an analyst believes a stock to be fairly valued relative to its projected and historical earnings.
	"""

	target_mean_price: float | None

	target_median_price: float | None

	recommendation_mean: float | None

	recommendation_key: str | None

	number_of_analyst_opinions: int | None

	total_cash: int | None
	"""
	In order to calculate net cash, you must first add up all cash (not credit) receipts for a period. 
	
	This amount is often referred to as "gross cash". 
	
	Once totaled, cash outflows paid out for obligations and liabilities are deducted from gross cash; the difference is net cash.
	"""

	total_cash_per_share: float | None
	"""
	Cash per share tells us the percentage of a company's share price available to spend on strengthening the business, paying down debt, returning money to shareholders, and other positive campaigns.
	
	Paradoxically, too much cash per share can be a negative indicator of a company's health, because it may suggest an unwillingness by management to nurture forward-thinking measures.
	
	Cash per share is often considered a much more reliable indicator of financial health than earnings per share (EPS).
	"""

	ebitda: int | None
	"""
	EBITDA, or earnings before interest, taxes, depreciation, and amortization, is a measure of a company's overall financial performance and is used as an alternative to net income in some circumstances. 
	
	EBITDA, however, can be misleading because it does not reflect the cost of capital investments like property, plants, and equipment.
	"""

	total_debt: int | None
	"""
	Total debt includes long-term liabilities, such as mortgages and other loans that do not mature for several years, as well as short-term obligations, including loan payments, credit card, and accounts payable balances.
	"""

	quick_ratio: float | None
	"""
	The quick ratio measures a company's capacity to pay its current liabilities without needing to sell its inventory or obtain additional financing.

	The quick ratio is considered a more conservative measure than the current ratio, which includes all current assets as coverage for current liabilities.
	
	The higher the ratio result, the better a company's liquidity and financial health; the lower the ratio, the more likely the company will struggle with paying debts.
	"""

	current_ratio: float | None
	"""
	The current ratio is a liquidity ratio that measures a company's ability to pay short-term obligations or those due within one year. 
	
	It tells investors and analysts how a company can maximize the current assets on its balance sheet to satisfy its current debt and other payables.
	"""

	total_revenue: int | None
	"""
	Total revenue is the full amount of total sales of goods and services. 
	
	It is calculated by multiplying the total amount of goods and services sold by the price of the goods and services.
	"""

	debt_to_equity: float | None
	"""
	The debt-to-equity (D/E) ratio compares a company's total liabilities to its shareholder equity and can be used to evaluate how much leverage a company is using.

	Higher-leverage ratios tend to indicate a company or stock with higher risk to shareholders.

	However, the D/E ratio is difficult to compare across industry groups where ideal amounts of debt will vary.
	"""

	revenue_per_share: float | None
	"""
	Revenue per share is calculated as a company's revenue divided by the outstanding shares of its common stock.
	"""

	return_on_assets: float | None
	"""
	Return on assets is a metric that indicates a company's profitability in relation to its total assets.

	ROA can be used by management, analysts, and investors to determine whether a company uses its assets efficiently to generate a profit.

	You can calculate a company's ROA by dividing its net income by its total assets.
	"""

	return_on_equity: float | None
	"""
	Return on equity (ROE) is the measure of a company's net income divided by its shareholders' equity.

	ROE is a gauge of a corporation's profitability and how efficiently it generates those profits.

	ROE is expressed as a percentage and can be calculated for any company if net income and equity are both positive numbers.
	"""

	gross_profits: int | None
	"""
	Gross profit is the profit a company makes after deducting the costs associated with making and selling its products, or the costs associated with providing its services. 
	
	Gross profit will appear on a company's income statement and can be calculated by subtracting the cost of goods sold (COGS) from revenue (sales).
	"""

	free_cash_flow: float | None
	"""
	Free cash flow (FCF) is the cash a company generates after taking into consideration cash outflows that support its operations and maintain its capital assets. 
	
	In other words, free cash flow is the cash left over after a company pays for its operating expenses and capital expenditures.
	"""

	operating_cash_flow: int | None
	"""
	Operating cash flow (OCF) is a measure of the amount of cash generated by a company's normal business operations. 
	
	Operating cash flow indicates whether a company can generate sufficient positive cash flow to maintain and grow its operations, otherwise, it may require external financing for capital expansion.
	"""

	earnings_growth: float | None
	"""
	Earnings growth is the change in an entity's reported net income over a period of time. 
	
	The measure is usually a period-to-period comparison, such as from quarter to quarter, from year to year, or a comparison of the current quarter's results to those of the same quarter last year.
	"""

	revenue_growth: float | None
	"""
	Revenue growth refers to an increase in revenue over a period of time. 
	
	In accounting, revenue growth is the rate of increase in total revenues divided by total revenues from the same period in the previous year.
	"""

	gross_margins: float | None
	"""
	Gross margin equates to net sales minus the cost of goods sold. 
	
	The gross margin shows the amount of profit made before deducting selling, general, and administrative (SG&A) costs. 
	
	Gross margin can also be called gross profit margin, which is gross profit divided by net sales.
	"""

	ebitda_margins: float | None
	"""
	The EBITDA margin is a measure of a company's operating profit as a percentage of its revenue. 
	
	The acronym EBITDA stands for earnings before interest, taxes, depreciation, and amortization. 
	
	Knowing the EBITDA margin allows for a comparison of one company's real performance to others in its industry.
	"""

	operating_margins: float | None
	"""
	The operating margin measures how much profit a company makes on a dollar of sales after paying for variable costs of production, such as wages and raw materials, but before paying interest or tax. 
	
	It is calculated by dividing a company's operating income by its net sales. 
	
	Higher ratios are generally better, illustrating the company is efficient in its operations and is good at turning sales into profits. 
	"""

	profit_margins: float | None
	"""
	The net profit margin ratio is the percentage of a business's revenue left after deducting all expenses from total sales, divided by net revenue. 
	
	Net profit is total revenue minus all expenses.

	The profit margin is critical to a free-market economy driven by capitalism. 
	
	The margin must be high enough when compared with similar businesses to attract investors.
	"""

	@staticmethod
	def from_input_file(path: str)-> FinancialData | None:
		with open(path, "r") as file:
			data = json.loads(file.read())
			return FinancialData.from_dict(data)

	@staticmethod
	def from_dict(data: dict)-> FinancialData | None:
		symbol = U.extract_key(data, "quoteType", "symbol")
		title = U.extract_key(data, "quoteType", "longName")
		d = U.extract_key(data, "financialData")
		if d is None or symbol is None:
			return None

		return FinancialData(
			symbol,
			title,
			U.extract_key(d, "currentPrice", "raw"),
			U.extract_key(d, "targetHighPrice", "raw"),
			U.extract_key(d, "targetLowPrice", "raw"),
			U.extract_key(d, "targetMeanPrice", "raw"),
			U.extract_key(d, "targetMedianPrice", "raw"),
			U.extract_key(d, "recommendationMean", "raw"),
			U.extract_key(d, "recommendationKey"),
			U.extract_key(d, "numberOfAnalystOpinions", "raw"),
			U.extract_key(d, "totalCash", "raw"),
			U.extract_key(d, "totalCashPerShare", "raw"),
			U.extract_key(d, "ebitda", "raw"),
			U.extract_key(d, "totalDebt", "raw"),
			U.extract_key(d, "quickRatio", "raw"),
			U.extract_key(d, "currentRatio", "raw"),
			U.extract_key(d, "totalRevenue", "raw"),
			U.extract_key(d, "debtToEquity", "raw"),
			U.extract_key(d, "revenuePerShare", "raw"),
			U.extract_key(d, "returnOnAssets", "raw"),
			U.extract_key(d, "returnOnEquity", "raw"),
			U.extract_key(d, "grossProfits", "raw"),
			U.extract_key(d, "freeCashflow", "raw"),
			U.extract_key(d, "operatingCashflow", "raw"),
			U.extract_key(d, "earningsGrowth", "raw"),
			U.extract_key(d, "revenueGrowth", "raw"),
			U.extract_key(d, "grossMargins", "raw"),
			U.extract_key(d, "ebitdaMargins", "raw"),
			U.extract_key(d, "operatingMargins", "raw"),
			U.extract_key(d, "profitMargins", "raw"),
		)