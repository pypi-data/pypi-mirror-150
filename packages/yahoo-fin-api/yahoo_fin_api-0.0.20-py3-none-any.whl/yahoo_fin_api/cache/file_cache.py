import json
from pathlib import Path
from datetime import datetime
from yahoo_fin_api.cache.base_cache import BaseCache

class FileCache(BaseCache):

	def __init__(self, output_dir: str, key_prefix: str = "", ttl: int = 60)-> None:
		super().__init__()

		Path(output_dir).mkdir(parents=True, exist_ok=True)

		self.output_dir = output_dir
		self.key_prefix = key_prefix
		self.ttl = ttl

	def __cache_file(self, symbol: str)-> str:
		return f"{self.output_dir}/{self.key_prefix}_{symbol}.json"

	def is_cached(self, symbol: str)-> bool:
		symbol = symbol.upper()
		file = Path(self.__cache_file(symbol))
		if file.is_file() == False:
			return False

		now =  int(datetime.now().timestamp())
		modified = int(file.stat().st_mtime)
		if (now - modified) > self.ttl:
			print(f"cache has expired for {symbol}")
			return False

		return True

	def from_cache(self, symbol: str)-> dict:
		symbol = symbol.upper()
		with open(self.__cache_file(symbol), "r") as file:
			return json.loads(file.read())

	def to_cache(self, symbol: str, body: dict)-> None:
		symbol = symbol.upper()
		with open(self.__cache_file(symbol), "w") as file:
			file.write(json.dumps(body))

	def clear_cache(self, symbol: str)-> bool:
		symbol = symbol.upper()
		if self.is_cached(symbol) is False:
			return True

		Path(self.__cache_file(symbol)).unlink()

		return True

