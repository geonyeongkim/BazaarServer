# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pymongo
from BazaarServer.settings import shop_collection

logger = logging.getLogger("category")

def select_categorynum(category_num,list_num):
    shops = list(shop_collection
        .aggregate(
            [
                {"$match":{"goods.category":category_num}}
                ,{"$project":{"_id":0}}
                ,{"$unwind":"$goods"}
                ,{"$match":{"goods.category":category_num}}
                ,{"$skip":(list_num-1)*10}
                ,{"$limit":10}
            ]
        )
    )
    meta = list(shop_collection
        .aggregate(
        [
            {"$match": {"goods.category": category_num}}
            , {"$project": {"_id": 0}}
            , {"$unwind": "$goods"}
            , {"$match": {"goods.category": category_num}}
            ,{"$group":{"_id":"null","count":{"$sum":1}}}
            ,{"$project":{"_id":0}}
        ]
    )
    )
    print(meta)
    data = {}
    logger.info("mongod db")
    for shop in shops:
        shop["good"] = shop["goods"]
        shop.pop("goods")
    data['items'] = shops
    data['meta'] = meta[0]
    logger.info("change shops")
    return Response(data)

@api_view(['GET'])
def get_category(request,category_num, list_num):
    return select_categorynum(category_num,list_num)

