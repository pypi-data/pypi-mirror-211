"""
Name : gm_parse_response_utils.py
Author  : 写上自己的名字
Contact : 邮箱地址
Time    : 2023-05-16 9:33
Desc:  快速解析请求返回text，并获取自己想要的数据。需学习jsonpath插件
"""

import json
from jsonpath import jsonpath

def gm_extract_json(text, jsonpath_expression):
    """使用jsonpath工具类解析请求返回值"""
    try:
        # 判断是否
        if isinstance(text, dict):
            data = jsonpath(text, jsonpath_expression)  # 使用jsonpath进行解析
        elif isinstance(text, str):
            data = jsonpath(text, jsonpath_expression)  # 使用jsonpath进行解析
        elif isinstance(text, list):
            data = jsonpath(text, jsonpath_expression)  # 使用jsonpath进行解析
        else:
            json_text = json.loads(text)  # 如果是非dict、str、list类型，则转换成python对象
            data = jsonpath(json_text, jsonpath_expression)  # 使用jsonpath进行解析
        return data
    except TypeError as e:
        print("入参{}的类型错误，请检查,{}".format(text, e))


if __name__ == '__main__':
    json_data = """
    { "store": {
        "book": [
          { "category": "reference",
            "author": "Nigel Rees",
            "title": "Sayings of the Century",
            "price": 8.95
          },
          { "category": "fiction",
            "author": "Evelyn Waugh",
            "title": "Sword of Honour",
            "price": 12.99
          },
          { "category": "fiction",
            "author": "Herman Melville",
            "title": "Moby Dick",
            "isbn": "0-553-21311-3",
            "price": 8.99
          },
          { "category": "fiction",
            "author": "J. R. R. Tolkien",
            "title": "The Lord of the Rings",
            "isbn": "0-395-19395-8",
            "price": 22.99
          }
        ],
        "bicycle": {
          "color": "red",
          "price": 19.95
        }
      }
    }
    """

    import jsonpath

    json_data = json.loads(json_data)
    store = jsonpath.jsonpath(json_data, '$.store')
    isbn_book = jsonpath.jsonpath(json_data, '$..book[?(@.isbn)]')  # 正则查询book节点下含 isbn 关键字的，并列出对应book子节点数据；
    price_book = jsonpath.jsonpath(json_data, '$..book[?(@.price<10)]')  # 正则查询book节点下 Price<10的，并列出对应book子节点数据；
    category = jsonpath.jsonpath(json_data, '$...isbn')  # 直接查找isbn
    price = jsonpath.jsonpath(json_data, '$.store..price')  # store节点下所有的price值
    three_price = jsonpath.jsonpath(json_data, '$.store.book[0].price')  # store节点第1部书的price值，索引从0开始
    last_book = jsonpath.jsonpath(json_data, '$.store.book[(@.length-1)]')  # 最后一本书

    print(store)
    print(isbn_book)
    print(price_book)
    print(category)
    print(price)
    print(three_price)
    print(last_book)
    print(type(last_book))
    print(jsonpath.jsonpath(json_data, '$..book[-2:]'))  # 最后两本书)

    s = """{"code":20000,"message":"ok","description":"",
    "data":{"todoRationalNum":18,"todoAuditNum":1,"todoEleGuaranteeNum":1,"todoAbolishEleGuaranteeNum":0}}"""
    s = json.loads(s)
    s1 = jsonpath.jsonpath(s, '$.code')
    print(s1[0])
