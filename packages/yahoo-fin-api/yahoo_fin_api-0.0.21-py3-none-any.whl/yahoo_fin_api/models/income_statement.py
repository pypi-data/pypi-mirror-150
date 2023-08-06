from __future__ import annotations
from typing import List
from dataclasses import dataclass
import json
import yahoo_fin_api.utils as U
from yahoo_fin_api.models.base_model import Model


@dataclass
class IncomeStatement(Model):

	end_date: int | None

	total_revenue: int | None
	"""
	Revenue (aka Net/Gross Sales or Income)

	The top-line figure that shows the income earned by a business for any products/services sold.
	"""

	cost_of_revenue: int | None
	"""
	Costs of Goods Sold (COGS) (aka Cost of Sales)

	Direct costs associated with the production of the goods sold by a business.
	"""

	gross_profit: int | None
	"""
	Gross Profit (aka Gross Income) 
	
	Total revenue less COGS.
	"""

	research_development: int | None
	"""
	Research and development (R&D) include activities that companies undertake to innovate and introduce new products and services. 
	
	It is often the first stage in the development process. The goal is typically to take new products and services to market and add to the company's bottom line.
	"""

	selling_general_administrative: int | None
	"""
	All everyday operating expenses of running a business that are not included in the production of goods or delivery of services. 
	
	Typical SG&A items include rent, salaries, advertising and marketing expenses and distribution costs.
	
	In fact, this line item includes nearly all business costs not directly attributable to making a product or performing a service. SG&A includes the costs of managing the company and the expenses of delivering its products or services.
	"""

	other_operating_expenses: int | None

	total_operating_expenses: int | None
	"""
	Operating Expenses (OPEX) 
	
	Costs associated with normal operations of a business. 
	
	Often includes selling, general, and administrative expense (SG&A) and depreciation (when assets lose value over time).
	"""

	operating_income: int | None
	"""
	Operating Income (aka Operating Profit or Recurring Profit) 
	
	Gross profit less operating expenses. 
	
	Very similar to EBIT.
	"""

	total_other_income_expense_net: int | None

	ebit: int | None
	"""
	Earnings (income) before interest and taxes.
	"""

	interest_expense: int | None
	"""
	An interest expense is the cost incurred by an entity for borrowed funds.

	It represents interest payable on any borrowings - bonds, loans, convertible debt or lines of credit.
	
	Interest expense on the income statement represents interest accrued during the period covered by the financial statements, and not the amount of interest paid over that period.
	"""

	income_before_tax: int | None
	"""
	Income before taxes represents a company's profitability after all deductions, besides taxes, have been made against revenue. 
	
	It deducts non-operating expenses, which are simply expenses incurred from activities not related to the core operations of the business.
	"""

	income_tax_expense: int | None
	"""
	Income tax expense is arrived at by multiplying taxable income by the effective tax rate.
	"""

	net_income_from_continuing_ops: int | None
	"""
	Income from continuing operations is also known as operating income. 
	
	Continuing operations are the primary source of income for most successful businesses.
	"""

	discontinued_operations: int | None
	"""
	In financial accounting, discontinued operations refer to parts of a company's core business or product line that have been divested or shut down, and which are reported separately from continuing operations on the income statement.
	"""

	effect_of_accounting_charges: int | None

	net_income: int | None
	"""
	Net Income (NI) (aka Net Profit, Net Sales, or Net Earnings)
	
	The bottom-line number left after subtracting all expenses, taxes, and costs from revenue. 
	
	Equal to EBT less taxes.
	"""

	net_income_applicable_to_common_shares: int | None
	"""
	Net income applicable to common shares is a figure on an organization's income statement. 
	
	It tells investors how much income is left over that could be distributed to common shareholders. 
	
	The figure is also called earnings available for common shares.
	"""

	def gross_profit_margin(self)-> float | None:
		"""
		Gross profit margin can be calculated as well, and gives us a better idea on the percentage of revenue that exceeds the COGS.
		"""
		if self.gross_profit is None or self.total_revenue is None:
			return None
		return round(self.gross_profit / self.total_revenue, 2)


@dataclass
class IncomeStatements:

	symbol: str | None

	title: str | None

	income_statements: List[IncomeStatement]

	@staticmethod
	def from_input_file(path: str)-> IncomeStatements | None:
		with open(path, "r") as file:
			data = json.loads(file.read())
			return IncomeStatements.from_dict(data)

	@staticmethod
	def from_dict(data: dict)-> IncomeStatements | None:
		symbol = U.extract_key(data, "quoteType", "symbol")
		title = U.extract_key(data, "quoteType", "longName")
		data = U.extract_key(data, "incomeStatementHistory", "incomeStatementHistory")
		if data is None or symbol is None:
			return None

		return IncomeStatements(
			symbol,
			title,
			[
				IncomeStatement(
					U.extract_key(d, "endDate", "raw"), 
					U.extract_key(d, "totalRevenue", "raw"),
					U.extract_key(d, "costOfRevenue", "raw"),
					U.extract_key(d, "grossProfit", "raw"),
					U.extract_key(d, "researchDevelopment", "raw"),
					U.extract_key(d, "sellingGeneralAdministrative", "raw"),
					U.extract_key(d, "otherOperatingExpenses", "raw"),
					U.extract_key(d, "totalOperatingExpenses", "raw"),
					U.extract_key(d, "operatingIncome", "raw"),
					U.extract_key(d, "totalOtherIncomeExpenseNet", "raw"),
					U.extract_key(d, "ebit", "raw"),
					U.extract_key(d, "interestExpense", "raw"),
					U.extract_key(d, "incomeBeforeTax", "raw"),
					U.extract_key(d, "incomeTaxExpense", "raw"),
					U.extract_key(d, "netIncomeFromContinuingOps", "raw"),
					U.extract_key(d, "discontinuedOperations", "raw"),
					U.extract_key(d, "effectOfAccountingCharges", "raw"),
					U.extract_key(d, "netIncome", "raw"),
					U.extract_key(d, "netIncomeApplicableToCommonShares", "raw")
				) for d in data
			]
		)
