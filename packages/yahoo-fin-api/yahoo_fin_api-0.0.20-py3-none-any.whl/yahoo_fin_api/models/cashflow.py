from __future__ import annotations
from typing import List
from dataclasses import dataclass
import json
import yahoo_fin_api.utils as U
from yahoo_fin_api.models.base_model import Model


@dataclass
class CashFlow(Model):

	end_date: int | None

	net_income: int | None
	"""
	Derived from the company's income statement for the corresponding period and is calculated by deducting all expenses from the company's total revenues. 
	
	Measures the profitability of a company.
	"""

	depreciation: int | None
	"""
	Depreciation is a non-cash expense and occurs when tangible assets lose value over the course of time (over its "useful life"). 
	
	Eventually, these assets will have a value of zero, because they will no longer be useful to the business. 
	
	Amortization refers to the practice of spreading an intangible asset's cost over the asset's useful life.
	"""

	change_to_net_income: int | None

	change_to_account_receivables: int | None
	"""
	Refers to the amount customers owe for products/services delivered to them, but not yet paid for (to the company). 
	
	Increases (decreases) in accounts receivable will therefore be deducted (added) to net income.
	"""

	change_to_liabilities: int | None

	change_to_inventory: int | None

	change_to_operating_activities: int | None

	total_cash_from_operating_activities: int | None

	capital_expenditures: int | None

	investments: int | None
	"""
	Shows how much money the company generated or lost from investments made from the excess cash the company generated. 
	
	These investments (i.e., bonds) are made to get better returns than what's possible in a savings account or money market fund, for example.
	"""

	other_cashflows_from_investing_activities: int | None

	total_cashflows_from_investing_activities: int | None

	dividends_paid: int | None
	"""
	Total amount of dividends paid to shareholders over the period. 
	
	Only relevant if the company issues dividends.
	"""

	net_borrowings: int | None

	other_cashflows_from_financing_activities: int | None

	total_cash_from_financing_activities: int | None

	change_in_cash: int | None

	repurchase_of_stock: int | None
	"""
	When a company buybacks stock from the public stock market, thereby causing the number of outstanding shares in the company to decrease.
	"""

	issuance_of_stock: int | None

	def free_cash_flow(self, formatted: bool = False)-> int | str | None:
		"""
		One of the most important numbers you can calculate from the cash flow statement is free cash flow (FCF). 
		
		FCF tells investors and analysts how much cash a business generates after growing and maintaining its business. 
		
		This cash can therefore be paid to shareholders as a dividend, be used to pay down debt, buyback shares, or to just keep as cash on the balance sheet for any future possible investment opportunity.
		"""
		if self.total_cash_from_operating_activities is None or self.capital_expenditures is None:
			return None

		val = self.total_cash_from_operating_activities - self.capital_expenditures
		return U.format_amount(val) if formatted else val

@dataclass
class CashFlows:

	symbol: str | None

	title: str | None

	cashflows: List[CashFlow]

	@staticmethod
	def from_input_file(path: str)-> CashFlows | None:
		with open(path, "r") as file:
			data = json.loads(file.read())
			return CashFlows.from_dict(data)

	@staticmethod
	def from_dict(data: dict)-> CashFlows | None:
		symbol = U.extract_key(data, "quoteType", "symbol")
		title = U.extract_key(data, "quoteType", "longName")
		data = U.extract_key(data, "cashflowStatementHistory", "cashflowStatements")
		if data is None or symbol is None:
			return None

		return CashFlows(
			symbol,
			title,
			[
				CashFlow(
					U.extract_key(d, "endDate", "raw"), 
					U.extract_key(d, "netIncome", "raw"),
					U.extract_key(d, "depreciation", "raw"),
					U.extract_key(d, "changeToNetincome", "raw"),
					U.extract_key(d, "changeToAccountReceivables", "raw"),
					U.extract_key(d, "changeToLiabilities", "raw"),
					U.extract_key(d, "changeToInventory", "raw"),
					U.extract_key(d, "changeToOperatingActivities", "raw"),
					U.extract_key(d, "totalCashFromOperatingActivities", "raw"),
					U.extract_key(d, "capitalExpenditures", "raw"),
					U.extract_key(d, "investments", "raw"),
					U.extract_key(d, "otherCashflowsFromInvestingActivities", "raw"),
					U.extract_key(d, "totalCashflowsFromInvestingActivities", "raw"),
					U.extract_key(d, "dividendsPaid", "raw"),
					U.extract_key(d, "netBorrowings", "raw"),
					U.extract_key(d, "otherCashflowsFromFinancingActivities", "raw"),
					U.extract_key(d, "totalCashFromFinancingActivities", "raw"),
					U.extract_key(d, "changeInCash", "raw"),
					U.extract_key(d, "repurchaseOfStock", "raw"),
					U.extract_key(d, "issuanceOfStock", "raw"),
				) for d in data
			]
		)
