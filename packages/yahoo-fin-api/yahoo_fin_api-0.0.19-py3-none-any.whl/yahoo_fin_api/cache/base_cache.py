
class BaseCache:
	def is_cached(self, symbol: str)-> bool:
		raise Exception("method 'is_cached' not implemented")

	def from_cache(self, symbol: str)-> dict:
		raise Exception("method 'from_cache' not implemented")

	def to_cache(self, symbol: str, body: dict)-> None:
		raise Exception("method 'to_cache' not implemented")

	def clear_cache(self, symbol: str)-> bool:
		raise Exception("method 'clear_cache' not implemented")