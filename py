#!/bin/bash
# py [projectname]

# set up python environment
# virtualenv
# git
# python version
# directory
# atom

# to be added:
# pylint
# pytest
# template

# rharolde@umich.edu 2018/04/11

# dry run apt-get to see if packages are installed
result=`apt-get -s install python-virtualenv | grep "0 upgraded, 0 newly"`
result2=`apt-get -s install git | grep "0 upgraded, 0 newly installed"`
if [ -z "$result" -o -z "$result2" ]; then
  echo "missing some packages, please run:"
  echo "sudo apt-get -s install python-virtualenv"
  echo "sudo apt-get -s install git"
  exit 1
fi

# set up base dir if needed
if [ -d /localshare ]; then
  basedir=/localshare/py
else
  basedir=$HOME/py
fi
mkdir -p $basedir
cd $basedir

# list projects
# and ask for project name if not specified on comand line
if [ "X" = "X$1" ]; then
  ls
  echo "project name: "
  read project
else
  project=$1
fi

# git should be set up with "Python" ignore settings
if [ ! -d $basedir/$project ]; then
  echo "please enter git url: (or just enter if none)"
  read giturl
  if [ ! -z "$giturl" ]; then
    git clone $giturl
  else
    mkdir -p $project
  fi
fi

if [ ! -d $project ]; then
  echo failed to create dir
  exit 1
fi

cd $project

# set up virtualenv if not set up yet
if [ ! -f ./venv/bin/activate ]; then
  echo "version of python: (python2, python3)"
  read pyver
  virtualenv venv -p $pyver
fi
source ./venv/bin/activate

# set up git if not set up yet
if [ ! -d .git ]; then
  git init
  git config user.email "rharolde@umich.edu"
  git config user.name "Bob Harold"
  echo "you will need to connect to git"
fi

# exclude the venv dir from git
# not needed if 'python' ignore is chosen in github
grep -q venv .git/info/exclude || echo "/venv/" >> .git/info/exclude

# show git status
if [ -f .git/config ]; then
  git status
fi

a=`pip show pytest`
if [ -z "$a" ]; then
  pip install pytest
  echo "pytest installed"
fi

a=`pip show pylint`
if [ -z "$a" ]; then
  pip install pylint
  echo "pylint installed"
fi

# check for 'atom' editor package
a=`apt version atom`
if [ -z "$a"]; then
  echo "please download and install 'atom' from https://atom.io/"
fi

# suggest commands
echo "suggested commands:"
echo "  atom ."
echo "  pytest *.py"
echo "  pylint -q"

# open shell for user
bash

# exit virtualenv
deactivate
