#사용법 python setup.py install
from cx_Freeze import setup,Executable

#includefiles = [ 'simplepos.db', 'templates\index.html', 'templates\product.html', 'templates\sale.html', 'static\javascripts\jquery-1.11.1.js', 'static\javascripts\jquery.tabletojson.js', 'static\javascripts\common.js', 'static\stylesheets\style.css']
includefiles = [ 'simplepos.db' ]
includes = []
excludes = []

setup(
    name = 'index',
    version = '0.9',
    description = 'Simple Pos App',
    options = {'build_exe': {'excludes':excludes,'include_files':includefiles}}, 
    executables = [Executable('simplepos.py')]
)