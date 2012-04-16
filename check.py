import MySQLdb
import re

conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'wangfengwei',db = 'ows_index')

def checkImgAlt():
    global conn
    print 'checkImgAlt start'
    checkImgResult = open('checkImgOut.txt','w')
    img = '(<img\s*src=.*/>)'
    sql = 'select page,cache from pages where host_id = 1 limit 0, 100'
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        matches = re.findall(img,row[1])
        for m in matches:
            if not 'alt=' in m:
                checkImgResult.write("[ERROR]IMG:%s\tURL:%s\n" %(m,row[0]))
    checkImgResult.close()
    print 'checkImgAlt over'

def extractFormURL():
    global conn
    FormURLResult = open('FormURLResult.txt','w')
    formPattern = '<form'
    sql = 'select page,cache from pages where host_id=1'
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        if re.search(formPattern,row[1]):
            FormURLResult.write("%s\n" %(row[0]))
    FormURLResult.close()

def extractGif():
    global conn
    GifResult = open('GifURL.txt','w')
    GifPattern = '\"([^\"]+\.gif)\"'
    sql = 'select page,cache from pages where host_id=1 limit 0, 100'
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    GifDic = set()
    for row in rows:
        matches = re.findall(GifPattern,row[1])
        for m in matches:
            GifDic.add(m)
    for gif in GifDic:
        GifResult.write("http://www.cdpsn.org.cn%s/%s\n" % (row[0],gif))
    GifResult.close()
    GifHtml = open('gifs.html','w')
    GifHtml.write('<html xmlns="http://www.w3.org/1999/xhtml"><body>')
    for gif in GifDic:
        if 'http://' in gif:
            GifHtml.write('<img src="%s" />' % (gif))
        else:
            GifHtml.write('<img src="http://www.cdpsn.org.cn/%s" />' % (gif))
    GifHtml.write('</body></html>')
    GifHtml.close()
    
if __name__ == '__main__':
    checkImgAlt()
    #extractFormURL()
    #extractGif()
