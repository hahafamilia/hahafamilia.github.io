---
layout: default
nav_exclude: true
parent: howto
title: "Jekyll, Github.io, Minimal mistakes 블로그 만들기, 목차 한글링크 버그"
tags: 
    - 2019
    - jekyll 
    - github.io
---

개발자 초창기에는 블로그([이전의 블로그](https://tjstory.tistory.com/)) 활동도 열심히 했었는데... 너무 잊고 살았었네요. 
새롭게 블로그를 시작 할 생각에 Jekyll, Github.io 로 블로그를 구성하게 되었어요.

간단히 Jekyll 은 정적파일 생성기, Github.io 는 호스팅, Minimal mistakes 는 수많은 Jekyll 테마중의 하나예요. 

선택의 기준은 markdown 에디터 때문이에요. 개발자는 에디터 툴을 가장 많이 다루는데요. 
아무래도 markdown 으로 글을 작성하고 Git 으로 Push 하여 포스팅을 하는 구조라면 블로그 활동량이 많아지지 않을까 합니다. 

그럼 Github.io, Jekyll, Minimal mistakes theme 를 이용해 블로그를 만들어 봐요.
쭉~ 진행해본후 복기하여 글을 작성해서 순서가 바뀐부분이 있음을 감안해주세요.

## Git
Git 은 형상관리 솔루션의 발전딘 형태로, 형상관리 외에도 많은 걸 해주고 있어요. 
혹시 글을 읽으시는 분께서 Git을 모르시는... 비 개발자라면 GitHub 사이트에서 파일을 생성/편집을 진행하셔도 되요. 
그렇게 진행하시다 Git에 대해서 알아가셔도 됩니다. 

## Github.io
GitHub 에 새로운 저장소를 생성해요. 저장소의 이름은 `<github username>.github.io` 로 생성하고 저장소의 이름이 도메인이 되요.
맘에 드는 [Jekyll 테마](https://github.com/topics/jekyll-theme) 테마를 선택하시면되요. 저는 `Minimal mistakes` 를 선택했어요.

## theme 설치
Minimal mistakes 의 가이드를 참고하면서 구성했어요.
[minimal-mistakes Quick Start](https://mmistakes.github.io/minimal-mistakes/docs/quick-start-guide/)
두가지 방법이 있어요. 
* 테마를 설치하는 방법 : local 에서 페이지 결과를 확인해 볼 수 있어요.
* 테마를 원격으로 사용하는 방법 : 설치 과정이 없어요.

저 같은 경우는 markdown 이니 preview 는 에디터 에서 가능하고, 초기 셋팅이 끝나면 설정하는 작업이 드물것이라 생각해서 원격 테마를 사용하는 방식으로 구성했어요. 하지만 조금 다른 방법으로 구성해 볼게요.

Quick Start 에는 [Minimal mistakes Github Project](https://github.com/mmistakes/minimal-mistakes/fork) `fork` 하여 `hahafamilia.github.io` 로 이름 변경하라고 되어있어요.

우선 mistakes 저장소를 이름 그대로 포크 합니다. 그림과 같이 Github에 2개의 Repository 가 있게 되요.
![repositories](/assets/images/2019/2019-08-03-00-45-31.png)

Quick Start 불필요한 파일들을 삭제하라고 되어있어요. 삭제 하셔도 되고 안하셔도 됩니다. 
```
remove the unnecessary
.editorconfig
.gitattributes
.github
/docs
/test
CHANGELOG.md
minimal-mistakes-jekyll.gemspec
README.md
screenshot-layouts.png
screenshot.png
```

mmistakes Repository 에서 `_config.yml` 파일을 `.github.io` Repository 로 복사하고 `remote_theme` 항목을 수정해요.

```yml
#_config.yml
remote_theme             : hahafamilia/minimal-mistakes
```
[Hello world! 블로그](https://hahafamilia.github.io) 이렇게 연동 작업이 끝났어요. 
Git `commit`, `push` 하시면 블로그 주소에 접속하시면 기본 화면을 보실 수 있어요.

`_config.yml`  에서 블로그에 관한 몇가지 정보들을 수정해 볼게요. 
```yml
#_config.yml
title                    : "HaHa Familia"
title_separator          : "-"
name                     : "HaHaFam"
description              : "HaHaFam Blog"
url                      : "https://hahafamilia.github.io"  
repository               : "hahafamilia/hahafamilia.github.io"
logo                     : "/assets/images/logo.jpg"

# Site Author
author:
  name             : "HaHaFam"
  avatar           : "/assets/images/author.png" # path of avatar image, e.g. "/assets/images/bio-photo.jpg"
  bio              : "Github.io Blog"
  location         : "Seoul, Korea"
```

## First Post
첫번째 글을 작성해 보도록 해요. `github.io` Repository 에 `_drafts`, `_posts` 두 개의 디렉토리를 생성해주세요.
`_posts` 디렉토리에 `년-월-일-글제목.md` 형식으로 글을 작성하고 Git `commit`, `push` 하시면 블로그에 글이 게시 되요.
`_drafts` 디렉토리는 작성중인 임시 글들을 저장하는 곳이라고 생각하시면 되요.

`_posts` 디렉토리에 `2019-01-25-first-post.md` 라는 파일을 생성해 줍니다. 
글을 작성하는 방법은 `Front Matter` 를 최상단에 작성하고, 이후 Markdown 형식으로 써내려 가면되요.
`Front Matter` 는 일종의 설정값이라고 생각하면되요. 

``` yaml
# Front Matter
---
title: "Jekyll 첫번째 글"
categories: blog
tags: jekyll
# 목차
toc: true  
toc_sticky: true 
---

```
글 내용으로 이미지를 첨부 하고 싶다면 `github.io` Repository `aassets/images` 라는 디렉토리에 보관해주세요.

## _config.yml
`_config.yml` 에 몇가지 설정을 추가해 볼게요. 

검색은 `google` 검색을 비롯해 다양한 연동 설정을 제공하고 있는데요. 우선은 기본만 설정하고 추후에 다루도록 할게요.

`author`, `footer` 의 `links` 설정에 블로그 주인장의 email, twitter, git, facebook 등의 링크들을 설정할 수 있어요.

`defaults` 는 글에 대한 기본 설정값이예요. 동일하게 글의 `Front Matter` 에서 개별적으로 설정이 가능해요.

```yaml
locale                   : "ko-KR"
search                   : true # true, false (default)
# Site Author
author:
  links:
# Site Footer
footer:
  links:
# Defaults
defaults:
  # _posts
  - scope:
      path: ""
      type: posts
    values:
      layout: single
      author_profile: true
      read_time: true
```

## Category, Tags
블로그 활동이 왕성해지만 글들도 많아지게 되고, 글들에 대한 분류 작업이 필요해져요.
그래서 블로그에 카테고리와 테그, 연도 아카이브로 분류하는 설정을 해 줄게요.

우선 `github.io` Repository 에 `_pages` 디렉토리를 생성하고, `category-archive.md`, `year-archive.md`, `tag-archive.md` 파일을 생성해주세요.
각각의 파일에 작성해야할 내용 이예요. 이렇게 되면 작성한 글의 `Front Matter` 설정값을 토대로 분류되요.
```yaml
# category-archive.md
---
title: "Posts by Category"
layout: categories
permalink: /categories/
author_profile: true
---
# year-archive.md
---
title: "Posts by Year"
permalink: /year-archive/
layout: posts
author_profile: true
---
# tag-archive.md
---
title: "Posts by Tag"
permalink: /tags/
layout: tags
author_profile: true
---
```

fork 해온 minimal mistakes Repository 에서 `_data/navigation.yml` 파일을 복사해서 동일한 디렉토리를 생성하고 저장해주세요.
이 설정은 블로그의 상단 메뉴에 관한 설정이예요. 카테고리, 테그, 연도 아카이브 메뉴를 생성해 주세요.
예를 들어 카테고리라면..
```yaml
  - title: "Categories"
    url: /categories/
```

## Stylesheet
minimal mistakes repository 에서 `assets/css/main.scss` 파일을 복사해서 동일한 경로의 디렉토리를 생성하고 저장해주세요.
대부분의 Style 수정은 `main.scss`  에서 이루어져요. 

### Font
`main.scss` 파일을 수정하여 변경할 웹폰트를 import 합니다. 
``` css
@charset "utf-8";

@import "minimal-mistakes/skins/{{ site.minimal_mistakes_skin | default: 'default' }}"; // skin
@import "minimal-mistakes"; // main p

// Font 변경
@import url('https://fonts.googleapis.com/css?family=Inconsolata');
```
전 `Inconsolata` 를 선택했습니다. Inconsolata 프로그래머들이 사용하는 Font 랭크 ( [Best Programming fonts](https://www.slant.co/topics/67/~best-programming-fonts))
순위권 안에 드는 고정폭 폰트 입니다. 

그리고 import 다음 라인으로 폰트 변수에 폰트를 할당해 줍니다.

``` css
$serif              : "Inconsolata", monospace, "PT Serif", Georgia, Times, serif;
$sans-serif-narrow  : "Inconsolata", monospace, "PT Sans Narrow", -apple-system, BlinkMacSystemFont, "Roboto", "Segoe UI", "Helvetica Neue", "Lucida Grande", Arial, sans-serif;

$global-font-family : $serif;
$header-font-family : $sans-serif-narrow;
$caption-font-family: $serif !default;
```
> css 변수에 대한 기본값은 minimal mistakes repository 의 `_sass/minimal-mitakes/_variables.scss` 에서 확인 가능해요.

### Font Size
`main.scss` 파일을 수정하여 폰트의 크기를 조정해요. 이렇게 설정할경우 블로그의 전체 폰트 크기가 일정한 폭으로 변경됩니다.
```css
html {
    font-size: 12px; // originally 16px
    @include breakpoint($medium) {
        font-size: 14px; // originally 18px
    }

    @include breakpoint($large) {
        font-size: 16px; // originally 20px
    }

    @include breakpoint($x-large) {
        font-size: 18px; // originally 22px
    }
}
```

### Title Link Style
포스트의 목록에서 타이틀의 언더라인이 깔끔해 보이지 않네요. `main.scss` 파일을 수정합니다. 

```css
// list title link remove underline
.archive a {
    color: inherit;
    text-decoration: none;
}
```

## 댓글(Disqus), 방문자통계(Google Analystics)
Disqus, Google Analystics 계정이 있다면 설정은 간단하게 이루어 저요. 

Google Analystics 는 트래킹 코드가 필요합니다. 
Disqus 댓글 설정시에는 `shortname` 필요합니다. shortname 은 Disqus 에서 사이트 생성시 할당되는 이름이예요. 
저 같은 경우 `hahafamilia.disqus.com` 의 `hahafamilia` 가 shorname 이 됩니다.

```yaml
# _config.yml
comments:
  provider               : "disqus" # false (default), "disqus", "discourse", "facebook", "google-plus", "staticman", "staticman_v2", "utterances", "custom"
  disqus:
    shortname            : "hahafamilia" # https://help.disqus.com/customer/portal/articles/466208-what-s-a-shortname-
```

```yaml
# _config.yml
analytics:
  provider               : "google" # false (default), "google", "google-universal", "custom"
  google:
    tracking_id          : "UA-145448356-1"
```

> Disqus 는 Git push 하고 반영 되는데 꽤 오랜 시간이 걸리네요.


## 목차(toc), 한글 링크 이동하지 않는 버그 
Front Matter ` toc: true ` 를 설정하게 되면 친절하게 markdown 헤더들로 목차를 만들어 줘요. 그런데 목차를 한글로 입력하니 클릭 해도 링크로 이동하질 않는 버그가 있어요.

해결책 찾는 과정에서 해결해서 프로젝트 기여하신 분이 계시네요. 이전 버전 사용하시는 분은 [Bugfix](https://aliwo.github.io/swblog/minimal-mistake/mmistake-contributor/#) 수정해서 사용하시면 되겠어요.

# 마치며
여기까지 Jekyll, Github.io, Minimal mistakes 를 이용해서 블로그 만드는 방법에 대해 알아 봤습니다. 
블로그 활동량이 많아져 그들이 많아지게 되면, 추가적인 구성들을 더 해볼 생각입니다.
먼저, 글을 꾸준히 올리는 습관을 들여야겠네요.
