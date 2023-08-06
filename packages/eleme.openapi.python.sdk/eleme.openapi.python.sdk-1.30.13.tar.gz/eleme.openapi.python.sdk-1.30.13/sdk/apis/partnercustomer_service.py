# -*- coding: utf-8 -*-


# 抖音商品信息补全服务
class PartnercustomerService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def query_commodity_info_by_location(self, request):
        """
        POI&LIVE&SQUARE&LIST配送信息和跳转链接实时补全（接入方必须做数据安全防控）
        :param request:查询条件
        """
        return self.__client.call("eleme.partnerCustomer.queryCommodityInfoByLocation", {"request": request})

