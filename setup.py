"""
Install stickynote.
"""

def main():
	try:
		from setuptools import setup
	except ImportError:
		from distutils.core import setup

	config = {
		'description': 'Tag objects (tables, columns, others) in a PostgreSQL database.',
		'author': 'Matt Christie',
		'download_url': 'https://github.com/christiemj09/stickynote.git',
		'author_email': 'christiemj09@gmail.com',
		'version': '0.1',
		'install_requires': ['psycopg2-binary', 'sqlalchemy'],
		'packages': ['stickynote'],
		'scripts': [],
		'entry_points': {
		    'console_scripts': [
		        'init_tag_tables=stickynote.init_tag_tables:console_script',
		        'insert_tags=stickynote.insert_tags:console_script',
		    ],
		},
		'name': 'stickynote',
	}

	setup(**config)	

if __name__ == '__main__':
	main()

