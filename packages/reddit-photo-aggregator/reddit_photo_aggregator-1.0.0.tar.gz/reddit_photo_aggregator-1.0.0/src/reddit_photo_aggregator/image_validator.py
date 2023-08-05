from urllib.parse import urlparse


class ImageURLValidator:
	__image_host_whitelist = ''
	__image_extension_whitelist = ''

	@classmethod
	def set_image_host_whitelist(cls, host: list[str]) -> None:
		cls.__image_host_whitelist = ';'.join(host)

	@classmethod
	def set_image_extension_whitelist(cls, extension: str|list[str]) -> None:
		cls.__image_extension_whitelist = ';'.join(extension)

	@classmethod
	def _is_image_url_valid(cls, url: str) -> bool:
		domain = urlparse(url).netloc
		if domain.startswith('www.'):
			domain = domain[4::]
		possibly_an_extension = url.split('.')[-1]

		if not url.startswith('http'):
			return False

		if domain == '' or domain not in cls.__image_host_whitelist:
			return False

		if not possibly_an_extension in cls.__image_extension_whitelist:
			return False

		return True


if __name__ == '__main__':
	ImageURLValidator.set_image_extension_whitelist([
		'png',
		'jpg',
	])

	ImageURLValidator.set_image_host_whitelist([
		'reddit.com',
		'imagur.com',
		'imbb.com',
	])

	assert ImageURLValidator._is_image_url_valid('https://www.reddit.com/gallery/bf5sg34.jpg') is True
	assert ImageURLValidator._is_image_url_valid('https://www.imagur.com/bf5sg34.png') is True
	assert ImageURLValidator._is_image_url_valid('https://imagur.com/bf5sg34.png') is True
	assert ImageURLValidator._is_image_url_valid('https://www.imagur.com/bf5sg34.png') is True
	assert ImageURLValidator._is_image_url_valid('https://imagur.com/bf5sg34.webp') is False
	assert ImageURLValidator._is_image_url_valid('https://imagur.net/bf5sg34.png') is False
	assert ImageURLValidator._is_image_url_valid('malicious.co.uk/bf5sg34.png') is False

