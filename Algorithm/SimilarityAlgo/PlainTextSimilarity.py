
import abc
from Algorithm.SimilarityAlgo.tfidf import TfIdf
from VO.Document import Document

REPORT_ID = "report_id"
SIMILARITY ="similarity"

'''
    文本相似度算法
'''

class TextSimilarityStrategy(metaclass=abc.ABCMeta):
    def __init__(self):
        return

    @abc.abstractmethod
    def get_top_n_similar_reports(self, N):
        pass


class TF_IDF( TextSimilarityStrategy ):

    def computeTextSimilarity(self, originalDocument, comparedDocument):
        resultList = self.get_top_n_similar_reports(originalDocument, [comparedDocument], 1)
        if len(resultList) == 0:
            return 0

        assert len(resultList) == 1

        similarity = resultList[0].get(SIMILARITY)
        return similarity  if similarity > 0 else 0


    '''
    得到文本上最相似的若干篇报告， 0 <= 报告数 <= N
    '''
    def get_top_n_similar_reports(self,originalDocument, comparedDocuments, N):
        table = TfIdf()
        table.add_document(originalDocument.id, originalDocument.text)


        for document in comparedDocuments:
            table.add_document( document.id, document.text )
        #
        # table.add_document("bar", ["alpha", "bravo", "charlie", "india", "juliet", "kilo"])
        # table.add_document("baz", ["kilo", "lima", "mike", "november"])
        #
        # print( table.similarities(["alpha", "bravo", "charlie"]) )  # => [['foo', 0.6875], ['bar', 0.75], ['baz', 0.0]]

        similarityList = table.similarities(originalDocument.text)
        # similarityList = [ [1,0.63], [2,0.04], [3,0.54], [4,0.98] ]
        self.__sortSimilarityList(similarityList)
        resultList = self.__wrapListToResultFormat( similarityList ,originalDocument.id)[:N] # 返回前N个
        resultList = self.__filtResultList( resultList )
        return resultList

    '''
    similarityList: [[5, 0.75],[3, 0.6875],  [13, 0.0]]
    resultList: [{ "report_id":3, "similarity": 0.6875 }, { "report_id":5, "similarity": 0.75 }, ... ]
    '''
    def __wrapListToResultFormat(self, similarityList, originalDocumentId ):
        resultList = list()
        for item in similarityList:
            if item[0] == originalDocumentId:
                continue
            else:
                resultList.append( { REPORT_ID: item[0], SIMILARITY: item[1]} )
        return resultList

    '''
    对结果对报告列表进行过滤， 目前只是剔除相似度小于等于0对报告
    '''
    def __filtResultList(self, originalList):
        resultList = list()
        for item in originalList:
            if item.get(SIMILARITY) <= 0:
                continue
            else:
                resultList.append(item)
        return resultList



    '''
    similarityList: [[3, 0.6875], [5, 0.75], [13, 0.0]]
    将其按相似度逆序排列
    '''
    def __sortSimilarityList(self, similarityList ):

        similarityList.sort(reverse = True, key = self.__myComparedKeyFunc)
        return


    def __myComparedKeyFunc(self, similarityListItem):
        return similarityListItem[1]


if __name__ == '__main__':
    plainTextSimilarityStrategy = TF_IDF()

    originalDocument = Document(1, "a,b,c,d,e,f,g,h" )
    comparedDocuments = list()

    comparedDocument1 = Document(2, "a,b,c,i,j,k")
    comparedDocument2 = Document(3, "k,l,m,n")
    comparedDocument3 = Document(6, "a,c,i,k,j,l,m")
    comparedDocuments.append(comparedDocument1)
    comparedDocuments.append(comparedDocument2)
    comparedDocuments.append(comparedDocument3)

    resultList = plainTextSimilarityStrategy.get_top_n_similar_reports(originalDocument, comparedDocuments, 2)
    for item in resultList:
        print(item)