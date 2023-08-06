from __future__ import annotations

def format_amount(value: float | int | None)-> str:
	return "${:,}".format(value) if value is not None else "$0"

def calculate_growth_rate(initial: float, last: float)-> float:
	diff = (last - initial) / initial * 100
	return round(diff)

def extract_key(data: dict, *keys: str):
	for k in keys:
		if k in data:
			data = data[k]
		else:
			return None

	return data