from distutils.core import setup
setup(
  name = 'DRUIDPY',         
  packages = ['DRUIDPY'],  
  version = '0.11',      
  license='MIT',        
  description = 'A package which provides minimum required methods for working with Druid through Python', 
  author = 'NARESH KUMAR B N',                  
  author_email = 'nareshbn007@gmail.com',      
  url = 'https://github.com/Naresh-kumar-B-N/druidpy',   
  download_url = 'https://github.com/Naresh-kumar-B-N/druidpy/archive/pypi-0_11.tar.gz',    
  keywords = ['DRUID', 'DRUID PYTHON', 'DRUID MODULE'],   
  install_requires=[            
          'json',
          'string',
	        'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',	  
  ],
)
