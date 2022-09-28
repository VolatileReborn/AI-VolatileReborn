from flask import request

# 将请求的body（ json格式 ）转换为 list<str>
def request_to_sentences( request ):
    json_data = request.json
    sentences = json_data # todo

    return sentences


