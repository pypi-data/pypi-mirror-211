# -*- coding: utf-8 -*-


# 开放服务
class PartnercomplainService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def create_ticket(self, create_ticket_dto):
        """
        创建woos工单
        :param createTicketDto:查询条件
        """
        return self.__client.call("eleme.partnerComplain.createTicket", {"createTicketDto": create_ticket_dto})

    def upload_ticket_file(self, upload_ticket_file_dto):
        """
        上传工单附件
        :param uploadTicketFileDto:查询条件
        """
        return self.__client.call("eleme.partnerComplain.uploadTicketFile", {"uploadTicketFileDto": upload_ticket_file_dto})

    def get_ticket_info(self, ticket_query_dto):
        """
        查询工单信息
        :param ticketQueryDto:查询条件
        """
        return self.__client.call("eleme.partnerComplain.getTicketInfo", {"ticketQueryDto": ticket_query_dto})

    def urge_ticket(self, urge_ticket_dto):
        """
        催促工单
        :param urgeTicketDto:查询条件
        """
        return self.__client.call("eleme.partnerComplain.urgeTicket", {"urgeTicketDto": urge_ticket_dto})

