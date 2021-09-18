from urllib.parse import urlparse
thingy = { "food": "pizza", "drink": "pepsi"}
empt = {}
print(len(empt))

url = '//www.literotica.com/stories/showstory.php?id=181688'

o = urlparse(url)
newUrl = o.geturl()
if o.scheme  != 'https':
    newUrl = o._replace(scheme='https').geturl()
print(newUrl)
