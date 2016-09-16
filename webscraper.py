#!/usr/bin/python

import urllib2
import urllib
from bs4 import BeautifulSoup
import sqlite3
import re
import time


link_count = 0
error_count = 0
link_list = list()
new_links_list = list()
error_list = list()

run_rank = 0

"""
            SQL will be used later on "
main_database = "links.db"
db_connect = sqlite3.connect(main_database)
db_cursor = db_connect.cursor()
sql_command = CREATE TABLE IF NOT EXISTS URL (LINKS CHAR(512), ID INT(512))
db_cursor.execute(sql_command)
"""


def Extractor(bs_ur):
    global link_list
    global new_links_list
    global link_count

    url = bs_ur
    req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0"})
    try:
        content = urllib2.urlopen(req).read()
    except:
        content = urllib.urlopen(url, None).read()
    soup = BeautifulSoup(content, "lxml")

    for link in soup.find_all('a'):
        new_links_list.append(link.get('href'))
        for lnk in new_links_list:
            try:
                la = len(lnk)
            except:
                la = 0
            if la < 1 or lnk == "#" or lnk == "javascript:void(0);":
                continue
            # Ignoring stuff like hash
            a = re.findall(".cdn-cgi.", lnk)
            if len(a) > 0:
                continue
            # Ignoring cloudfare email protection.
            lnk = Refining(lnk, url)
            if lnk not in link_list:
                link_list.append(lnk)
                link_count += 1
                print str(link_count) + " " + lnk
                # Merging the old list and new list

    del new_links_list[:]
    # Saving Ram by deleting contents of the temporary list

def Refining(u, b_u):
    if u[-1] != "/":
        u = u + "/"
        # ex:: http://efwdwfed.com ==> http://efwdwfed.com/

    if u[:2] == "//":
        if b_u[:5] == "https":
            u = "https:" + u
            # ex:: //tegrfdgrfd.com ==> https://tegrfdgrfd.com , only if base url has https

        if b_u[:5] == "http:":
            u = "http:" + u
            # ex:: //tegrfdgrfd.com ==> http://tegrfdgrfd.com , only if base url has http

    if b_u[-1] == "/":
        b_u = b_u[:-1]
        # Removing / from the base url, to avoid link being incorrectly modified. Ex :: http://rwfdsrfd//rwfedas ==> http://rwfdsrfd/rwfedas

    if u[0] == "/" and u[:2] != "//":
        u = b_u + u
        # Some urls are :: /regfdscrfd/rgfd ==> Therefore the correct url is ==> hxxpx://baseURL/regfdscrfd/rgfd/

    if u[0] == "?":
        u = b_u + "/" + u
        # Adding / to the base url, to avoid link being incorrectly modified. Ex :: http://rwfdsrfdrwfedas ==> http://rwfdsrfd/rwfedas

    if u[:3] != "www" and u[:4] != "http" and u.split('.') > 0 and u[0] != "/":
        u = b_u + "/" + u

    if u[:3] != "www" and u[:4] != "http" and u.split('.') > 0 and u[0] == "/":
        u = b_u + u

    return u


def Link_looper(uuu):
    global link_list
    global run_rank

    while True:
        if run_rank > link_count:
            temp_new_link = raw_input("Please enter another link, as these have very few links")
            link_list.append(temp_new_link)
        Extractor(link_list[run_rank])
        run_rank += 1
        if link_count > 2500:
            break
            # Temporarly kept, for benchmarking
if __name__ == '__main__':
    print "Please enter the link in proper format lile::-"
    print "https://vfedscxrfd.com/"
    a = raw_input("Please enter a starting link:: ")
    start = time.clock()
    link_list.append(a)
    Link_looper(a)

timer = time.clock() - start
print timer
print link_count/timer
