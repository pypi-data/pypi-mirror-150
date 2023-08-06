from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Quote:
	
	timestamp: int

	open: float

	close: float

	high: float

	low: float

	volume: int

	def get_datetime_fmt(self)-> str:
		ts = datetime.fromtimestamp(self.timestamp)
		return ts.strftime("%Y-%m-%d %H:%M:%S")
