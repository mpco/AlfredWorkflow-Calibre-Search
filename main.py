#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import json
import sqlite3
import subprocess


# SQLite3 aggregate 类
class Concatenate():
    def __init__(self):
        self.itemList = []

    def step(self, value):
        # print 'step(%r)' % value
        self.itemList.append(value)

    def finalize(self):
        # print("final: %r" % ",".join(self.itemList))
        return "!@#$".join(self.itemList)


# SQLite3 aggregate 类
class IdentifiersConcat():
    def __init__(self):
        self.itemList = []

    def step(self, key, val):
        # print 'step(%r)' % value
        # 当val中存在冒号时，id2weblink 中 idJsonStr 会出现 {"aa":"bb":"xx", ...} 的情况而出错
        # 所以使用 #kvSeparator# 作为 key 与 val 的分隔符
        self.itemList.append(u'%s#kvSeparator#%s' % (key, val))

    def finalize(self):
        # print("final: %r" % ",".join(self.itemList))
        return "!@#$".join(self.itemList)


# book's website id to link
def id2weblink(idStrs):
    # idStrs   amazon:0596005954, douban:1850938, isbn:9780596005955
    websiteLinkDict = {"douban": "https://book.douban.com/subject/{}/",
                       "amazon": "https://www.amazon.com/dp/{}",
                       "amazon_cn": "https://www.amazon.cn/dp/{}",
                       "google": "https://books.google.com/books?id={}",
                       "isbn": "https://www.worldcat.org/isbn/{}"}
    websiteOrderedList = ["douban", "amazon_cn", "amazon", "google", "isbn"]
    idJsonStr = '{"' + idStrs.replace('#kvSeparator#', '":"').replace(', ', '", "') + '"}'
    # {"isbn":"xxxx", "amazon":"xxxxx"}
    idJsonObj = json.loads(idJsonStr)
    bookWebsite = os.getenv("BookWebsite")
    # if the env exists and the book has the website id
    if bookWebsite and bookWebsite in idJsonObj:
        return websiteLinkDict[bookWebsite].format(idJsonObj[bookWebsite])
    # 如果没有指定的网站 或者 这本书没有指定网站的id，则按照一定的优先级顺序处理
    for website in websiteOrderedList:
        if website in idJsonObj:
            return websiteLinkDict[website].format(idJsonObj[website])
    # 如果没有以上网站的id，则获取 idJsonObj 中的第一个
    return idJsonObj[idJsonObj.keys()[0]]


def main(querySQL):
    libraryPath = subprocess.check_output(
        '/Applications/calibre.app/Contents/MacOS/calibre-debug -c "from calibre.utils.config import prefs; print(prefs.get(\'library_path\'),end=\'\')"', shell=True)
    metaDbPath = os.path.join(libraryPath, 'metadata.db')
    con = sqlite3.connect(metaDbPath)
    con.create_aggregate("concat", 1, Concatenate)
    con.create_aggregate("identifiers_concat", 2, IdentifiersConcat)
    cur = con.cursor()
    cur.execute(querySQL)
    queryResult = cur.fetchall()

    workflowResult = {"items": []}
    for item in queryResult:
        # bookCalibreID = item[0]
        bookTitle = item[1]
        # if the book has no author, error will occur: "AttributeError: 'NoneType' object has no attribute 'replace'"
        bookAuthors = item[2].replace("!@#$", ", ") if item[2] else ""
        # bookSize = item[3]
        bookTags = item[4].replace("!@#$", ", ") if item[4] else "No Tags"
        bookFormatList = item[5].split("!@#$") if item[5] else ""
        bookFilenameList = item[6].split("!@#$") if item[6] else ""
        bookRating = (str(item[7]) + "  ") if isinstance(item[7], int) else "N/A"
        bookIdentifiers = item[8].replace("!@#$", ", ").replace("#kvSeparator#", ": ") if item[8] else "No data"
        bookWeblink = id2weblink(item[8].replace("!@#$", ", ")) if item[8] else ""
        bookPath = item[9]

        bookFormat = bookFormatList[0] if bookFormatList else "No book file"
        bookFilename = bookFilenameList[0] if bookFormatList else "No book file"
        # 在没有书籍文件时，该值会成为 "/librarypath/author/booktitle/No book file.No book file"
        # 不过可能由于 temp["type"] = "file" 因而 Alfred 会检查文件是否存在 因而 Alfred 不会出错
        bookFullPath = os.path.join(libraryPath, bookPath, bookFilename + "." + bookFormat.lower())
        temp = {}
        temp["type"] = "file"
        temp["title"] = bookTitle
        temp["icon"] = {"path": os.path.join(libraryPath, bookPath, "cover.jpg")}
        temp["subtitle"] = u"📙 {:<7} ⭐️ {:<5}  ✍️ {}".format(bookFormat, bookRating, bookAuthors)
        temp["arg"] = bookFullPath
        temp["mods"] = {
            "alt": {"valid": True, "arg": bookWeblink, "subtitle": bookIdentifiers},
            "cmd": {"valid": True, "arg": bookFullPath, "subtitle": u"🏷 " + bookTags}}
        workflowResult['items'].append(temp)

        # if more than one format
        if len(bookFormatList) > 1:
            for i in range(1, len(bookFormatList)):
                bookFormat = bookFormatList[i]
                bookFilename = bookFilenameList[i]
                temp = {}
                temp["type"] = "file"
                temp["title"] = bookTitle
                temp["icon"] = {"path": os.path.join(
                    libraryPath, bookPath, "cover.jpg")}
                temp["subtitle"] = u"📙 {:<7} ⭐️ {:<5}  ✍️ {}".format(
                    bookFormat, bookRating, bookAuthors)
                temp["arg"] = os.path.join(
                    libraryPath, bookPath, bookFilename + "." + bookFormat.lower())
                temp["mods"] = {
                    "alt": {"valid": True, "arg": bookWeblink, "subtitle": bookIdentifiers},
                    "cmd": {"valid": True, "arg": bookTags, "subtitle": u"🏷 " + bookTags}}
                workflowResult['items'].append(temp)
    print json.dumps(workflowResult, indent=4, sort_keys=True)


if __name__ == '__main__':

    queryScope = sys.argv[1].strip()
    queryStr = sys.argv[2].strip()
    if not queryStr:
        sys.exit()
    if queryScope == "all":
        querySQL = """SELECT id, title,
        (SELECT concat(name) FROM books_authors_link AS bal JOIN authors ON(author = authors.id) WHERE book = books.id) authors,
        (SELECT MAX(uncompressed_size) FROM data WHERE book=books.id) size,
        (SELECT concat(name) FROM tags WHERE tags.id IN (SELECT tag from books_tags_link WHERE book=books.id)) tags,
        (SELECT concat(format) FROM data WHERE data.book=books.id) formats,
        (SELECT concat(name) FROM data WHERE data.book=books.id) filename,
        (SELECT rating FROM ratings WHERE ratings.id IN (SELECT rating from books_ratings_link WHERE book=books.id)) rating,
        (SELECT identifiers_concat(type,val) FROM identifiers WHERE identifiers.book=books.id) ids,
        path
        FROM books
        WHERE title like '%{qs}%' or tags like '%{qs}%'""".format(qs=queryStr)
    elif queryScope == "title":
        querySQL = """SELECT id, title,
        (SELECT concat(name) FROM books_authors_link AS bal JOIN authors ON(author = authors.id) WHERE book = books.id) authors,
        (SELECT MAX(uncompressed_size) FROM data WHERE book=books.id) size,
        (SELECT concat(name) FROM tags WHERE tags.id IN (SELECT tag from books_tags_link WHERE book=books.id)) tags,
        (SELECT concat(format) FROM data WHERE data.book=books.id) formats,
        (SELECT concat(name) FROM data WHERE data.book=books.id) filename,
        (SELECT rating FROM ratings WHERE ratings.id IN (SELECT rating from books_ratings_link WHERE book=books.id)) rating,
        (SELECT identifiers_concat(type,val) FROM identifiers WHERE identifiers.book=books.id) ids,
        path
        FROM books
        WHERE title like '%{qs}%'""".format(qs=queryStr)
    elif queryScope == "tags":
        querySQL = """SELECT id, title,
        (SELECT concat(name) FROM books_authors_link AS bal JOIN authors ON(author = authors.id) WHERE book = books.id) authors,
        (SELECT MAX(uncompressed_size) FROM data WHERE book=books.id) size,
        (SELECT concat(name) FROM tags WHERE tags.id IN (SELECT tag from books_tags_link WHERE book=books.id)) tags,
        (SELECT concat(format) FROM data WHERE data.book=books.id) formats,
        (SELECT concat(name) FROM data WHERE data.book=books.id) filename,
        (SELECT rating FROM ratings WHERE ratings.id IN (SELECT rating from books_ratings_link WHERE book=books.id)) rating,
        (SELECT identifiers_concat(type,val) FROM identifiers WHERE identifiers.book=books.id) ids,
        path
        FROM books
        WHERE title like '%{qs}%' or tags like '%{qs}%'""".format(qs=queryStr)
    main(querySQL)
