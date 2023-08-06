from __future__ import annotations
from datetime import datetime

class Model:

	def fmt_end_date(self)-> str | None:
		if self.end_date is None: # type: ignore 
			return None
		ts = datetime.fromtimestamp(self.end_date) # type: ignore 
		return ts.strftime("%Y-%m-%d")