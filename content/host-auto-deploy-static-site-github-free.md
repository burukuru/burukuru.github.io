Title: How to host and auto deploy a static website using Pelican, CircleCI and GitHub Pages for free
Date: 2020-05-04 22:24
Author: Thanh
Category: DevOps
Tags: devops, cicd
Status: draft

In this post I will go through how you can:

- host a simple static website for free using GitHub Pages and Pelican
- auto deploy the site with CircleCI

# Tools
## Pelican
My website, a fairly simple tech blog, is created using a static site generator written in Python called [Pelican](https://github.com/getpelican/pelican/). Pelican supports Markdown, which is one of my favourite ways of writing documentation and hence a natural choice to write tech blog posts in. I have written a few blogs on platforms with WISYWIG editors and they have sometimes felt a bit clunky when formatting code.

**Why Pelican?**

I like the simplicity of having a static site, it's:

- lightweight
- fast
- cacheable

This post assumes you already have a basic site working with Pelican and ready to deploy; if not, head over to [Pelican's quickstart](https://docs.getpelican.com/en/stable/quickstart.html). Also you need a GitHub and CircleCI account.

## GitHub Pages
[GitHub Pages](https://pages.github.com/) allows you to host a static website for free from a GitHub repository under the domain *yourusername*.github.io. As this is a user site, any content you push to the master branch of the repository called *yourusername*.github.io will be available at that domain.

Note that if you are starting from scratch, you could look at using Jekyll which is supported out of the box.

**Custom domain**

GitHub also give you the ability to [link a custom domain](https://help.github.com/en/github/working-with-github-pages/configuring-a-custom-domain-for-your-github-pages-site) and even configure HTTPS. All for free, what's not to like!  

## CircleCI
[CircleCI](https://circleci.com/) is a very popular cloud-based CI product with a free tier for private projects. This gets even more generous for open-source projects: nearly $3000 per year's worth of credits. This is more than enough to deploy a static website.

# Deployment

CircleCI has an excellent blog post on [how to deploy documentation to GitHub Pages with CI](https://circleci.com/blog/deploying-documentation-to-github-pages-with-continuous-integration/). I am going to expand on it with the specific use case of deploying a personal website using Pelican.

## Repository and branches
First you will need to [create a repository](https://pages.github.com/) for your GitHub Pages. As the website is deployed from the master branch of our repository, we will store all Pelican configuration files and source Markdown files in a branch called `pelican`. The two branches are completely separate and do not share a common Git history.

## SSH keys

Using SSH keys, instead of personal access tokens, will let you follow the principle of least privileges and only allow the CI jobs to push to this specific repository. We want to protect any higher value repositories you might have under your administration.

[Generate ssh key](https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent); the command from GitHub docs are usually a great guidance but in this case I had to tweak them as the OpenSSH default format has changed and CircleCI did not seem to support it.
```shell
ssh-keygen -m PEM -t rsa -b 4096 -C "ci-build@example.com"
```
Upload the [private SSH key to CircleCI](https://circleci.com/docs/2.0/add-ssh-key/).  
Then add the public key as a [deploy key with read/write](https://developer.github.com/v3/guides/managing-deploy-keys/#deploy-keys) to your GitHub project.

## Continuous Deployment
In the CircleCI configuration, we need to generate site which is as easy as:

```shell
pipenv run pelican 
```

Then to trigger the site deploy, we'll use a great Python-based tool called [ghp-import](https://github.com/davisp/ghp-import/) to push our changes to the master branch. From there, GitHub automation will publish the site.

ghp-import even has a flag to write a CNAME file which I didn't use as I have already done it in Pelican before I noticed it. You should definitely use it though.

Putting all the above together, your config should look roughly like the code below. Commit it to the `pelican` branch and push it.

```yaml
version: 2.1

orbs:
  python: circleci/python@0.2.1

jobs:
  build-and-push:
    executor: python/default
    steps:
      - add_ssh_keys
      - checkout
      - run: 
          command: |
            # Get the theme
            git clone https://github.com/burukuru/Flex
            # Install dependencies in new pip environment
            pipenv install pelican markdown ghp-import
            # Generate the site
            pipenv run pelican
            # Configure the Git user so the commit messages look neat
            git config user.email "ci-build@thanhpham.cloud"
            git config user.name "ci-build"
            # Push the content of the output directory to the master branch
            pipenv run ghp-import output -m "[skip ci] Update website" -b master -p

workflows:
  main:
    jobs:
      - build-and-push:
        filters:
          branches:
            only:
             - pelican
```

We use `[skip ci]` in the commit message so that new website updates don't trigger a build in CircleCI.  
The GitHub automation to publish the website will still work.

Lastly you need to [set up your new repository with CircleCI](https://circleci.com/blog/setting-up-continuous-integration-with-github/) and in your CircleCI dashboard you should see a new job generating your website and pushing it out.

Now every time you push a change to the `pelican` branch, your website should be automatically updated within minutes. Enjoy your automation and get writing!
