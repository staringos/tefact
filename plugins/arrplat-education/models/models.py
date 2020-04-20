import time

from sqlalchemy import Column, Integer, \
    ForeignKey, BigInteger, VARCHAR, DECIMAL, Text, Float
from arrplat.common.utils import generate_uuid
from extensions import db
from sqlalchemy.dialects.mysql import TINYINT


class Course(db.Model):
    __tablename__ = 'edu_course'
    __table_args__ = (
        db.UniqueConstraint('campus_id', 'teacher_employee_id', 'start_time', name='uix_campus_teacher_time'),
    )
    color_enum = {
        1: 'red',
        2: 'blue'
    }
    course_type_enum = {
        1: "正式课",
        2: "试听课",
        3: "占用"
    }

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(20), nullable=True, server_default="")
    teacher_employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='教师ID')
    base_course_id = Column(VARCHAR(32), comment='基础课程', server_default="")
    campus_id = Column(VARCHAR(32), ForeignKey('edu_campus.id', ondelete='CASCADE'), comment='校区id')
    classroom_id = Column(VARCHAR(32), comment='教室id', server_default="")
    # student_count = Column(Integer, nullable=True, server_default="0")
    material_id = Column(VARCHAR(255), comment='素材ID', server_default="")
    start_time = Column(BigInteger, nullable=True, server_default="0")
    end_time = Column(BigInteger, nullable=True, server_default="0")
    color = Column(TINYINT, comment='颜色  1：red  2：blue, 无用,默认用基础课程字段, 试听和占用使用固定颜色', server_default="0")
    status = Column(TINYINT, server_default="0")
    remark = Column(VARCHAR(200), nullable=True, comment='备注', server_default="")
    course_type = Column(TINYINT, comment='课程类型 1正式2试听3占用', server_default="0")
    course_level_id = Column(VARCHAR(32), comment='课程等级', server_default="")
    sale_employee_id = Column(VARCHAR(32), comment='销售人员id', server_default="")
    description = Column(VARCHAR(1024), server_default="")
    intention = Column(TINYINT, comment='意向', server_default="0")
    intention_remark = Column(VARCHAR(1024), comment='意向备注', server_default="")
    create_time = Column(BigInteger, default=time.time, comment='注册时间', server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    org_id = Column(VARCHAR(32), comment='组织ID', server_default="")
    is_limit_student = Column(TINYINT, comment='仅自己学员可见, 1是2否', server_default="1")
    customer_id = Column(VARCHAR(32), comment='客户ID', server_default="")
    business_id = Column(VARCHAR(32), comment='商机ID', server_default="")
    subscript = Column(VARCHAR(20), nullable=True, comment="角标, 自定义字符", server_default="")

    def __repr__(self):
        return '<{}: phone: {} >'.format(
            self.__class__.__name__, self.name
        )

    __str__ = __repr__


class BaseCourse(db.Model):
    __tablename__ = 'edu_base_course'

    crowd_type_enum = {
        1: '成人',
        2: '儿童',
        3: '学生',
    }

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(20), nullable=True, server_default="")
    course_type_id = Column(VARCHAR(32), ForeignKey('edu_course_type.id', ondelete='CASCADE'), comment='课程种类')
    instrument_type_id = Column(VARCHAR(32), ForeignKey('edu_instrument_type.id', ondelete='CASCADE'), comment='乐器类型',
                                nullable=True)
    class_points = Column(Integer, comment='每次消耗课点', server_default="0")
    class_minutes = Column(Integer, comment='每课时分钟数', server_default="0")
    crowd_type = Column(TINYINT, comment='适合人群', server_default="0")
    student_count = Column(Integer, comment='最大学员数', server_default="0")
    is_formal = Column(TINYINT, comment='是否是正式课', server_default="0")
    is_other = Column(TINYINT, comment='能不能约别的课', server_default="0")
    color = Column(VARCHAR(32), comment='颜色标签', server_default="0")
    is_cancel = Column(TINYINT, comment='是否允许学员取消', server_default="0")
    is_enabled = Column(TINYINT, comment='是否启用', server_default="0")
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class BaseCourseCampus(db.Model):
    __tablename__ = 'edu_base_course_campus'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    base_course_id = Column(VARCHAR(32), ForeignKey('edu_base_course.id', ondelete='CASCADE'), comment='')
    campus_id = Column(VARCHAR(32), ForeignKey('edu_campus.id', ondelete='CASCADE'), comment='')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class Employee(db.Model):
    __tablename__ = 'edu_employee'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    level = Column(Integer, default=1, comment="教师等级", server_default="0")
    is_teacher = Column(TINYINT, default=1, comment="是否是老师(0 false 1 true)", server_default="0")
    campus_id = Column(VARCHAR(32), ForeignKey('edu_campus.id', ondelete='CASCADE'), comment='员工关联校区')
    user_id = Column(VARCHAR(32), ForeignKey('user.id', ondelete='CASCADE'), comment='关联登录用户')
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')

    create_time = Column(BigInteger, default=time.time, comment='注册时间', server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")

    def __repr__(self):
        return '<{}: {} >'.format(
            self.__class__.__name__, self.name
        )

    __str__ = __repr__


class Campus(db.Model):
    __tablename__ = 'edu_campus'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    number = Column(Integer, nullable=True, server_default="0")
    name = Column(VARCHAR(20), nullable=True, server_default="")
    address = Column(VARCHAR(128), nullable=True, server_default="")
    manage_employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='管理员ID')
    classroom_count = Column(Integer, default=0, comment='教室数', server_default="0")
    is_enabled = Column(TINYINT, default=0, comment='是否启用', server_default="0")
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')

    description = Column(VARCHAR(1024), server_default="")
    create_time = Column(BigInteger, default=time.time, comment='注册时间', server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class CourseStudent(db.Model):
    __tablename__ = 'edu_course_student'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    course_id = Column(VARCHAR(32), ForeignKey('edu_course.id', ondelete='CASCADE'), comment='课程ID')
    student_id = Column(VARCHAR(32), ForeignKey('edu_student.id', ondelete='CASCADE'), comment='学生ID')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class CourseTag(db.Model):
    __tablename__ = 'edu_course_tag'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    course_id = Column(VARCHAR(32), ForeignKey('edu_course.id', ondelete='CASCADE'), comment='课程ID')
    tag_id = Column(VARCHAR(32), ForeignKey('edu_tag.id', ondelete='CASCADE'), comment='标签ID')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class Tag(db.Model):
    __tablename__ = 'edu_tag'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(20), nullable=True, server_default="")
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class CampusClassroom(db.Model):
    __tablename__ = 'edu_campus_classroom'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(20), nullable=True, server_default="")
    campus_id = Column(VARCHAR(32), ForeignKey('edu_campus.id', ondelete='CASCADE'), comment='关联校区')
    is_enabled = Column(TINYINT, default=1, comment='1:启用  2： 停用', server_default="0")
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class Material(db.Model):
    __tablename__ = 'edu_material'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(20), nullable=True, server_default="")
    employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所有者')
    teacher_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所属老师')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    status = Column(TINYINT, server_default="0")


class Subject(db.Model):
    __tablename__ = 'edu_subject'

    crowd_type_enum = {
        1: '成人',
        2: '儿童',
        3: '学生',
    }

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    instrument_type_id = Column(VARCHAR(32), ForeignKey('edu_instrument_type.id', ondelete='CASCADE'), comment='乐器ID')
    difficulty = Column(TINYINT, comment='难度', server_default="0")
    crowd_type = Column(TINYINT, comment='适合人群', server_default="0")
    is_enabled = Column(TINYINT, comment='是否启用', server_default="0")

    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")

    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')


class SubjectEssential(db.Model):
    __tablename__ = 'edu_subject_essential'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    subject_id = Column(VARCHAR(32), ForeignKey('edu_subject.id', ondelete='CASCADE'), comment='')
    essential_id = Column(VARCHAR(32), ForeignKey('edu_essential.id', ondelete='CASCADE'), comment='')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class SubjectCampus(db.Model):
    __tablename__ = 'edu_subject_campus'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    subject_id = Column(VARCHAR(32), ForeignKey('edu_subject.id', ondelete='CASCADE'), comment='')
    campus_id = Column(VARCHAR(32), ForeignKey('edu_campus.id', ondelete='CASCADE'), comment='')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class Packet(db.Model):
    __tablename__ = 'edu_packet'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    price = Column(DECIMAL)
    origin_price = Column(DECIMAL)
    intro = Column(VARCHAR(1024), server_default="")
    start_time = Column(BigInteger, server_default="0")
    end_time = Column(BigInteger, server_default="0")
    is_hour_limit = Column(TINYINT, comment='是否限课时', server_default="0")
    class_hours = Column(Integer, comment='课时', server_default="0")
    class_points = Column(Integer, comment='课点', server_default="0")
    is_enabled = Column(TINYINT, comment='是否启用', server_default="0")
    base_course_id = Column(VARCHAR(32), ForeignKey('edu_base_course.id', ondelete='CASCADE'), comment='基础课程')
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class PacketSubject(db.Model):
    __tablename__ = 'edu_packet_subject'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    subject_id = Column(VARCHAR(32), ForeignKey('edu_subject.id', ondelete='CASCADE'), comment='主题ID')
    packet_id = Column(VARCHAR(32), ForeignKey('edu_packet.id', ondelete='CASCADE'), comment='套餐ID')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class Student(db.Model):
    __tablename__ = 'edu_student'
    sex_enum = {
        1: "男",
        2: "女"
    }
    has_basis_enum = {
        1: "有",
        2: "无"
    }
    has_comment_enum = {
        1: "未点评",
        2: "已告知",
        3: "已点评"
    }

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    phone = Column(VARCHAR(11), server_default="")
    sex = Column(TINYINT, server_default="0")
    number = Column(Integer, comment='学号', server_default="0")
    level_id = Column(VARCHAR(32), ForeignKey('edu_student_level.id', ondelete='CASCADE'), comment='学生等级ID')
    campus_id = Column(VARCHAR(32), ForeignKey('edu_campus.id', ondelete='CASCADE'), comment='校区ID')
    apply_time = Column(BigInteger, comment='报名时间', server_default="0")
    end_time = Column(BigInteger, comment='结课时间', server_default="0")
    teacher_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='老师ID')
    has_basis = Column(TINYINT, comment='有无基础', server_default="2")
    current_packet_id = Column(VARCHAR(32), ForeignKey('edu_packet.id', ondelete='CASCADE'), comment='当前套餐')
    order_id = Column(VARCHAR(32), comment='订单id', server_default="")
    instrument_type_id = Column(VARCHAR(32), ForeignKey('edu_instrument_type.id', ondelete='CASCADE'), comment='乐器类型')
    instrument_use_id = Column(VARCHAR(32), ForeignKey('edu_instrument_use.id', ondelete='CASCADE'), comment='乐器使用情况')
    has_comment = Column(TINYINT, comment='是否点评', server_default="1")
    remark = Column(VARCHAR(1024), comment='点评信息', server_default="")
    is_enabled = Column(TINYINT, comment='是否可以约课', server_default="2")
    is_locked = Column(TINYINT, comment='是否冻结课程', server_default="0")
    locked_times = Column(Integer, comment='冻结课程次数', server_default="0")
    is_lock_teacher = Column(TINYINT, comment='是否锁定老师', server_default="0")
    is_end = Column(TINYINT, comment='是否结课', server_default="2")
    is_teach_plan = Column(TINYINT, comment='是否教学计划', server_default="2")
    show_student_value = Column(TINYINT, comment='学员的能力值是否可见', server_default="2")
    all_class_hours = Column(Integer, comment='课时', server_default="0")
    used_class_hours = Column(Integer, comment='已用课时', server_default="0")
    remainder_class_points = Column(Integer, comment='剩余课点', server_default="0")
    sign_times = Column(Integer, comment='签到次数', server_default="0")
    student_color = Column(TINYINT, comment='颜色', server_default="0")
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class StudentColor(db.Model):
    __tablename__ = 'edu_student_color'

    color_enum = {
        1: 'RED',
        2: 'BLUE'
    }

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    course_id = Column(VARCHAR(32), ForeignKey('edu_student.id', ondelete='CASCADE'), comment='课程ID')
    color = Column(TINYINT, default=1, comment='颜色  1： 红色 2： 绿色', server_default="0")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class StudentValue(db.Model):
    __tablename__ = 'edu_student_value'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    student_id = Column(VARCHAR(32), ForeignKey('edu_student.id', ondelete='CASCADE'), comment='')
    subject_id = Column(VARCHAR(32), ForeignKey('edu_subject.id', ondelete='CASCADE'), comment='')
    value = Column(Integer, comment='能力值', server_default="0")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class StudentCourseLock(db.Model):
    __tablename__ = 'edu_student_course_lock'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    student_id = Column(VARCHAR(32), ForeignKey('edu_student.id', ondelete='CASCADE'), comment='')
    teacher_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='老师ID')
    start_time = Column(BigInteger, default=time.time, comment='开始时间', server_default="0")
    end_time = Column(BigInteger, default=time.time, comment='结束时间', server_default="0")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class StudentRemark(db.Model):
    __tablename__ = 'edu_student_remark'
    remark_type_enum = {
        1: "学员",
        2: "教师"
    }

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    student_id = Column(VARCHAR(32), ForeignKey('edu_student.id', ondelete='CASCADE'), comment='')
    teacher_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='老师ID')
    remark_type = Column(TINYINT, comment='备注类型(学员/教师)', server_default="0")
    remark = Column(VARCHAR(1024), comment='备注内容', server_default="")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class Customer(db.Model):
    __tablename__ = 'edu_customer'

    intention_enum = {
        1: '精准',
        2: '有意向',
        3: '意向一般',
        4: '长期关注',
        5: '无意向'
    }

    source_enum = {
        1: '大众美团',
        2: '学员推荐',
        3: '临时到店',
        4: '其他',
        5: '微信小程序'
    }

    status_enum = {
        1: '进行中',
        2: '已成单',
        3: '已结束',
        4: '无效客户'
    }

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    nick_name = Column(VARCHAR(32), comment="微信昵称", server_default="")
    openid = Column(VARCHAR(32), comment="微信用户当前应用标识", server_default="")
    unionid = Column(VARCHAR(32), comment="微信用户统一标识", server_default="")
    head_url = Column(VARCHAR(255), comment="微信头像", server_default="")
    phone = Column(VARCHAR(11), server_default="")
    remark = Column(VARCHAR(1024), server_default="")
    sex = Column(TINYINT, server_default="0")
    ages = Column(TINYINT, server_default="0")
    has_arrived = Column(TINYINT, comment='是否二次到店', server_default="0")
    has_basis = Column(TINYINT, comment='是否有基础', server_default="0")
    source = Column(TINYINT, comment='来源', server_default="0")
    color = Column(TINYINT, comment='颜色标签', server_default="0")
    connect_employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='联系客户人', )
    recommend_employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='获取信息人')
    current_packet_id = Column(VARCHAR(32), ForeignKey('edu_packet.id', ondelete='CASCADE'), comment='当前套餐')
    instrument_type_id = Column(VARCHAR(32), ForeignKey('edu_instrument_type.id', ondelete='CASCADE'), comment='乐器类型')
    campus_id = Column(VARCHAR(32), ForeignKey('edu_campus.id', ondelete='CASCADE'), comment='校区')
    status = Column(TINYINT, comment='客户状态', server_default="0")
    intention = Column(TINYINT, comment='客户意向', server_default="0")
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class Business(db.Model):
    __tablename__ = 'edu_business'
    business_status_enum = {
        1: "考虑中",
        2: "已成单",
        3: "确认不购"
    }

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    business_name = Column(VARCHAR(32), comment='商机名称', server_default="")
    business_type = Column(TINYINT, comment='商机类型(试听/非试听)', server_default="0")
    business_status = Column(TINYINT, comment='试听阶段', server_default="0")
    color = Column(TINYINT, comment='颜色标签', server_default="0")
    phone = Column(VARCHAR(11), server_default="")
    sex = Column(TINYINT, server_default="0")
    ages = Column(TINYINT, server_default="0")
    has_basis = Column(TINYINT, comment='是否有基础', server_default="0")
    instrument_type_id = Column(VARCHAR(32), ForeignKey('edu_instrument_type.id', ondelete='CASCADE'), comment='乐器类型',
                                server_default="")
    customer_id = Column(VARCHAR(32), ForeignKey('edu_customer.id', ondelete='CASCADE'), comment='客户ID',
                         server_default="")
    sales_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='课程ID', server_default="")
    intention = Column(TINYINT, comment='客户意向', server_default="0")
    teacher_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='老师ID',
                        server_default="")
    remark = Column(VARCHAR(1024), server_default="")
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID', server_default="")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class Order(db.Model):
    __tablename__ = 'edu_order'
    pay_type_enum = {
        1: '微信',
        2: '支付宝',
        3: '银行卡',
        4: '现金'
    }

    status_enum = {
        1: '已成单',
        2: '无效订单',
        3: '已退费'
    }
    order_type_enum = {
        1: "课程类",
        2: "物品类",
        3: "其他"
    }

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    customer_id = Column(VARCHAR(32), ForeignKey('edu_customer.id', ondelete='CASCADE'), comment='客户ID')
    business_id = Column(VARCHAR(32), ForeignKey('edu_business.id', ondelete='CASCADE'), comment='客户ID')
    order_type = Column(TINYINT, comment='1:课程类 2:物品类 3:其它', server_default="0")
    packet_id = Column(VARCHAR(32), ForeignKey('edu_packet.id', ondelete='CASCADE'), comment='当前套餐', )
    instrument_type_id = Column(VARCHAR(32), ForeignKey('edu_instrument_type.id', ondelete='CASCADE'), comment='乐器类型')
    category = Column(TINYINT, comment='订单二级类目', server_default="0")
    price = Column(DECIMAL)
    pay_price = Column(DECIMAL, comment='付款金额')
    pay_type = Column(TINYINT, comment='支付方式', server_default="0")
    is_owed = Column(TINYINT, comment='是否欠费', server_default="0")
    status = Column(TINYINT, comment='支付状态', server_default="0")
    remark = Column(VARCHAR(1024), server_default="")
    status_remark = Column(VARCHAR(1024), comment='异常情况备注', server_default="")
    other_name = Column(VARCHAR(32), comment='名称(其它时填写)', server_default="")
    campus_id = Column(VARCHAR(32), ForeignKey('edu_campus.id', ondelete='CASCADE'), comment='校区', server_default="")
    connect_employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='联系客户人')
    recommend_employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='获取信息人')
    sale_employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='销售人员')
    teacher_employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所属老师')
    audition_teacher_employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'),
                                          comment='试听课教师')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')


class Instrument(db.Model):
    __tablename__ = 'edu_instrument'
    instrument_type_enum = {
        1: 'GUITAR',
        2: 'UKULELE',
        3: 'PIANO'
    }

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    price = Column(DECIMAL)
    name = Column(VARCHAR(32), server_default="")
    instrument_type = Column(VARCHAR(32), ForeignKey('edu_instrument_type.id', ondelete='CASCADE'), comment='物品种类')
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class OrderData(db.Model):
    __tablename__ = 'edu_order_data'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    finish_order = Column(Integer, comment='已完成订单', server_default="0")
    refund_order = Column(Integer, comment='退费订单', server_default="0")
    course_order = Column(Integer, comment='课程类订单', server_default="0")
    product_order = Column(Integer, comment='物品类订单', server_default="0")
    all_order = Column(Integer, comment='全部订单', server_default="0")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    remark = Column(VARCHAR(1024), server_default="")
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')


class TeachData(db.Model):
    __tablename__ = 'edu_teach_data'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    teacher_number = Column(Integer, comment='教师数', server_default="0")
    course_number = Column(Integer, comment='课程数', server_default="0")
    work_time = Column(Float, comment='工作时长')
    usedCourse_time = Column(Float, comment='消耗课时数')
    student_number = Column(Integer, comment='学生数', server_default="0")
    remark = Column(VARCHAR(1024), server_default="")
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class BaseInfo(db.Model):
    __tablename__ = 'edu_base_info'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    logo_url = Column(VARCHAR(255), comment='logo路径', server_default="")
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class CourseType(db.Model):
    __tablename__ = 'edu_course_type'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所有者')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    status = Column(TINYINT, server_default="0")


class Essential(db.Model):
    __tablename__ = 'edu_essential'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    level = Column(Integer, server_default="0")
    content = Column(VARCHAR(1024), comment='要点内容', server_default="")
    class_hours = Column(Float, comment='参考课时', server_default="0")
    employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所有者')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    status = Column(TINYINT, server_default="0")


class DifficultyLevel(db.Model):
    __tablename__ = 'edu_difficulty_level'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所有者')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    status = Column(TINYINT, server_default="0")


class InstrumentType(db.Model):
    __tablename__ = 'edu_instrument_type'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所有者',
                         server_default="")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    status = Column(TINYINT, server_default="0")


class InstrumentUse(db.Model):
    __tablename__ = 'edu_instrument_use'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所有者',
                         server_default="")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    status = Column(TINYINT, server_default="0")


class StudentLevel(db.Model):
    __tablename__ = 'edu_student_level'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    sort = Column(Integer, comment="排序字段", server_default="0")
    employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所有者',
                         server_default="")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    status = Column(TINYINT, server_default="0")


class TeacherLevel(db.Model):
    __tablename__ = 'edu_teacher_level'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所有者',
                         server_default="")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    status = Column(TINYINT, server_default="0")


class CourseLevel(db.Model):
    __tablename__ = 'edu_course_level'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所有者',
                         server_default="")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    status = Column(TINYINT, server_default="0")


class CustomerSource(db.Model):
    __tablename__ = 'edu_customer_source'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所有者',
                         server_default="")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    status = Column(TINYINT, server_default="0")


class Banner(db.Model):
    __tablename__ = 'edu_banner'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), server_default="")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所有者',
                         server_default="")
    image_url = Column(VARCHAR(255), server_default="")
    link_url = Column(VARCHAR(255), server_default="")
    article_id = Column(VARCHAR(32), comment='文章ID', server_default="")
    sort = Column(Integer, server_default="0")


class Article(db.Model):
    __tablename__ = 'edu_article'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    title = Column(VARCHAR(32), server_default="")
    subtitle = Column(VARCHAR(32), server_default="")
    content = Column(Text)
    is_top = Column(TINYINT, server_default="0")
    visible_type = Column(TINYINT, comment='可见类型', server_default="0")
    author = Column(VARCHAR(32), server_default="")
    employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所有者',
                         server_default="")
    sort = Column(Integer, server_default="0")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class Agreement(db.Model):
    __tablename__ = 'edu_agreement'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    is_enabled = Column(TINYINT, comment='是否启用', server_default="0")
    title = Column(VARCHAR(32), server_default="")
    content = Column(Text)
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所有者')


class About(db.Model):
    __tablename__ = 'edu_about'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    is_enabled = Column(TINYINT, comment='是否启用', server_default="0")
    title = Column(VARCHAR(32), server_default="")
    content = Column(Text)
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
    employee_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='所有者')


class PacketCampus(db.Model):
    __tablename__ = 'edu_packet_campus'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    packet_id = Column(VARCHAR(32), ForeignKey('edu_packet.id', ondelete='CASCADE'), comment='')
    campus_id = Column(VARCHAR(32), ForeignKey('edu_campus.id', ondelete='CASCADE'), comment='')
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")


class CourseSign(db.Model):
    __tablename__ = 'edu_course_sign'

    sign_type_enum = {
        1: "已签到",
        2: "取消预约",
        3: "学生旷课",
        4: "已签到",
        5: "无意向到店",
        6: "爽约",
        7: "已预约"
    }
    course_sign_type = {
        # 正式课
        1: {
            1: "已签到",
            2: "取消预约",
            3: "学生旷课",
            7: "已预约"
        },
        # 试听课
        2: {
            4: "已签到",
            5: "无意向到店",
            6: "爽约"
        }
    }
    # 小程序展示排序
    mp_course_sign_type = [
        {7: "已预约"},
        {1: "已签到"},
        {2: "取消预约"},
        {3: "学生旷课"}
    ]
    apply_type_enum = {
        1: "小程序约课",
        2: "教师约课"
    }

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    course_id = Column(VARCHAR(32), ForeignKey('edu_course.id', ondelete='CASCADE'), comment='课程ID')
    student_id = Column(VARCHAR(32), comment='学生ID', server_default="")
    teacher_id = Column(VARCHAR(32), ForeignKey('edu_employee.id', ondelete='CASCADE'), comment='老师id')
    sign_student_level_id = Column(VARCHAR(32), comment='学员等级', server_default="")
    subject_remark = Column(VARCHAR(1024), comment='主题要点', server_default="")
    complete_percent = Column(Integer, comment='完成率', server_default="0")
    apply_type = Column(TINYINT, comment='约课方式(小程序/教师约课)', server_default="0")
    # subject_id = Column(VARCHAR(32), ForeignKey('edu_subject.id', ondelete='CASCADE'), comment='主题ID', server_default="")
    material_id = Column(VARCHAR(255), comment='素材ID', server_default="")
    student_remark = Column(VARCHAR(1024), comment='备注(学员可见)', server_default="")
    teacher_remark = Column(VARCHAR(1024), comment='备注(后台可见)', server_default="")
    status = Column(TINYINT, server_default="0")
    sign_type = Column(TINYINT, comment='签到类型 正式/试听/非体系课程', server_default="0")
    subject_essential_info = Column(Text, comment='体系签到主题素材完成情况')
    business_id = Column(VARCHAR(32), comment='商机ID, 试听课签到', server_default="")
    create_time = Column(BigInteger, default=time.time, server_default="0")
    update_time = Column(BigInteger, default=time.time, server_default="0")
