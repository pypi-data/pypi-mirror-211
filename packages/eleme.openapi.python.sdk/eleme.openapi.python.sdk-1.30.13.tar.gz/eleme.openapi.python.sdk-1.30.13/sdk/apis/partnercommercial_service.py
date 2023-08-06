# -*- coding: utf-8 -*-


# 抖音服务
class PartnercommercialService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def sync_cooperate_relation_change(self, request):
        """
        服务商/代运营绑定通知
        :param request:查询条件
        """
        return self.__client.call("eleme.partnerCommercial.syncCooperateRelationChange", {"request": request})

