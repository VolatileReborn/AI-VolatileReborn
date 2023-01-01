from aip import AipOcr


def get_baidu_ocr_res(img_path):
    img = open(img_path, 'rb').read()
    options = {'language-type': "CNH_ENG"}
    # please replace with your own app_id, api_key, and secret_key
    client = AipOcr('26307650', 'eAQGKGnthnfHOfx6U8hc1pt4', 'RPncQuWAzFu0ZaXzmiWbLSdPMCWpQZej')
    res = client.basicAccurate(img, options)
    if 'words_result' in res:
        txt = [r['words'] for r in res['words_result']]
    else:
        res = client.basicGeneral(img, options)
        if 'words_result' in res:
            txt = [r['words'] for r in res['words_result']]
        else:
            txt = []
    return txt
