---
layout: default
parent: development
title: Python 개발환경, Pyenv, Anaconda3
tags: [python]
---

Mac 에서 Homebrew 통해서 Python 가상화 환경을 구성하려고 합니다. 
우선 Mac 버전이 모하비라면 [모하비 brew error](https://nesoy.github.io/articles/2018-10/Mac-Mojave-brew-error) 글을 한번 읽어보세요. 

Python 가상환경 구성방법은 여러가지가 있지만, pyenv/virtualenv 를 사용할거예요. 
대략적인 과정은 pyenv 설치, anaconda3 설치, 가상환경 구성의 순서예요. pyenv 는 가상화 관리를 위해서 pyenv-virtual 패키지를 사용하는데, anaconda3 정도만 사요할 예정이면 설치 하지 않아요 되요.


## pyenv

```shell

brew help

brew install pyenv

pyenv -v
    pyenv 1.2.13

pyenv install -list | grep anaconda
    ...

pyenv install anaconda3-2019.03
    coffee time...

pyenv versions
    * system....
    anaconda3-2019.03

pyenv activate anaconda3-2019.03
pyenv deactivate 


# zshell ~/.zshrc 
# bash ~/.bashrc
eval "$(pyenv init -)"
source ~/.zshrc

```

> zshell 만 그런진 모르겠지만, PATH 설정은 안해줘도 pyenv 명령어 사용이 가능했어요. 
> anaconda3 설치후 conda 명령어는 사용이 불가능 했어요. activate 로 가상환경 들어갔다나오니 사용 가능해지더라고요.


## default Python 
만약 특정 버전만 사용 하고, 가상화 activate 가 귀찮다면, default python(2.7) 을 변경 시킬 수 있어요.

```shell

pyenv global anaconda3-2019.03
python -V
python versions

```

## pyenv-virtualenv

```shell

brew install pyenv-virtualenv

pyenv virtualenv <인터프리터명> <가상화명>
pyenv versions
pyenv virtualenvs

pyenv activate <가상화명>
pyenv deactivate

# anaconda3
pyenv virtualenv anaconda3-2019.03 conda3
conda activate conda3
which python
conda deactivate

# zshell ~/.zshrc 
# bash ~/.bashrc
eval "$(pyenv virtualenv-init -)"
source ~/.zshrc

```

> anaconda3 를 사용할경우 `pyenv activate conda3` 이렇게 사용이 안되요. 

## uninstall 

```

pyenv uninstall anaconda3-2019.03
pyenv uninstall conda3

```

[pyenv 가상환경 구성 방법](http://egloos.zum.com/mcchae/v/11271948), 그 외의 방법들까지 상세 하게 정리 해놓으신 블로그 입니다. 
