from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

long_description = 'This is a tool to convert a monolith application to an intermediate microservice and deploy it using serverless '

setup(
		name ='monomic',
		version ='1.0.0',
		author ='Team Hash',
		author_email ='180253@tkmce.ac.in',
		url ='',
		description ='Sedai Package',
		long_description = long_description,
		long_description_content_type ="text/markdown",
		license ='MIT',
		packages = find_packages(),
		entry_points ={
			'console_scripts': [
				'monomic = monomic.intermediate:main'
			]
		},
		classifiers =(
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		),
		keywords ='monolith microservice serverless django',
		install_requires = requirements,
		zip_safe = False
)
