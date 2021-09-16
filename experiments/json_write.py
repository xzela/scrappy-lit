import json
import os

LINK_LOG_PATH = './oplog/links.txt'

# {
#     "anal": {
#         "https://url.com/anal/01": {
#             "title": "Some anal title 01",
#             "text": "Lots of text here 01"
#         },
#         "https://url.com/anal/02": {
#             "title": "Some anal title 02",
#             "text": "Lots of text here 02"
#         }
#     },
#     "mature": {
#         "https://url.com/mature/01": {
#             "title": "Some mature title 01",
#             "text": "Lots of text here 01"
#         },
#         "https://url.com/mature/02": {
#             "title": "Some mature title 02",
#             "text": "Lots of text here 02"
#         }
#     }
# }

def open_file(category, link, content):
    with open(LINK_LOG_PATH) as json_file:
        try:
            decode = json.load(json_file)
            json_file.close()
        except ValueError:
            print('OP LOG EMPTY, Using')
            decode = { }
    if category not in decode:
        decode[category] = { }

    if link in decode[category]:
        print('skiping ' + category + ' ' + link)
        return
    else:
        print('processing ' + category + ' ' + link)
        decode[category][link] = { }

    decode[category][link] = content
    with open(LINK_LOG_PATH, 'w') as json_file:
        json.dump(decode, json_file, indent=4)
        json_file.close()

categories = ['butt-stuff', 'anal', 'mature', 'sexy-times', 'toys', 'gay']
links = [ 'http://url.com/',  'http://url.com/']
for category in categories:
    i = 1
    for link in links:
        link += category + '/0' + str(i)
        content = {
            'title': 'My Rad Title ' + category + ' 0' + str(i),
            'text': 'Lost of ' + category + ' text here 0' + str(i)
        }
        open_file(category, link, content)
        i += 1
