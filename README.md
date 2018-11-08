# Bug Analysis Application (BAA)
[![star this repo](http://githubbadges.com/star.svg?user=wangzhe&repo=jira_bug_analysis&style=default)](https://github.com/wangzhe/jira_bug_analysis)
[![fork this repo](http://githubbadges.com/fork.svg?user=wangzhe&repo=jira_bug_analysis&style=default)](https://github.com/wangzhe/jira_bug_analysis/fork)
![python](https://img.shields.io/badge/python-3.6-ff69b4.svg)

## What is BAA

BAA (Bug Analysis Application) is an application of bug analysis against Jira

## How to start BAA

1) Step One
   +    if you are using docker, please use dockfile to setup everything
   +    if you are using linux, go into the application root and run

```bash
pip install -r requirements.txt
```

2) Step Two
    +   get system username 
    +   generate local file in config folder (like zwang.local)
    +   use the format like
```bash
[DEFAULT]
INSTANCE_HOST=
SPACE_NAME=
DEBUG_MODE=

[ACCOUNT]
A_USER=
A_TOKEN=

```
2) Step Three
    + run python
```bash
python main.py
```

