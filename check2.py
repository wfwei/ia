import MySQLdb
import re

conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'wangfengwei',db = 'ows_index')

def checkImgAlt():
    global conn
    print 'checkImgAlt start'
    checkImgResult = open('imgWithoutAlt.html','w')
    sql = '''SELECT  imagehost.hostname as img_host, img.image as img_src, pagehost.hostname as page_host, img.src_page as page_src
        from ows_index.images as img, ows_hosts.hostlist as imagehost, ows_hosts.hostlist as pagehost 
        where img.alt_text = "" and img.image_host_id = imagehost.id and img.src_host_id = pagehost.id'''
    cursor = conn.cursor()
    start = 0 
    perFetch = 10000
    while True:
        cursor.execute(sql+' limit '+ str(start) + ', ' + str(perFetch) )
        rows = cursor.fetchall()
        for row in rows:
            if myfilter(row[3], '/links/'):
                continue
            checkImgResult.write('<a href="http://%s%s"><img style="border:1px dashed white; padding:2px; width:60px; height:60px;" src="http://%s%s" /></a><br/>\n' %(row[2], row[3], row[0], row[1]));
        if len(rows) == 10000:
            start += perFetch
            print str(start) + ' items extracted \n'
        else:
            break
    checkImgResult.close()
    print 'checkImgAlt over'
   
def extractGif():
    global conn
    print 'extract gif start'
    gifResult = open('GifURL.html','w')
    sql = '''SELECT  imagehost.hostname as img_host, img.image as img_src, pagehost.hostname as page_host, img.src_page as page_src
        from ows_index.images as img, ows_hosts.hostlist as imagehost, ows_hosts.hostlist as pagehost 
        where img.image LIKE '%.gif' and img.image_host_id = imagehost.id and img.src_host_id = pagehost.id'''
    cursor = conn.cursor()
    start = 0 
    perFetch = 10000
    while True:
        cursor.execute(sql+' limit '+ str(start) + ', ' + str(perFetch) )
        rows = cursor.fetchall()
        for row in rows:
            if myfilter(row[3], '/links/'):
                continue
            gifResult.write('<a href="http://%s%s"><img style="border:1px dashed white; padding:2px; width:60px; height:60px;" src="http://%s%s" /></a>' %(row[2], row[3], row[0], row[1]))
        if len(rows) == 10000:
            start += perFetch
            print str(start) + ' items extracted \n'
        else:
            break
    gifResult.close()
    print 'extract gif over'
     

def extractFormURL():
    global conn
    print 'extract form urls start'
    FormURLResult = open('PageWithForm.html','w')
    formPattern = '<form'
    sql = 'select page,cache from pages'
    cursor = conn.cursor()
    start = 0 
    perFetch = 10000
    while True:
        cursor.execute(sql+' limit '+ str(start) + ', ' + str(perFetch) )
        rows = cursor.fetchall()
        for row in rows:
            if myfilter(row[0], '/links/'):
                continue
            if re.search(formPattern,row[1]):
                FormURLResult.write('<a href="http://www.cdpsn.org.cn%s">http://www.cdpsn.org.cn%s </a><br/>\n' %(row[0], row[0]))
        if len(rows) == 10000:
            start += perFetch
            print str(start) + ' items extracted \n'
        else:
            break
    FormURLResult.close()
    print 'extract form urls over'

def extractVideoURL():
    global conn
    print 'extract video urls start'
    VideoURLResult = open('PageWithVideo.html','w')
    videoPattern = '/[^\\.]+\\.swf|/[^\.]+\.wmv|/[^\.]+\.avi'
    sql = 'select page,cache from pages'
    cursor = conn.cursor()
    start = 0 
    perFetch = 10000
    while True:
        cursor.execute(sql+' limit '+ str(start) + ', ' + str(perFetch) )
        rows = cursor.fetchall()
        for row in rows:
            if myfilter(row[0], '/links/'):
                continue
            if re.search(videoPattern,row[1]):
                VideoURLResult.write('<a href="http://www.cdpsn.org.cn%s">http://www.cdpsn.org.cn%s </a><br/>\n' %(row[0], row[0]))
        if len(rows) == 10000:
            start += perFetch
            print str(start) + ' items extracted \n'
        else:
            break
    VideoURLResult.close()
    print 'extract video urls over'

def myfilter(url, ptn):
    if ptn in url:
        return True
    return False
        

if __name__ == '__main__':
    checkImgAlt()
    extractGif()
    extractFormURL()
    extractVideoURL()