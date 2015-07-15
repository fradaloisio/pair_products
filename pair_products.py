import urllib
from xml.dom import minidom
import datetime
import time
import sys
import argparse

def main(argv):

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-u','--username', help='DataHub username', required=True)
    parser.add_argument('-p','--password', help='DataHub password', required=True)
    parser.add_argument('-d','--datahub', help='DataHub link', required=True)
    parser.add_argument('-q','--query', help='Query to perform', required=True,type=str)
    args = vars(parser.parse_args())

    username    = args["username"]
    password    = args["password"]
    datahub     = args["datahub"]
    query       = args["query"]

    max_limit   = '10000'   # Max number of products per query
    MAX_DIFF = 10           # Max difference between start sensing time

    url = datahub + "/search?q=" + query + "&rows=" + max_limit
    print url
    if (url.split("://")[0] != "https" and url.split("://")[0] != "http"):
        url = "http://" + url.split("://")[1]

    url = url.split("://")[0] +"://"+ username+":"+password+"@"+url.split("://")[1]

    usock = urllib.urlopen(url)
    xmldoc = minidom.parse(usock)


    itemlist = xmldoc.getElementsByTagName('entry')
    print("found " + str(itemlist.length) + " products")
    print ("possible pairs: ")

    for i in range(0,itemlist.length) :
        prod = "undefined"
        ron = 0
        # find product name
        strs = itemlist[i].getElementsByTagName('str')
        for stri in strs:
            if (stri.attributes['name'].value == "filename"):
                prod = stri.firstChild.data
        ints = itemlist[i].getElementsByTagName('int')
        for inte in ints:
            if (inte.attributes['name'].value == "relativeorbitnumber"):
                ron = inte.firstChild.data

        #find beginposition
        dates = itemlist[i].getElementsByTagName('date')
        for date in dates:
            if (date.attributes['name'].value == "beginposition"):
                beginPosition = datetime.datetime.strptime(date.firstChild.data, "%Y-%m-%dT%H:%M:%S.%fZ")
                next_beginPosition = beginPosition + datetime.timedelta(days=12)

                # find next
                for j in range(i,itemlist.length):
                    nProd = "undefined"
                    nRon = 0
                    nStrs = itemlist[j].getElementsByTagName('str')
                    for nStr in nStrs:
                        if (nStr.attributes['name'].value == "filename"):
                            nProd = nStr.firstChild.data

                    nInts = itemlist[j].getElementsByTagName('int')
                    for nInte in nInts:
                        if (nInte.attributes['name'].value == "relativeorbitnumber"):
                            nRon = nInte.firstChild.data

                    nDates = itemlist[j].getElementsByTagName('date')
                    for nDate in nDates:
                        if (nDate.attributes['name'].value == "beginposition"):
                            nBeginPosition = datetime.datetime.strptime(nDate.firstChild.data, "%Y-%m-%dT%H:%M:%S.%fZ")

                            diff = abs( time.mktime(next_beginPosition.timetuple()) - time.mktime(nBeginPosition.timetuple()))

                            if diff <= MAX_DIFF and nRon == ron:
                                print prod + " " + nProd
    usock.close()

if __name__ == '__main__':
    main(sys.argv[1:])