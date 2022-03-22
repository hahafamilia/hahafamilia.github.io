---
layout: default
nav_exclude: true
parent: howto
title : 휴고 설치 및 설정, Learn 테마, Hugo Website
tags: 
    - 2019
    - hugo-staticgen
---

Jekyll 을 사용하다 이번에 Hugo 로 블로그를 이전하게 되었어요. 
Jekyll 과 Hugo 를 비교하는 글들이 많은데, 제 이유는 Category 관리가 Hugo 가 좀 더 직관적이여서 예요.

[Hugo](https://gohugo.io/) 를 설치하고 [Learn Theme](https://learn.netlify.com/en/) 를 
적용하는 방법을 살펴볼게요. 
또 Disqus 댓글, 검색어 노출을 위해 Google Analystics, Google Search, 네이버 웹마스터와 연동하는 방법, 
초안(Draft) 작성을 위한 설정 등을 살펴 볼게요.

### Environment & Requirement
* Hugo Static Site Generator v0.57.2
* Mac
* Git

## Quick Start
### Install
Mac 에서 [Hugo Install Doc](https://gohugo.io/getting-started/quick-start/) 
따라서 설치는 쉽게 진행 가능해요.

> Mac이 아닐경우 [Hugo Install](https://gohugo.io/getting-started/installing/)

```shell
brew install hugo
hugo version
```

Directory Structure
```md
.
├── archetypes
├── config.toml
├── content
├── data
├── layouts
├── static
└── themes
```
몇 개만 살펴보면 `content` 작성한 글, `layouts` Custom html 파일, `static` 는 css, image 등이 저장되요.

### 웹사이트 생성
```shell
# Site 생성
hugo new site <site directory>
# Website server 실행
cd <site directory>
hugo server -D 
```
> Hugo의 CLI 명령어는 웹사이트의 Root `<site directory>` 에서 수행해 주세요.
어떠한 명령어들은 Root 디렉토리가 아닐경우 정상 동작하지 않아요.

### 설정, config.toml
```toml
baseURL = "https://hahafamilia.github.io/"
languageCode = "ko-kr"
title = "haha family's happy blog"
theme = "learn"
```

### 글 작성
컨텐츠 추가 
```shell
hugo new content/posts/my-first-post.md
```
> `hugo new` 명령어로 생성되는 파일은 `archetypes/default.md` 파일에 템플릿화 되어 있어요. 

글은 최상단에 [Front Matter](https://gohugo.io/content-management/front-matter/#readout) 를
추가하고 Markdown 으로 써 내려 가요.

## Theme, hugo-theme-learn 
[Hugo Theme](https://themes.gohugo.io/) 다양한 테마가 존재하네요. Jekyll 에 비해 조금 부족한 듯 보이긴 해요.

[Github Hugo Theme Stars](https://github.com/search?o=desc&q=hugo+theme&s=stars&type=Repositories)
`hugo-academic` 테마가 압도적으로 많이 사용되고 있네요. 
전 `hugo-theme-learn` 테마를 사용하도록 하겠습니다. 
아무래도 개발 관련 포스트 들이 주이기에 조금 올드한 트리구조의 메뉴가 편할 것 같거든요.

Git [submodule](https://git-scm.com/book/ko/v1/Git-%EB%8F%84%EA%B5%AC-%EC%84%9C%EB%B8%8C%EB%AA%A8%EB%93%88)
로 등록하는 것을 추천합니다. 테마는 언제든지 바뀔 수 있고, 업데이트 될 수 있으니까요.

테마추가
```shell
cd <site directory>
git init
git submodule add https://github.com/matcornic/hugo-theme-learn.git themes/learn

# themes/ 디렉토리 이하 테마 디렉토리 명
echo 'theme = "learn"' >> config.toml
```
> 이후 부터는 hugo-theme-learn 에서 재공하는 `shortcode` 나 설정들에 따라 테마 종속적인 것들이 있어요.
그리 많지는 않으니 다른 테마를 사용해도 많이 달라지지는 않아요.

### 메뉴
[hugo-heme-learn](https://learn.netlify.com/en/)
테마는 `content` 디렉토리 이하의 디렉토리, `.md` 파일을 자동으로 좌측 메뉴에 트리 구조로 표시해줘요.

`content` 디렉토리 포함하여, 하나의 디렉토리 마다 `_index.md` 파일을 작성해 주세요.
디렉토리 이하의 `_index.md` 메뉴에서 디렉토리 클릭시 표시되는 페이지 예요.

디렉토리 index 페이지에서 이하의 포스트들을 나열하고 싶으면 
`children` [shortcode](https://learn.netlify.com/en/shortcodes/children/)
를 사용해 보세요.

[Front Matter](https://learn.netlify.com/en/cont/pages/#front-matter-configuration)
필드를 사용해 보세요.

메뉴에 별도의 Link 를 연결하길 원할 경우(Git 주소등) `config.toml` 파일에 `menu.shortcuts` 을 사용하면되요.
```toml
# config.toml
[[menu.shortcuts]]
name = "<i class='fas fa-tags'></i> Tags"
url = "/tags"
```

### favicon
`static/images/favicon.png` 파일명으로 저장

### logo
`layouts/partials/logo.html` 편집
```html
<a id="logo" href="{{ .Site.BaseURL }}">
<img src="/images/logo.png" alt="logo.png">
</a>
```
### Menu Footer
`layouts/partials/menu-footer.html` 편집

> `themes/layouts/partials` 디렉토리를 보시면 이 외에도 설정 가능한 html 들이 있어요.
`themes` 디렉토리에서 설정하지 마시고, website 루트 디렉토리에서 설정해야 관리가 편해요.

### Font
Hugo 에서 font-familiy 를 변경할 수 있는 설정은 없어요. 엄밀히 말하면 있긴 해요.
각 테마에서 Style 편집을 해주는 게 손쉬운 방법 이에요.
[hugo-theme-learn Custom Style](https://learn.netlify.com/en/basics/style-customization/#yours-variant)
문서에 Custom Style 설정 방법이 나와있어요.

`static/css/theme-custom.css` 파일을 생성하고 기본 Style 값을 복사 해주세요.

```toml
[params]
themeVariant = "custom"
```
> 파일명의 `theme-` 는 고정이고, `custom` 은 변수명 처럼 사용가능해요.

font-family 변경은 더 좋은 방법이 있을 것으로 보이지만, 우선 포스트 영역만 변경 했어요.
```style

@import url('https://fonts.googleapis.com/css?family=Inconsolata:400,700&display=swap');
body {
  font-family: 'Inconsolata', monospace;
}
code {
  font-family: 'Inconsolata', monospace;
}
```

> 더 상세히 Style 조정을 하려면, `themes/learn//static/css/` 디렉토리를 확인해 보세요.

font-size 는 테마에서 `rem` 단위를 사용하기 때문에 `html` 요소의 font-size 변경해주세요.
```
html {
  font-size: 14px;
}
```

## 추가기능
Hugo Website 가  hugo-theme-learn 테마를 사용해서 조금 깔끔해 졌네요. 
이제 블로그 운영을 위해 필수적으로 필요한 추가 기능들을 적용해 봐요.
Disqus, Google Analystics, Google Search, 네이버 웹마스터 의 계정이 필요하고 
각 사이트 설정 방법에 대해서는 생략할게요. 
연동에 필요한 것들을 구성하는 방법 이예요.

### Google Analystics
```toml
# config.toml
googleAnalytics = "<your tracking id>"
```

`layouts/partials/custom-header.thml` Google Analystics `Internal Template` 삽입
```
{{ template "_internal/google_analytics.html" . }}
```

### Disqus 댓글
```toml
# config.toml
disqusShortname = "<disqus shortname>"
```

[Hugo Disqus Docs](https://gohugo.io/templates/internal#conditional-loading-of-disqus-comments)
에 Disqus 댓글을 조건에 따라 설정하는 방법이 나와있어요.
`layouts/partials/disqus.html` 에 문서에서 제공하는 스크립트를 추가해주세요.
예를 들어 _index.md 파일에서는 Disqus 댓글을 안보이게 할 수도 있겠어요.
```js
var logicalName = '{{ .File.LogicalName }}';
if (logicalName == "_index.md")
    return;
```

### 검색노출
정적 HTML 생성기로 만들어진 블로그는 검색 사이트에 노출되지 않기에 노출될 수 있도록 설정해줘야 되요.
Google Search, 네이버 웹마스터 등록에 필요한 것은 robots, sitemap, rss feed 링크에요.

다른 설정을 하기 전에 우선 config.toml 에 outputs 설정을 해줘야 해요.
```toml
# config.toml
[outputs]
home = ["HTML", "RSS", "JSON"]
```

어서오세요. 로봇님. robots.txt
```toml
# config.toml
enableRobotsTXT = true
```
[http://localhost:1313/robots.txt](http://localhost:1313/robots.txt)

sitemap.xml
```toml
# config.toml
[sitemap]
changefreq = "weekly"
filename = "sitemap.xml"
```
[http://localhost:1313/sitemap.xml](http://localhost:1313/sitemap.xml)

RSS Template
[여기](https://gohugo.io/templates/rss/) 를 보면
Hugo 에서 자동으로 RSS 파일을 생성하는데 다양하게 있어요.
모든 컨텐츠를 포함할 수 있도록 최상단의 RSS 를 사용해요.

[http://localhost:1313/index.xml](http://localhost:1313/index.xml)

## Github 호스팅
### Github Repository
우선 Github 에 2개의 저장소를 만들어야 합니다. 
Hugo 프로젝트 소스를 저장할 저장소를 생성하고 Hugo 프로젝트 소스를 업로드 해서 유실에 대비하세요.
GitHub Pages 호스팅 방법은 
[Github Pages](https://pages.github.com/) 와
[Hugo on Github Doc](https://gohugo.io/hosting-and-deployment/hosting-on-github/) 에 
잘 설명되어 있어요.

[Hugo on Github Doc](https://gohugo.io/hosting-and-deployment/hosting-on-github/) 
문서를 요약하면

1.  Hugo Project 리포지토리 생성

1. `Git Username` 리포지토리 생성

1. 새로운 디렉토리에 `git clone` 하라고 하는데 지금까지 작업한 디렉토리에 연동해도 되요.

```
cd <site directory>
git init
git remote add origin <Hugo Project Repository>
git add .
git commit -m 'first commit'
git push -u origin master
```
1. `public` 디렉토리가 있다면 삭제해주세요.

    > 루트에서 `hugo` 명령어를 수행하면 `public` 디렉토리가 생성되고 정적파일들이 생성되요.

1.  submodule 로 `public` 디렉토리를 Github Repository 에 등록
```shell
git submodule add -b master <Username Repository> public
```

### 배포 
[deploy.sh](https://gohugo.io/hosting-and-deployment/hosting-on-github/#put-it-into-a-script)
쉘을 작성해주세요.
`depoly.sh` 를 실행하면 정적파일을 생성하고 Repository 로 commit 합니다. 
`https://<git username>.github.io` 주소가 블로그 주소가 됩니다. 

> 포스트를 삭제하거나 카테고리 디렉토리를 삭제해도 `hugo` 명령어를 통해 정적 파일을 생성할때, 
`public` 디렉토리에서 삭제되지 않아요. 이럴때  `public` 디렉토리를 삭제후 정적 파일을 재생성 해야 하는데요. 
이때 `public` 디렉토리의 `.git` 파일이 삭제 되지 않도록 하세요.


## 팁, 게시글 초안
Jekyll 에서는 `_drafts` 디렉토리를 사용해서 작성중인 포스트를 관리 했었는데, 
Hugo 에서는 `Front Matter` 의 `draft: true` 값으로 관리 되요.

전 Jekyll 의 방식이 더 좋아서 Jekyll 처럼 구성해 봤어요.
간단히 설명드리면 2개의 환경을 구성해서 초안작성 환경에서 
초안작성용 Config 파일이 초안이 있는 Content 디렉토리를 바라보게 해서
Hugo Server 실행할 때 초안 환경을 지정해 주는 방식이에요 

[Hugo Configuration Directory Doc](https://gohugo.io/getting-started/configuration/#configuration-directory) 에
Config 관리 방식이 나와있어요.

1. `draft/content` 초안 작성 디렉토리를 생성해주세요. `_index.md` 파일도 생성하고 `children` shortcode 로 작성글도 리스트업 해주세요.

1. 지금까지의 설정이 저장된 `config.toml`파일을 `config/_default/config.toml` 로 옮겨주세요.

1. `config/draft/config.toml` 빈 파일을 생성하고 `contentDir` 디렉토리를 초안작업 디렉토리로 설정하세요.
```toml
contentDir = "draft"
```
1. draft 환경으로 hugo 서버를 시작하세요.
```shell
hugo server -e draft
```

**Draft**
![Draft](/images/howto/2019-09-20-16-00-10.png# mk-threefourths)
**Production**
![Production](/images/howto/2019-09-20-16-00-51.png# mk-threefourths)

## 마치며 
Jekyll 과 Hugo 를 잠깐씩 써본 경험상 성능의 이슈는 제외하고 Hugo 가 셋팅하기에 아주 약간 수월했어요.
Hugo 테마가 좀 적어 아쉽긴 하지만 만족합니다. 
