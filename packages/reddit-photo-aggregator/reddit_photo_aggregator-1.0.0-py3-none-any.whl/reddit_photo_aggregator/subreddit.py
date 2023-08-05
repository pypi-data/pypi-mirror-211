import requests
from bs4 import BeautifulSoup
from .image import Image
from .image_validator import ImageURLValidator
from .user_agent import get_user_agent
from .sorting import SortBy


class SubReddit:
	def __init__(self, name: str) -> None:
		self.__name = self.__format_name(name)
		self.__images = []

	@property
	def loaded_images(self) -> list[Image]:
		return self.__images

	@property
	def url(self) -> str:
		return f'https://old.reddit.com/r/{self.__name}'

	def discover_images(self, sorted_by=SortBy.hot) -> int:
		headers = {
			'User-Agent': get_user_agent()
		}

		with requests.get(self.url + sorted_by, headers=headers) as r:
				soup = BeautifulSoup(r.content, 'html.parser')

		thumbnails = soup.find_all('a', {'class': 'thumbnail'})
		for thumbnail in thumbnails:
			data_url: str = thumbnail.parent.attrs.get('data-url')

			if ImageURLValidator._is_image_url_valid(data_url):
				self.__images.append(Image(data_url))

		return len(self.__images)

	def __format_name(self, name: str) -> str:
		new_name = name

		if '/' in new_name:
			if new_name.endswith('/'):
				new_name = new_name[:-1:]
			new_name = new_name.split('/')[-1]

		if new_name == name:
			return name
		else:
			return self.__format_name(new_name)

	def __repr__(self) -> str:
		return f'{self.__class__.__name__}[{self.__name}]'


if __name__ == '__main__':
	print(SubReddit('LandscapePhotography'))
	print(SubReddit('r/LandscapePhotography'))
	print(SubReddit('r/EarthPorn/'))
	print(SubReddit('https://old.reddit.com/r/LandscapePhotography/'))
	print(SubReddit('https://www.reddit.com/r/photocritique/'))
