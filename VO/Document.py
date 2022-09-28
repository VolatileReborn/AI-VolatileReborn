import re
class Document(object):
    def __init__(self, reportId, reportText):
        self.__reportId = reportId
        self.__reportText = reportText

    @property
    def id(self):
        return self.__reportId


    '''
    词列表， 按空格和逗号分割
    '''
    @property
    def text(self):
        return re.split('[,| ]', self.__reportText )

if __name__ == "__main__":
    doc = Document( 1, "hello world,nice to meet you" )
    print( doc.text )