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

## Config (Setting Up)

### Directory

- mkdir Pantry
- cd Pantry
- git clone https://github.com/WAD2-Team-5B/Pantry.git
- conda create -n pantry python=3.9
- conda activate pantry
- pip install django==2.2.28
- pip install pillow

### Branching

- git branch -a (logs all branches and tells you what branch you are on)

#### Creating A Branch

- git branch NAME (creates branch called NAME)
- git checkout NAME (switches to branch called NAME)
- git push -u origin NAME (publishes branch called NAME to your remote repo) (basically publishes your branch so everyone can see it! you can now see it on GitHub)

Now you can commit and push as normal on VsCode

#### Merging A Branch

First ensure your ready to merge i.e. you have pulled and pushed on your branch, then

- git checkout main (switching to production branch)
- git pull (IMPORTANT - always pull first when on production branch so you are up to date)
- git merge NAME (sets up a commit to merge branch called NAME)
- git push (push the merge commit and thus carry out the merge)
- git branch -d NAME (delete branch called NAME) (it is safe to delete your branch after it is merged or you can keep it) (DO NOT DELETE main PRODUCTION BRANCH!!!)

## Contributing

Git commit messages for this repo must follow the conventions outlined [here](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)

## File Structure

Pantry
- README.md
- api.md
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
 
