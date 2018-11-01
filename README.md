# Calibre Search

Search books in calibre. [Download](https://github.com/mpco/AlfredWorkflow-Calibre-Search/releases)

## How to use

- `cali  + keywords` to search books by **Title** and **Tags**.
- `calin + keywords` to search books by **Title**.
- `calit + keywords` to search books by **Tags**.

![screenshot](https://user-images.githubusercontent.com/3690653/47604761-846fb980-da30-11e8-8949-5018c135702d.png)

*The workflow can list multiple formats of the same book in Calibre.*

In the search results:

- The subtext of each result consists of 📙file format, ⭐️rating, and ✍️ authors.
- The subtext will be **Tags** of the book when you press `⌘Command`.
- The subtext will be **ISBN** or **webpage ID** for the book on Amazon, Google Book .etc when you press `⌥Option`.

Besides,

- Press `Enter` to open the book file.
- Press `⌘Command + Enter` to open the folder of the book file.
- Press `⌥Option + Enter` to open the webpage for the book on Amazon, Google Book .etc.

### Configuration

You can set which website to open by setting the value of variable `BookWebsite` after clicking the icon `[x]` in the top right of the workflow.

Candidate for `BookWebsite`: `douban`, `amazon_cn`, `amazon`, `google`, `isbn`.

If `BookWebsite` has no value or a book has no webpage ID of the website of `BookWebsite` value, this workflow will open a webpage in a certain order of priority after pressing `⌥Option + Enter`.

Order: `Douban、Amzon CN、Amazon、Google Book、ISBN`

****

# 中文说明

**功能：** 搜索 Calibre 中的书籍。[下载](https://github.com/mpco/AlfredWorkflow-Calibre-Search/releases)

## 用法

- 输入 `cali  + 关键词` 进行搜索，列出**标题**或**标签（Tags）**符合的书籍。
- 输入 `calin + 关键词` 进行搜索，列出**标题**符合的书籍。
- 输入 `calit + 关键词` 进行搜索，列出**标签（Tags）**符合的书籍。

![screenshot](https://user-images.githubusercontent.com/3690653/47604761-846fb980-da30-11e8-8949-5018c135702d.png)

*如果 Calibre 中某本书含有多个格式的多个文件，该 Workflow 支持将其一一列出，如上图中的最后两本。*

如上图所示，搜索结果中：

- 副文本的组成为： 📙书籍文件格式, ⭐️评分 和 ✍️ 作者。
- 按下 `⌘Command` 键，则显示该书籍关联的标签（Tags）信息。
- 按下 `⌥Option` 键，则显示该书籍关联的 ISBN 编号或豆瓣、亚马逊、谷歌图书等网站上的书籍页面编号。

此外，

- 按下 `回车` 键，直接打开该书籍文件。
- 按下 `⌘Command + 回车`键，打开该书籍文件所在文件夹。
- 按下 `⌥Option + 回车`键，打开该书籍在豆瓣、亚马逊、谷歌图书等网站上的页面。


### 环境变量

打开 Alfred 中该 Workflow 页面的右上角`[x]`图标，填写变量`BookWebsite`的值，可以指定优先打开的书籍网站。

`BookWebsite` 的可选值：`douban`, `amazon_cn`, `amazon`, `google`, `isbn`.

此外，Calibre 中的一本书若有豆瓣、亚马逊、谷歌图书等网站的页面编号以及 ISBN 编号，则在未填写`BookWebsite`或该书籍没有`BookWebsite`指定的网站编号时，会按照一定的优先级顺序打开对应网站书籍页面。

目前的优先级排序：`豆瓣、亚马逊中国、亚马逊、谷歌图书、ISBN`

