# Pantry

## Description

WAD2 Team 5B project **_Pantry_** repo.

**_Pantry_** is a social media site based around food recipes to allow users to share their food ideas and explore others.

## Team

- [Andrew Holligan](https://github.com/andrew-holligan)
- [Nicole Sung](https://github.com/uofg-neec)
- [Jeval Halton](https://github.com/xygn99b)
- [Andrew McGill](https://github.com/andrewmcgill)
- [Andrew Shaw](https://github.com/shawshank316)
- [Layla Clark](https://github.com/layla-e-c)

## Contributing

Git commit messages for this repo must follow the conventions outlined [here](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)

### Branching

Please create your own branch when working on a feature then submit a pull request.

#### Commands/Usage

- git branch 'BRANCH NAME' (creates branch)
- git checkout 'BRANCH NAME' (moves to the branch)

_Now you can commit and push to this new branch and it won't affect the main production branch_

_When you have finished your feature you can merge your branch with the main production branch_

- git checkout main (switch back to production branch)
- git merge 'BRANCH NAME'
- git branch -d 'BRANCH NAME' (delete the branch once merged)

## Config

- _created 'Pantry' workspace dir_
- cd Pantry
- conda create -n pantry python=3.9
- conda activate pantry
- pip install django==2.2.28
- pip install pillow
- mkdir pantry_project
- cd pantry_project
- django-admin startproject pantry_project .
- python manage.py startapp pantry
- _added 'pantry' to settings.py 'INSTALLED_APPS'_
