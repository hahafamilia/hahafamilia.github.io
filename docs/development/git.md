---
layout: default
nav_exclude: true
parent: development
title: "Git"
tags: 
    - 2019
    - git
---

### Git 기본개념

#### 파일상태
* Committed : 커밋상태, `git commit`
* Modified : 수정상태
* Staged : 커밋대기상태, `git add`

#### 사용영역
* Git directory(Local repository) : `git init` 으로 지정, `.git` 디렉토리가 생성
* Working directory : branch 를 checkout 한 내용
* Staging Area

#### 환경설정
* $GIT_HOME/[installed_path]/gitconfig : 시스템의 모든 사용자 설정, `git config --system`
* $USER_HOME : 특정 사용자 설정, `git config --global`
* .git/config : 특정 저장소 설정

#### Getting Started
```
cd /your/project/home
touch readme.md
git init # make git directory
git status
git add readme.md
git status
git commit -m 'commit message'
```

#### Branch
* 목록 : `git branch`, `git branch -a`
* 생성 : `git branch [branch_name]`
* 변경 : `git checkout [branch_name]`

#### Branch merge
`git branch [another_branch]` `another_branch`를 현재 Branch에 병합
같은 파일의 같은 곳 수정되었을 경우 `conflict`가 발생하고, 수정작업이 필요

#### .gitignore
[gitignore.io](https://www.gitignore.io/)

### Remote Repository
#### GitHub
대표적인 `GitHub` 는 추가적인 기능으로 `fork`, `pull request` 제공

* Fork : 다른 사용자 Repository를 내 계정으로 복제
* Pull Request : Fork한 Repository를 수정한 후 원본 Repository 로 병합 요청

#### Remote Repository관리목적의 Git 명령어
* `git clone` : Remote에서 Local로 복사
* `git remote` : Local Repository를 Remote Repository와 연결
* `git push` : Local의 변경내용을 Remote Repository에 저장
* `git fetch` : Remote와 Local이 다를 때 충돌을 해결하고 최신데이터 반영
* `git pull` : Remote의 변경내용을 Local로 가져오면서 merge하는데 conflict 발생시 추적이 어려우므로 Fetch 수행후 Local 파일을 수정하고 Commit/Push 한 후 Pull

```
git remote add origin remote_repository_url
git push -u origin branch_name[master]
git remote -v

git cloen https://github.com/path/pproject.git
```
> clone하게되면 자동으로 master를 origin/master(업스트림 브랜치)의 트래킹브랜치로 생성, 
`-u, --set-upstream`는 트래킹 브랜치 이름을 대체

#### Remote Branck 가져오기
```
## Remote branch list, -a : All Branch remote/local
git branch -r
git checkout -t remote_branch_name
## 다른이름으로 가져올 때
git checkout -b local_branch_name remote_branch_name
```

### Submodule 
#### 삭제
git submodule add https://github.com/chaconinc/DbConnector

```shell
cd <projejct dir>
# delete module on .gitmodules
vi .gitmodules
git rm --cached <module>
git submodule deinit <module>
rm -rf .git/modules/<module>
rm -rf <module>
git commit -m 'delete module'
git push
```

### HowTo
#### Mac Github 비밀번호 재설정
```shell
git config --local --unset credential.helper
```
