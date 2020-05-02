git clone https://github.com/burukuru/Flex
pipenv install pelican
pipenv run pelican -s pelicanconf.py
git commit -a -m 'Update site'

