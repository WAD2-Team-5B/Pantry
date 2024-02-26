# Pantry

## Description

WAD2 Team 5B project ***Pantry*** repo.

***Pantry*** is a social media site based around food recipes to allow users to share their food ideas and explore others.

## Team

- [Andrew Holligan](https://github.com/andrew-holligan)
- [Nicole Sung](https://github.com/uofg-neec)
- [Jeval Halton](https://github.com/xygn99b)
- [Andrew McGill](https://github.com/andrewmcgill)
- [Andrew Shaw](https://github.com/shawshank316)
- [Layla Clark](https://github.com/layla-e-c)

## Contributing

Git commit messages for this repo must follow the conventions outlined [here](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)

## Config

- *created 'Pantry' workspace dir*
- cd Pantry
- conda create -n pantry python=3.9
- conda activate pantry
- pip install django==2.2.28
- pip install pillow
- *created 'Pantry' repo on Git*
- echo "# Pantry" >> README.md
- git init
- git add *
- git commit -m "first commit"
- git branch -M main
- git remote add origin https://github.com/WAD2-Team-5B/Pantry.git
- git push -u origin main
- mkdir pantry_project
- cd pantry_project
- django-admin startproject pantry_project .
- git add *
- git commit -m "init django"
- git push
