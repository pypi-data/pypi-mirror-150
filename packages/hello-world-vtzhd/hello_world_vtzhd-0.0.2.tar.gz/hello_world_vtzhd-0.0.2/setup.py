import setuptools

# Открытие qweREйцуqwewADqwME.md и присвоение его long_description.
with open("README.md", "r") as fh:
	long_description = fh.read()

# Определение2 requests как requirements для того, чтобы этот пакет работал. Зависимости проекта.
# requirements = ["requests<=2.21.0"]

setuptools.setup(
	name="hello_world_vtzhd",
	version="0.0.2",
	author="vtzhd",
	author_email="i@zhdanov-1.ru",
	description="Hello World package",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/vitzhdanov/test_lib.git",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)