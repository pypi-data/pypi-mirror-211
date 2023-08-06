from .blog import blog
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

myblog = blog('blog')
count = len(myblog.blogs)
def frontpage(item_start=0,item_number=20):
    choices=myblog.return_titles()[item_start:item_start+item_number]
    msg = "==============================================\n"
    msg += "  lixiang90博客首页\n"
    msg += "  ==============================================\n"
    title = inquirer.select(
        message=msg,
        choices=choices+[Choice(value=None, name="Exit")],
        default=None
    ).execute()
    if title:

        if title=="下一页":
            nextpage()
        else:
            for item in myblog.blogs:
                if item.title==title:
                    item.raw_output()
        frontpage()
    else:
        print('==============================================')
        print('结束浏览')
def nextpage():
    pass
if __name__=='__main__':
    frontpage()
