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

## File Structure

Pantry
- README.md
- pantry_project
    - media
    - pantry
        - ...
    - pantry_project
        - ...
    - static
        - css
            - base
            - pages
        - images
        - js
            - pages
    - templates
        - pantry
            - base

## Contributing

Git commit messages for this repo must follow the conventions outlined [here](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)

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
