# -*- coding: utf-8 -*-


# 提供给dy的查询服务
 ，
 包括：服务数据，仲裁信息，赔付信息等
class PartnercustomerserviceService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def query_server_info_by_order_id(self, query_server_param):
        """
        服务数据
 ，
 查询订单服务信息
        :param queryServerParam:查询条件
        """
        return self.__client.call("eleme.partnerCustomerService.queryServerInfoByOrderId", {"queryServerParam": query_server_param})

    def query_arbitration_by_order_id(self, query_arbitration_param):
        """
        仲裁
 ，
 查询订单仲裁信息
        :param queryArbitrationParam:查询条件
        """
        return self.__client.call("eleme.partnerCustomerService.queryArbitrationByOrderId", {"queryArbitrationParam": query_arbitration_param})

    def query_compensation_by_order_id(self, query_compensation_param):
        """
        赔付
 ，
 查询订单赔付信息
        :param queryCompensationParam:查询条件
        """
        return self.__client.call("eleme.partnerCustomerService.queryCompensationByOrderId", {"queryCompensationParam": query_compensation_param})

    def query_food_safety_compensation_by_order_id(self, query_compensation_param):
        """
        赔付
 ，
 查询订单食安赔付
        :param queryCompensationParam:查询条件
        """
        return self.__client.call("eleme.partnerCustomerService.queryFoodSafetyCompensationByOrderId", {"queryCompensationParam": query_compensation_param})

    def query_order_single(self, query_order_info_param):
        """
        订单
 ，
 订单相关数据
        :param queryOrderInfoParam:查询条件
        """
        return self.__client.call("eleme.partnerCustomerService.queryOrderSingle", {"queryOrderInfoParam": query_order_info_param})

    def cs_handling_report(self, query_report_param):
        """
        离线数据
 ，
 工单处理情况
        :param queryReportParam:查询条件
        """
        return self.__client.call("eleme.partnerCustomerService.csHandlingReport", {"queryReportParam": query_report_param})

    def cs_service_statistics_report(self, query_report_param):
        """
        离线数据
 ，
 咨询人工服务量
        :param queryReportParam:查询条件
        """
        return self.__client.call("eleme.partnerCustomerService.csServiceStatisticsReport", {"queryReportParam": query_report_param})

