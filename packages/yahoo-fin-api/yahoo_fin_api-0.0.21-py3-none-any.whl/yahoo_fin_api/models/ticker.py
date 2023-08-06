from __future__ import annotations
from typing import List
from dataclasses import dataclass
from yahoo_fin_api.models.balance_sheet import BalanceSheet
from yahoo_fin_api.models.income_statement import IncomeStatement
import yahoo_fin_api.utils as U
from yahoo_fin_api.models import (
	FinancialData, 
	SummaryDetail, 
	CashFlow,
	CashFlows,
	BalanceSheets,
	IncomeStatements,
	KeyStatistics,
)

@dataclass
class Ticker:

	symbol: str | None

	title: str | None

	financial_data: FinancialData | None

	summary_detail: SummaryDetail | None

	cashflows: CashFlows | None

	balance_sheets: BalanceSheets | None

	income_statements: IncomeStatements | None

	key_statistics: KeyStatistics | None

	def get_cashflows(self)-> List[CashFlow] | None:
		if self.cashflows is None:
			return None
		return self.cashflows.cashflows

	def get_income_statements(self)-> List[IncomeStatement] | None:
		if self.income_statements is None:
			return None
		return self.income_statements.income_statements

	def get_balance_sheets(self)-> List[BalanceSheet] | None:
		if self.balance_sheets is None:
			return None
		return self.balance_sheets.balance_sheets

	@staticmethod
	def from_dict(data: dict)-> Ticker | None:
		symbol = U.extract_key(data, "quoteType", "symbol")
		title = U.extract_key(data, "quoteType", "longName")
		if symbol is None:
			return None

		return Ticker(
			symbol,
			title,
			FinancialData.from_dict(data),
			SummaryDetail.from_dict(data),
			CashFlows.from_dict(data),
			BalanceSheets.from_dict(data),
			IncomeStatements.from_dict(data),
			KeyStatistics.from_dict(data),
		)

