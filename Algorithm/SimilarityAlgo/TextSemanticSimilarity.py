# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 语义相似文本检索
This is a simple application for sentence embeddings: semantic search

We have a corpus with various sentences. Then, for a given query sentence,
we want to find the most similar sentence in this corpus.

This script outputs for various queries the top 5 most similar sentences in the corpus.
"""
import sys

sys.path.append('../../..')

from text2vec import SentenceModel, cos_sim, semantic_search, BM25
import torch

import abc

mock_result = [ {"report_id": 7, "similarity": 0.922}, {"report_id": 2, "similarity": 0.855}, {"report_id": 9, "similarity": 0.543 } ]

'''
    语义相似度算法
'''
class TextSemanticSimilarityStrategy(metaclass=abc.ABCMeta):

    def __init__(self, queries, corpus):
        self.queries = queries
        self.corpus = corpus

        self.embedder = SentenceModel()
        self.corpus_embeddings = self.embedder.encode(self.corpus)

    # @classmethod
    # def constrct(cls):
    #     pass

    @abc.abstractmethod
    def get_top_n_semantically_similar_reports(self, N):
        pass


class CosineTextSemanticSimilarityStrategy(TextSemanticSimilarityStrategy):

    def get_top_n_semantically_similar_reports(self, N):
        embedder = self.embedder
        corpus = self.corpus
        queries = self.queries

        # embedder = SentenceModel()
        corpus_embeddings = embedder.encode(corpus)
        # Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
        print('\nuse cos sim calc each query and corpus:')
        top_k = min(N, len(corpus))
        for query in queries:
            query_embedding = embedder.encode(query)

            # We use cosine-similarity and torch.topk to find the highest 5 scores
            cos_scores = cos_sim(query_embedding, corpus_embeddings)[0]
            top_results = torch.topk(cos_scores, k=top_k)

            print("\n\n======================\n\n")
            print("Query:", query)
            print("\nTop N most similar sentences in corpus:")

            for score, idx in zip(top_results[0], top_results[1]):
                print(corpus[idx], "(Score: {:.4f})".format(score))

        print('#' * 42)
        return mock_result

class SemanticSearchTextSemanticSimilarityStrategy( TextSemanticSimilarityStrategy ):
    def get_top_n_semantically_similar_reports(self, N):
        ########  use semantic_search to perform cosine similarty + topk
        embedder = self.embedder
        corpus = self.corpus
        queries = self.queries
        corpus_embeddings = self.corpus_embeddings

        print('\nuse semantic_search to perform cosine similarty + topk:')

        for query in queries:
            query_embedding = embedder.encode(query)
            hits = semantic_search(query_embedding, corpus_embeddings, top_k=N)
            print("\n\n======================\n\n")
            print("Query:", query)
            print("\nTop 5 most similar sentences in corpus:")
            hits = hits[0]  # Get the hits for the first query
            for hit in hits:
                print(corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))

        print('#' * 42)
        return mock_result


class BM25TextSemanticSimilarityStrategy(TextSemanticSimilarityStrategy):
    def get_top_n_semantically_similar_reports(self, N):
        corpus = self.corpus
        queries = self.queries

        ######## use bm25 to rank search score
        print('\nuse bm25 to calc each score:')

        search_sim = BM25(corpus=corpus)
        for query in queries:
            print("\n\n======================\n\n")
            print("Query:", query)
            print("\nTop 5 most similar sentences in corpus:")
            for i in search_sim.get_scores(query, top_k=N):
                print(i[0], "(Score: {:.4f})".format(i[1]))

        return mock_result




if __name__ == '__main__':
    queries = ['qwrwqrew']
    corpus = ['wrwqre', 'qrwereqw', 'qrwerwqrew']
    cosineTextSimilarityStrategy = CosineTextSemanticSimilarityStrategy(queries, corpus)
    print(cosineTextSimilarityStrategy.get_top_n_semantically_similar_reports(10))