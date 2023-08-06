from __future__ import annotations
from typing import List
from dataclasses import dataclass
import json
import yahoo_fin_api.utils as U
from yahoo_fin_api.models.base_model import Model


@dataclass
class BalanceSheet(Model):
	"""
	A balance sheet is a financial statement that reports a company's assets, liabilities, and shareholder equity.
	
	It provides a snapshot of a company's finances (what it owns and owes) as of the date of publication.
	"""

	end_date: int | None

	cash: int | None
	"""
	Cash or company assets that can be converted into cash quickly. 
	
	The most liquid current asset.
	"""

	short_term_investments: int | None

	net_receivables: int | None
	"""
	Money customers owe a company that has not been paid yet.
	"""

	inventory: int | None
	"""
	A company's products that are awaiting to be sold to customers, along with raw materials and work-in-progress that will eventually become finished goods.
	
	If the inventory line item appears high, this may imply the company has inferior products, product deficiencies, out-of-favor products, or a similar factor which is causing its products to not sell in stores. 
	
	Moreover, this may be a sign of poor sales and/or marketing departments. 
	
	Naturally, if products are not needed from the company's inventory, this can lead to higher storage costs for the company, thereby reducing profit margins.
	"""

	other_current_assets: int | None

	total_current_assets: int | None

	long_term_investments: int | None

	property_plant_equipment: int | None
	"""
	These are the company's assets that are essential to the normal operations of the business. 
	
	Typically, this will be a large figure on a company's balance sheet and includes land, office, machinery, vehicles, factories, and other physical assets that cannot be easily converted into cash.
	"""

	other_assets: int | None

	total_assets: int | None

	accounts_payable: int | None
	"""
	Represents payment due to lenders. 
	
	Raw materials purchased from a supplier, but not yet paid for by the company, is a common example of what will be recorded as accounts payable. 
	
	Companies are responsible for paying their suppliers, and if accounts payable appears too big, this may be a warning sign to not invest in the company. 
	
	Put simply, this indicates that a company cannot pay its short-term debts as it owes its suppliers a lot and may fail at settling its debts. 
	
	Obviously, if a company regularly fails to pay off its short-term debts, it may become bankrupt rather quickly.
	"""

	short_term_debt: int | None

	other_current_liab: int | None

	long_term_debt: int | None
	"""
	Refers to a catch-all phrase for when a company takes on a loan and repayments are made for multiple years to pay down the loan. 
	
	Types of long term debt include bank debt, mortgages, bonds, and debentures.
	"""

	other_liab: int | None

	total_current_liabilities: int | None

	total_liab: int | None

	common_stock: int | None
	"""
	Represents the shareholders' investment in the business. 
	
	Common stock is sold, purchased, and resold in a stock exchange, and given a publicly listed price. 
	
	Some pay dividends, typically on a quarterly basis, and ownership of common stock will give you voting rights in a company's policies and procedures.
	"""

	retained_earnings: int | None
	"""
	Amount of earnings a company has left over after paying dividends to its shareholders. 
	
	In other words, retained earnings is any profit a company retains that has not been distributed to its owners, which can be used to buy assets and invest in the future of the company.
	"""

	treasury_stock: int | None
	"""
	Refers to shares that have been repurchased by the issuing company that were previously outstanding. 
	
	Also known as "reacquired stock," and causes total shareholders' equity to be reduced.
	"""

	other_stockholder_equity: int | None

	total_stockholder_equity: int | None

	net_tangible_assets: int | None
	"""
	Physical assets that can be touched. 
	
	This includes plant, property, and equipment (PP&E). 
	
	Most tangible assets depreciate in value over time as well.
	"""

	def current_ratio(self)-> float | None:
		"""
		You can calculate the current ratio to ensure the company you're evaluating has enough short-term assets to cover its short-term debt obligations.
		
		Although this liquidity ratio should be compared to its competitors and the industry, the current ratio should be above 2.0, and no less than 1.5. 
		
		In general, this helps to prove that the company has enough cash to cover any debts that are due within the next 12 months.
		"""
		if self.total_current_assets is None or self.total_current_liabilities is None:
			return None
		return round(self.total_current_assets / self.total_current_liabilities, 2)

	def quick_ratio(self)-> float | None:
		"""
		If you want be more conservative, you can also calculate the quick ratio, as shown below:
		
		Ultimately, this liquidity ratio is more conservative than the current ratio because it doesn't include inventory, which is more difficult to liquidate, thereby focusing on the company's more liquid assets.
		"""
		if self.total_current_assets is None or self.inventory is None or self.total_current_liabilities is None:
			return None
		return round(
			(self.total_current_assets - self.inventory) / self.total_current_liabilities, 
			2
		)

	def working_capital(self)-> float | None:
		"""
		Working capital, as another liquidity figure, is simply the difference between a company's current assets and current liabilities.
		
		Clearly, if working capital is greater, it means that the company has more current assets than current liabilities.
		
		If this number seems too high, this may be an indication of a company that is not investing its excess cash. 
		
		However, a positive working capital number is generally good, as it means the capital can fund the company's operations and invest in future growth opportunities.
		
		If working capital is negative, this may be a sign of short-term liquidity issues with the company. For example, this may be due to a large cash outlay purchase for raw goods, with the accounts payable account increasing substantially.
		"""
		if self.total_current_assets is None or self.total_current_liabilities is None:
			return None
		return self.total_current_assets - self.total_current_liabilities

	def shareholders_equity(self)-> float | None:
		"""
		Shareholders' equity, as the name suggests, refers to the amount owners of a company (e.g., investors, managers, institutions, etc) have invested in the business, through investments and by retaining earnings over time. 
		
		So, when you purchase stock in a company and gain partial ownership, the money that goes into the company is considered shareholders' equity.
		"""
		if self.total_assets is None or self.total_liab is None:
			return None
		return self.total_assets - self.total_liab

	def debt_to_equity(self)-> float | None:
		"""
		To quickly analyze debt levels, you can use the debt-to-equity (D/E) ratio and look for a ratio close to 0.5.
		
		Obviously, if the company you're evaluating has no debt, there's no risk of the company defaulting. However, there's always a risk of default if the company has debt, and the more debt a company has, the greater this risk.
		"""
		shareholders_equity = self.shareholders_equity()
		if self.short_term_debt is None or self.long_term_debt is None or shareholders_equity is None:
			return None
		return round(
			(self.short_term_debt + self.long_term_debt) / shareholders_equity,
			2
		)

@dataclass
class BalanceSheets:

	symbol: str | None

	title: str | None

	balance_sheets: List[BalanceSheet]

	@staticmethod
	def from_input_file(path: str)-> BalanceSheets | None:
		with open(path, "r") as file:
			data = json.loads(file.read())
			return BalanceSheets.from_dict(data)

	@staticmethod
	def from_dict(data: dict)-> BalanceSheets | None:
		symbol = U.extract_key(data, "quoteType", "symbol")
		title = U.extract_key(data, "quoteType", "longName")
		data = U.extract_key(data, "balanceSheetHistory", "balanceSheetStatements")
		if data is None or symbol is None:
			return None

		return BalanceSheets(
			symbol,
			title,
			[
				BalanceSheet(
					U.extract_key(d, "endDate", "raw"), 
					U.extract_key(d, "cash", "raw"),
					U.extract_key(d, "shortTermInvestments", "raw"),
					U.extract_key(d, "netReceivables", "raw"),
					U.extract_key(d, "inventory", "raw"),
					U.extract_key(d, "otherCurrentAssets", "raw"),
					U.extract_key(d, "totalCurrentAssets", "raw"),
					U.extract_key(d, "longTermInvestments", "raw"),
					U.extract_key(d, "propertyPlantEquipment", "raw"),
					U.extract_key(d, "otherAssets", "raw"),
					U.extract_key(d, "totalAssets", "raw"),
					U.extract_key(d, "accountsPayable", "raw"),
					U.extract_key(d, "shortLongTermDebt", "raw"),
					U.extract_key(d, "otherCurrentLiab", "raw"),
					U.extract_key(d, "longTermDebt", "raw"),
					U.extract_key(d, "otherLiab", "raw"),
					U.extract_key(d, "totalCurrentLiabilities", "raw"),
					U.extract_key(d, "totalLiab", "raw"),
					U.extract_key(d, "commonStock", "raw"),
					U.extract_key(d, "retainedEarnings", "raw"),
					U.extract_key(d, "treasuryStock", "raw"),
					U.extract_key(d, "otherStockholderEquity", "raw"),
					U.extract_key(d, "totalStockholderEquity", "raw"),
					U.extract_key(d, "netTangibleAssets", "raw"),
				) for d in data
			]
		)
