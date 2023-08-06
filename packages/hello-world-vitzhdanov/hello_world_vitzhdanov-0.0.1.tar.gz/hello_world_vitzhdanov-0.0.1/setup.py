import setuptools

# Открытие README.md и присвоение его long_description.
with open("README.md", "r") as fh:
	long_description = fh.read()

# Определение requests как requirements для того, чтобы этот пакет работал. Зависимости проекта.
# requirements = ["requests<=2.21.0"]

# Функция, которая принимает несколько аргументов. Она присваивает эти значения пакету.
setuptools.setup(
	name="hello_world_vitzhdanov",
	version="0.0.1",
	author="Eric Chi",
	author_email="i@zhdanov-1.ru",
	description="A Hello World package",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/ericjaychi/sample-pypi-package",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)