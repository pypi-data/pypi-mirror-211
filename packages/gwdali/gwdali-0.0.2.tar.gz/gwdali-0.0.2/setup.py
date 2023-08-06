from setuptools import setup

with open("README.md",'r') as arq:
	readme = arq.read()

setup(
	name = 'gwdali',
	version = '0.0.2',
	license = 'MIT License',
	author  = 'Josiel Mendonça Soares de Souza',
	long_description = readme,
	long_description_content_type = "text/markdown",
	author_email = 'jmsdsouza.phd@gmail.com',
	keywords = 'fisher matrix, gravitational waves, gw, dali',
	description = 'A Fisher-Based Software for Parameter Estimation from Gravitational Waves',
	packages = ['GWDALI'],
	install_requeries = ['numpy','matplotlib','scipy','bilby','astropy','itertools'],
	#url = "https://github.com/jmsdsouzaPhD/gwdali/",
)
