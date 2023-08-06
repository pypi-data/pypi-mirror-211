from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
  name = 'auth_package',         
  long_description=long_description,
  long_description_content_type='text/markdown',
  packages = ['auth_package'],
  version = '1.4', 
  license='mit',        
  description = 'Auth package for authentication with microservices',  
  author = 'Ramin Zamanighiri',                  
  author_email = 'zamaniramin549@gmail.com',      
  url = 'https://www.ramzamani.com/',   
  download_url = 'https://github.com/zamaniramin549/auth_project_package/archive/refs/tags/1.4.tar.gz', 
  keywords = ['microservices', 'Auth package', 'API'], 
  install_requires=[    
          'requests',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',     
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)