import setuptools

long_description = open("README.md", "r").read()

setuptools.setup(
	name = "yuyu",
	version = "0.4.2",
	author = "Akas Wisnu Aji / justakazh",
	description = "Web Information Gathering And Analyst",
	long_description=long_description,
    	long_description_content_type='text/markdown',
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	install_requires=[
          'Wappalyzer',
	  'requests'
      	],

	)
