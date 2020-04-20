"""
@author xiaofei
@date   2020-03-10
@desc
"""

import time

from sqlalchemy import Column, Integer, \
    ForeignKey, BigInteger, VARCHAR, DECIMAL, Text, Float
from arrplat.common.utils import generate_uuid
from extensions import db
from sqlalchemy.dialects.mysql import TINYINT


class Meeting(db.Model):
    __tablename__ = 'meeting'

    notice_type_enum = {
        1: "企业微信",
        # 2: "短信"
    }

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(20), nullable=True, server_default="", comment="会议主题")
    content = Column(VARCHAR(255), nullable=True, server_default="", comment="会议内容")
    start_time = Column(BigInteger, default=time.time, server_default="0", comment="会议开始时间")
    end_time = Column(BigInteger, default=time.time, server_default="0", comment="会议结束时间")
    meeting_room_id = Column(VARCHAR(32), ForeignKey('meeting_room.id', ondelete='CASCADE'), comment='会议室id')
    sponsor_id = Column(VARCHAR(32), ForeignKey('employee.id', ondelete='CASCADE'), comment='发起人')
    notice_type = Column(TINYINT, comment='通知类型', server_default="0")
    employee_count = Column(Integer, comment='会议人数(实时同步修改)', server_default="0")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class MeetingRoom(db.Model):
    __tablename__ = 'meeting_room'

    layout_type_enum = {
        1: "椭圆长桌",
        2: "回字形",
        3: "阶梯式"
    }

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(20), nullable=True, server_default="", comment="会议室名字")
    address = Column(VARCHAR(20), nullable=True, server_default="", comment="会议室地址")
    city_id = Column(VARCHAR(32), ForeignKey('city.id', ondelete='CASCADE'), comment='城市id')
    period = Column(VARCHAR(32), comment='时间段', server_default="")
    employee_total = Column(Integer, comment='容纳人数', server_default="0")
    floor = Column(Integer, comment='层数/列数', server_default="0")
    pic_url = Column(VARCHAR(255), server_default="", comment="会议室图片")
    device_list = Column(VARCHAR(255), server_default="", comment="设备工具, 逗号分隔")
    layout_type = Column(TINYINT, comment='布局类型', server_default="0")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class City(db.Model):
    __tablename__ = 'city'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    city_name = Column(VARCHAR(20), nullable=True, server_default="", comment="城市名")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class MettingInfo(db.Model):
    __tablename__ = 'meeting_info'
    employee_meeting_type_enum = {
        1: "参会人员",
        2: "抄送人员"
    }
    meeting_status_enum = {
        0: "未反馈",
        1: "未签到",
        2: "已签到"
    }

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    meeting_id = Column(VARCHAR(32), ForeignKey('meeting.id', ondelete='CASCADE'), comment="会议id")
    employee_id = Column(VARCHAR(32), ForeignKey('employee.id', ondelete='CASCADE'), comment="人员id")
    employee_meeting_type = Column(TINYINT, comment='人员会议类型', server_default="0")
    department_name = Column(VARCHAR(20), comment="部门名称", server_default="")
    employee_name = Column(VARCHAR(20), comment="参会人员名称", server_default="")
    Position_name = Column(VARCHAR(20), comment="职务名称", server_default="")
    employee_phone = Column(VARCHAR(11), comment="联系方式", server_default="")
    meeting_status = Column(TINYINT, comment='会议状态', server_default="0")
    arrivals_time = Column(BigInteger, default=time.time, comment="到达日期", server_default="0")
    remark = Column(VARCHAR(255), nullable=True, comment='备注', server_default="")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class MettingDepartment(db.Model):
    __table__name = "meeting_department"

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    meeting_id = Column(VARCHAR(32), ForeignKey('meeting.id', ondelete='CASCADE'), comment="会议id")
    department_id = Column(VARCHAR(32), ForeignKey('department.id', ondelete='CASCADE'), comment='部门id')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class Employee(db.Model):
    __tablename__ = 'employee'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(20), nullable=True, server_default="", comment="名字")
    Position_name = Column(VARCHAR(20), comment="职务名称", server_default="")
    department_id = Column(VARCHAR(32), ForeignKey('department.id', ondelete='CASCADE'), comment='部门id')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class Department(db.Model):
    __tablename__ = "department"

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    department_name = Column(VARCHAR(20), nullable=True, server_default="", comment="部门名")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
