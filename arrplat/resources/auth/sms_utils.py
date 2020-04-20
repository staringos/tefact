# -*- coding: utf-8 -*-
import json
import uuid
import random

from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from arrplat.config import config

Conf = config.get('message')

acs_client = AcsClient(Conf.get('ACCESS_KEY_ID'), Conf.get('ACCESS_KEY_SECRET'), Conf.get('REGION'))
region_provider.modify_point(Conf.get('PRODUCT_NAME'), Conf.get('REGION'), Conf.get('DOMAIN'))


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    sms_request = SendSmsRequest.SendSmsRequest()
    sms_request.set_TemplateCode(template_code)

    if template_param is not None:
        sms_request.set_TemplateParam(template_param)

    sms_request.set_OutId(business_id)
    sms_request.set_SignName(sign_name)
    sms_request.set_PhoneNumbers(phone_numbers)
    sms_response = acs_client.do_action_with_exception(sms_request)

    return sms_response


def send_phone_code(phone):
    __business_id = uuid.uuid1()
    code = random.randint(100000, 999999)
    params = {'code': code}
    payload = send_sms(__business_id, phone, "锐途云", "SMS_152655055", params)

    payload = json.loads(payload)
    payload = {
        "code": payload["Code"],
        "message": payload["Message"],
        "phone": phone,
        "phone_code": code
    }
    return payload
