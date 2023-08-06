'''
博客文章
'''
import pkgutil
import json
class article:
    '''
    文章类
    '''
    def __init__(self, path, title, type='txt', tags = None, timestamp = None):
        self.path = path
        data = pkgutil.get_data(__package__, path)
        self.text = data.decode()
        self.title = title
        self.type = type
        self.tags = tags
        self.timestamp = timestamp
    
    def get_title(self):
        return self.title
    
    def get_text(self):
        return self.text
    
    def get_tags(self):
        return self.tags
    
    def get_time(self):
        return self.timestamp

    def raw_output(self):
        print(self.title)
        print(f'关键词:{self.get_tags()}')
        print(f'时间:{self.get_time()}')
        print('==============================================')
        print(self.text)

class blog:
    '''
    博客类
    '''
    def __init__(self, path):

        # try finding metadata
        meta = pkgutil.get_data(__package__, path+'\\metadata.json')
        f = meta.decode()
        metadata = json.loads(f)
        
        if metadata:
            blogs=[]
            for item in metadata:
                currpath = item['path']
                currtitle = item['title']
                if item['type']:
                    currtype = item['type']
                else:
                    currtype = 'txt'
                if item['tags']:
                    currtags = item['tags']
                else:
                    currtags = None
                if item['timestamp']:
                    currtimestamp = item['timestamp']
                currblog = article(currpath,currtitle,currtype,currtags,currtimestamp)
                blogs.append(currblog)
            self.blogs = blogs                              
        else:
            print('No metadata!')
    
    def list_articles(self):
        return self.blogs
    
    def return_titles(self):
        return [item.title for item in self.blogs]