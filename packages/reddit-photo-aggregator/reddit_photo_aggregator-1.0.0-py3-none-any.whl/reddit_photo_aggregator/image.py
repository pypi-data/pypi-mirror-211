import os
import requests
from .exceptions import ImageRetrieveError


class Image:
	def __init__(self, url: str) -> None:
		self.__url = url
		self.__content: bytes = None

	@property
	def filename(self) -> str:
		return self.__url.split('/')[-1]

	def load(self) -> None:
		if self.__content is not None:
			return

		with requests.get(self.__url) as r:
			if r.status_code == 200:
				self.__content = r.content
				return

			raise ImageRetrieveError(f'Image retrieval failed with status code: {r.status_code} and content: {r.content}')

	def __check_dest(self, path: str) -> None:
		if not os.path.exists('images'):
			os.mkdir('images')

	def save(self, to: str='./'):
		self.__check_dest(to)

		if self.__content is None:
			self.load()

		with open(os.path.join(to, self.filename), 'wb') as f:
			f.write(self.__content)
