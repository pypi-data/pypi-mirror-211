# -*- coding: utf-8 -*-


# 抖音风险同步服务
class PartnerriskService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def sync_risk_result(self, request):
        """
        抖音风险同步
        :param request:同步参数
        """
        return self.__client.call("eleme.partnerRisk.syncRiskResult", {"request": request})

