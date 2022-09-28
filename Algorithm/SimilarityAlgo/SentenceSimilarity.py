import sys

sys.path.append('../..')
from text2vec import Similarity

# Two lists of sentences
# sentences1 = ['如何更换花呗绑定银行卡',
#               'The cat sits outside',
#               'A man is playing guitar',
#               'The new movie is awesome']
#
# sentences2 = ['花呗更改绑定银行卡',
#               'The dog plays in the garden',
#               'A woman watches TV',
#               'The new movie is so great']
def computeSentenceSimilarity( sentences1, sentences2 ):
    sim_model = Similarity()
    final_score = 0.0
    for i in range(len(sentences1)):
        for j in range(len(sentences2)):
            score = sim_model.get_score(sentences1[i], sentences2[j])
            # print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[j], score))


