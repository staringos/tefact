"""
@author xiaofei
@date   2020-02-28
@desc
"""

from flask_restful import Resource
from extensions import db
from arrplat.common.utils import json_response, generate_uuid, sql_tuple_to_dict, sql_execute_commit, wx_get_user_info
import pymysql, pendulum
from flask import request
import copy, time, json
from ..models.models import Banner, Article, Customer, Course, BaseCourse, Employee, Student, CourseSign, CourseLevel, \
    CampusClassroom, CourseType, Business, Packet, BaseInfo, StudentLevel, Order, Business, InstrumentType, \
    PacketSubject, Subject, Campus

from arrplat.resources.user.models import UserInfo
from arrplat.common.store_utils import redis_0
from ..controller.views import CommonResource


class LoginResource(Resource):
    customer = Customer()
    order = Order()
    student = Student()
    business = Business()
    campus = Campus()
    courseType = CourseType()
    employee = Employee()
    packet = Packet()
    baseCourse = BaseCourse()
    instrumentType = InstrumentType()

    def post(self):
        """登陆
         ---
         tags:
           - 学生端小程序
         parameters:
           - name: data
             in: body
             type: string
             required: true
             enum: [{"phone": "手机号", "source":5, "org_id": "组织id", "code": "微信登陆code", "encryptedData":"", "iv": ""}]
             description: 数据体
         responses:
           200:
             description:  成功
             examples:
               response: {
                "data": {
                    "list": [
                      {
                      "id": "学员id",
                      "customer_id": "客户id",
                      "customer_name": "客户名字",
                      "business_id": "商机id",
                      "business_name": "商机名字",
                      "customer_head_url": "客户头像",
                      "teacher_name": "老师名",
                      "teacher_id": "老师id",
                      "course_type_name": "课程种类",
                      "course_type_id": "课程种类id"
                      }
                    ],
                    "is_visitor": "是否为游客, 1是2否, list里为学员对应的商机信息, 游客为空"
                    },
                    "message": null,
                    "page": null
                    }
       """
        response = request.get_json()
        phone = response.get("phone", "")
        if not phone:
            return json_response(data={}, message="获取用户信息失败", status=500)
        # 获取微信信息
        user_info = wx_get_user_info(response["code"], response["encryptedData"], response["iv"])
        # user_info = {}
        openid = user_info.get("openid", "")
        nick_name = user_info.get("nickName", "")
        head_url = user_info.get("avatarUrl", "")
        unionid = user_info.get("unionid", "")
        # 判断该客户是否存在
        sql = f"select * from {self.customer.__tablename__} where phone='{phone}'"
        res = db.session.execute(sql)
        data = res.fetchall()
        # 转换
        data = sql_tuple_to_dict(data)
        db.session.commit()
        if data:
            # 存在更新属性
            data = data[0]
            data_id = data["id"]

            update_sql = f"update {self.customer.__tablename__} set openid='{openid}', unionid='{unionid}', " \
                f"update_time={int(time.time())},nick_name='{nick_name}',head_url='{head_url}'  where id = '{data_id}'"
            db.session.execute(update_sql)
            db.session.commit()
            # 查找返回对应学生信息
            select_sql = f"select student.*,`order`.customer_id, `order`.business_id, business.name as business_name," \
                f" customer.name as customer_name, customer.head_url as customer_head_url, campus.name as campus_name, u.nickname as teacher_name," \
                f" ty.id as course_type_id, ty.name as course_type_name, type1.name as instrument_type_name " \
                f" from {self.order.__tablename__} as `order`" \
                f" right join {self.student.__tablename__} as student on student.order_id=`order`.id" \
                f" left join {self.business.__tablename__} as business on `order`.business_id =business.id " \
                f" left join {self.customer.__tablename__} as customer on `order`.customer_id = customer.id" \
                f" left join {self.campus.__tablename__} as campus on student.campus_id=campus.id " \
                f" left join {self.employee.__tablename__} as employee on student.teacher_id=employee.id" \
                f" left join `user` as u on employee.user_id=u.id " \
                f" left join {self.packet.__tablename__} as packet on packet.id=student.current_packet_id" \
                f" left join {self.baseCourse.__tablename__} as baseCourse on packet.base_course_id=baseCourse.id " \
                f" left join {self.courseType.__tablename__} as ty on baseCourse.course_type_id=ty.id " \
                f" left join {self.instrumentType.__tablename__} as type1 on  student.instrument_type_id=type1.id" \
                f" where order.customer_id='{data_id}'"
            student_info = sql_execute_commit(select_sql)
            return json_response(data={"list": student_info, "is_visitor": 2})
        else:
            inser_dic = {
                "openid": openid,
                "nick_name": nick_name,
                "head_url": head_url,
                "phone": phone,
                "source": response.get("source", 5),
                "org_id": response.get("org_id", 5)
            }
            # 不存在则新建用户属性
            inser_dic["create_time"] = inser_dic["update_time"] = int(time.time())
            inser_dic["id"] = generate_uuid()
            field_str = ",".join(inser_dic.keys())
            value_str = ",".join([f"'{val}'" for val in inser_dic.values()])
            insert_sql = f"INSERT INTO {self.customer.__tablename__}({field_str}) VALUE({value_str})"
            db.session.execute(insert_sql)
            db.session.commit()
            # 返回为游客
            return json_response(data={"list": [], "is_visitor": 1})


class CourseResource(Resource):
    course = Course()
    baseCourse = BaseCourse()
    employee = Employee()
    student = Student()
    courseSign = CourseSign()
    courseLevel = CourseLevel()
    campusClassroom = CampusClassroom()
    courseType = CourseType()
    customer = Customer()
    business = Business()

    def get(self):
        """课程列表页
        ---
         tags:
           - 学生端小程序
         parameters:
            - name: campus_id
              in: query
              type: string
              required: true
              enum: ['0ed62d02491c4fb884d881c09d0f28a7']
              description: 校区id
            - name: teacher_employee_id
              in: query
              type: string
              required: false
              # enum: [{"name": "123", 'age': 13}]
              description: 教师id
            - name: instrument_type_id
              in: query
              type: string
              required: false
              description: 乐器类型
            - name: start_time
              in: query
              type: int
              required: false
              description: 当天的起始时间
            - name: sign_type
              in: query
              type: int
              required: false
              description: 签到状态
            - name: student_id
              in: query
              type: string
              required: false
              description: 学生id
            - name: is_student
              in: query
              type: string
              required: false
              description: 是否只查学生相关
         responses:
           status:
             description:
             examples:
               response: {
                    "data": {
                    "list": [
                      {
                        "appointment_num": "已约",
                        "last_num": "剩余",
                        "class_room_name": "教室名",
                        "course_name": "课程名",
                        "level_name": "等级名",
                        "subscript": "角标",
                        "remark": "备注",
                        "sign_type_str": "签到状态",
                        "reserve_type": "1可以预约2可以取消3已约满",
                        "course_type_id": "课程种类id",
                        "course_type_name": "课程种类名字"
                      }
                    ]
                    },
                    "message": null,
                    "page": null
                    }
               """

        campus_id = request.args.get('campus_id', "")
        teacher_employee_id = request.args.get("teacher_employee_id", "")
        instrument_type_id = request.args.get("instrument_type_id", "")
        start_time = int(request.args.get("start_time", pendulum.now().start_of("day").timestamp()))
        sign_type = int(request.args.get("sign_type", 0))
        student_id = request.args.get("student_id", "")
        is_student = int(request.args.get("is_student", 0))
        query = f" a.course_type=1  and a.start_time>{start_time} and a.end_time<{start_time + 86400}"
        query += f" and a.campus_id='{campus_id}'" if campus_id else ""
        query += f" and a.teacher_employee_id='{teacher_employee_id}'" if teacher_employee_id else ""
        query += f" and b.instrument_type_id='{instrument_type_id}'" if instrument_type_id else ""
        query += f" and sign.sign_type = {sign_type}" if sign_type else ""
        query += f" and sign.student_id = '{student_id}'" if student_id and is_student else ""
        sql = f"select a.*,b.name as course_name, b.student_count,b.is_other,b.is_cancel, d.nickname, e.name as level_name," \
            f" f.name as class_room_name, type1.id as course_type_id, type1.name as course_type_name" \
            f" from {self.course.__tablename__} as a " \
            f" left join {self.baseCourse.__tablename__} as b on a.base_course_id=b.id" \
            f" left join {self.employee.__tablename__} as c on a.teacher_employee_id=c.id " \
            f" left join `user` as d on c.user_id=d.id" \
            f" left join {self.courseLevel.__tablename__} as e on a.course_level_id=e.id " \
            f" left join {self.campusClassroom.__tablename__} as f on a.classroom_id=f.id " \
            f" left join {self.courseSign.__tablename__} as sign on a.id=sign.course_id" \
            f" left join {self.courseType.__tablename__} as type1 on b.course_type_id=type1.id" \
            f"  where {query} order by a.start_time asc"
        data = sql_execute_commit(sql)
        if data:
            # 获取该课已预约报名人数
            course_ids = [i["id"] for i in data]
            course_sgin_dic = self.getCoureSignCount(course_ids)
            # 获取课程跟学员的关系
            course_student_info = self.getStudentSignStatus(course_ids, student_id)
            # 计算已约和剩余人数
            for val in data:
                val["appointment_num"] = course_sgin_dic.get(val["id"], 0)  # 已约
                val["student_count"] = 0 if val["student_count"] is None else val["student_count"]
                val["last_num"] = val["student_count"] - val["appointment_num"]  # 剩余
                # 添加签到状态
                val["sign_type"] = 0 if course_student_info.get(val["id"], 0) is None else course_student_info.get(
                    val["id"], 0)
                val["sign_type_str"] = self.courseSign.sign_type_enum.get(val["sign_type"], "")
                val["reserve_type"] = 0
                if int(val["last_num"]) <= 0:
                    val["reserve_type"] = 3  # 已约满
                elif val["sign_type"] == 0:
                    val["reserve_type"] = 1  # 可以预约
                else:
                    val["reserve_type"] = 2  # 已预约, 可以取消

            return json_response(data={"list": data, "sign_type_enum": self.courseSign.mp_course_sign_type})
        else:
            return json_response(data={"list": [], "sign_type_enum": self.courseSign.mp_course_sign_type})

    def getCourseInfo(self, course_ids):
        # 获取要点信息
        course_ids_str = str(tuple(course_ids)) if len(course_ids) > 1 else str(tuple(course_ids)).replace(
            ",", "")
        # 获取课程信息
        sql = f"select course.*, baseCourse.name as course_name, baseCourse.student_count, baseCourse.is_cancel, baseCourse.course_type_id, baseCourse.is_other from {self.course.__tablename__} as course left join {self.baseCourse.__tablename__} as baseCourse on course.base_course_id" \
            f"=baseCourse.id where course.id in {course_ids_str}"
        data = sql_execute_commit(sql)
        res = {}
        for val in data:
            res[val["id"]] = val
        return res

    def getCoureSignCount(self, course_ids: list):
        # 获取课程列表所有的报名人数
        course_ids_str = str(tuple(course_ids)) if len(course_ids) > 1 else str(tuple(course_ids)).replace(
            ",", "")
        sql = f"select count(1) as total, course_id from {self.courseSign.__tablename__} where course_id in {course_ids_str} group by course_id"
        data = sql_execute_commit(sql)
        dic = {}
        for val in data:
            dic[val["course_id"]] = val["total"]
        return dic

    def getStudentSignStatus(self, course_ids: list, student_id):
        # 获取学生预约的课程
        course_ids_str = str(tuple(course_ids)) if len(course_ids) > 1 else str(tuple(course_ids)).replace(
            ",", "")
        sql = f"select course_id, sign_type from {self.courseSign.__tablename__} where student_id='{student_id}' and course_id in {course_ids_str}"
        data = sql_execute_commit(sql)
        dic = {}
        for val in data:
            dic[val["course_id"]] = val["sign_type"]
        return dic


class CourseSignResource(Resource):
    courseSign = CourseSign()
    student = Student()
    baseCourse = BaseCourse()
    packet = Packet()
    courseResource = CourseResource()

    def post(self):
        """预约课程
          ---
          tags:
            - 学生端小程序
          parameters:
            - name: data
              in: body
              type: string
              required: true
              enum: [{"student_id": "学生id", "course_id": "课程id", "org_id":"组织id"}]
              description: 数据体
          responses:
            200:
              description:  成功
              examples:
                response: {"message": "ok"}
        """
        data = request.get_json()
        student_id = data.get("student_id", "")
        course_id = data.get("course_id", "")
        org_id = data.get("org_id", "")
        # 获取学生信息
        sql = f"select student.*, baseCourse.course_type_id, baseCourse.student_count from {self.student.__tablename__} as student left join {self.packet.__tablename__} as packet " \
            f"on packet.id=student.current_packet_id left join {self.baseCourse.__tablename__} as baseCourse on packet.base_course_id=baseCourse.id" \
            f" where student.id='{student_id}'"
        student_info = sql_execute_commit(sql)
        # 判断课程类型 is_other=1就不受课程类型限制
        course_info = self.courseResource.getCourseInfo([course_id]).get(course_id, {})
        if course_info["is_other"] != 1 and student_info[0]["course_type_id"] != course_info.get("course_type_id", ""):
            return json_response(data={}, message="课程类型不同,不能预约", status=500)
        # 再判断课程人数
        sign_count = self.courseResource.getCoureSignCount([course_id]).get(course_id, 0)
        if course_info["student_count"] is None or course_info["student_count"] <= sign_count:
            return json_response(data={}, message="预约学员数已满", status=500)
        # 插入
        uid = generate_uuid()
        now_time = int(time.time())
        key_str = "(`id`,course_id, teacher_id, student_id, create_time, update_time, sign_type, apply_type)"
        val_str = ",".join([f"'{i}'" for i in
                            [uid, course_info["id"], course_info["teacher_employee_id"], student_id, now_time,
                             now_time, 7, 1]])
        sign_insert_sql = f"INSERT INTO {self.courseSign.__tablename__}{key_str} VALUES ({val_str})"
        print(sign_insert_sql)
        db.session.execute(sign_insert_sql)
        db.session.commit()
        return json_response(data={}, message="预约成功")

    def delete(self):
        """取消预约
          ---
          tags:
            - 学生端小程序
          parameters:
            - name: data
              in: body
              type: string
              required: true
              enum: [{"student_id": "学生id", "course_id": "课程id"}]
              description: 数据体
          responses:
            200:
              description:  成功
              examples:
                response: {"message": "ok"}
        """
        data = request.get_json()
        student_id = data.get("student_id", "")
        course_id = data.get("course_id", "")

        # 判断该课程是否允许取消
        course_info = self.courseResource.getCourseInfo([course_id]).get(course_id, {})
        if course_info.get("is_cancel", 0) != 1:
            return json_response(data={}, message="该课程不允许取消", status=500)
        # 更改状态
        try:
            sql = f"UPDATE {self.courseSign.__tablename__} set sign_type=2 where course_id ='{course_id}' and student_id = '{student_id}'"
            db.session.execute(sql)
            db.session.commit()
        except Exception as e:
            return json_response(message=f"取消预约，{e}", status=500)
        return json_response(data={}, message="取消预约成功")


class BannerResource(Resource):
    banner = Banner()

    def get(self):
        """banner图查询
            ---
             tags:
               - 学生端小程序
             responses:
                status:
                  description:
                  examples:
                    response: {
                       "data": {
                         "list": [
                         {}
                         ]
                       },
                       "message": null,
                       "page": null
                     }
         """
        sql = f"select * from {self.banner.__tablename__} order by sort desc limit 5"
        data = sql_execute_commit(sql)
        return json_response(data={"list": data})


class ArticleResource(Resource):
    article = Article()

    def get(self):
        """文章列表
            ---
             tags:
               - 学生端小程序
             parameters:
               - name: page
                 in: query
                 type: int
                 required: false
                 description: 页数
               - name: size
                 in: query
                 type: int
                 required: false
                 description: 条数
             responses:
                status:
                  description:
                  examples:
                    response: {
                       "data": {
                         "list": [
                         {}
                         ]
                       },
                       "message": null,
                       "page": null
                     }
         """
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 5))
        index = (page - 1) * size
        sql = f"select * from {self.article.__tablename__} order by is_top desc, sort desc limit {index},{size} "
        data = sql_execute_commit(sql)
        # 获取数据量
        total_sql = f"select count(1) as total from {self.article.__tablename__}"
        total = sql_execute_commit(total_sql)
        total = total[0].get("total", 0) if total else 0
        return json_response(data={"list": data, "total": total})


class CustomerResource(Resource):
    customer = Customer()

    def post(self):
        """申请免费课
          ---
          tags:
            - 学生端小程序
          parameters:
            - name: data
              in: body
              type: string
              required: true
              enum: [{"name": "名字", "phone": "手机号", "source": 5, "phone_code": "验证码", "org_id": "d06455545e6d4b929f4fbacbdc93dd24"}]
              description: 数据体
          responses:
            200:
              description:  成功
              examples:
                response: {"message": "ok"}
        """

        data = request.get_json()
        data["org_id"] = "d06455545e6d4b929f4fbacbdc93dd24"
        phone = data.get("phone", "")
        phone_code = data.get("phone_code", "")
        # 判断验证码
        if redis_0.get(f"mp_code_{phone}") and phone_code == str(redis_0.get(f"mp_code_{phone}"), "utf8"):
            pass
        else:
            return json_response(data={}, message="验证码错误/过期", status=500)
        del data["phone_code"]
        # 覆盖逻辑, 先判断之前有没有
        select_sql = f"select * from {self.customer.__tablename__} where phone='{phone}'"
        res = db.session.execute(select_sql)
        customer_info = res.fetchall()
        db.session.commit()
        customer_info = sql_tuple_to_dict(customer_info)
        if customer_info:
            update_sql = f"""UPDATE {self.customer.__tablename__} set `name`='{data["name"]}', source={data[
                "source"]}, update_time={int(time.time())} where id = '{customer_info[0]["id"]}' """
            db.session.execute(update_sql)
        else:
            data["id"] = generate_uuid()
            data["create_time"] = data["update_time"] = int(time.time())
            field_str = ",".join(data.keys())
            value_str = ",".join([f"'{val}'" for val in data.values()])
            insert_sql = f"INSERT INTO {self.customer.__tablename__}({field_str}) VALUE({value_str})"
            db.session.execute(insert_sql)
        db.session.commit()
        return json_response(data={}, message="申请成功")


class BaseInfoResource(Resource):
    baseInfo = BaseInfo()

    def get(self):
        """四个快捷入口
            ---
             tags:
               - 学生端小程序
             responses:
               status:
                 description:
                 examples:
                   response: {
                      "data": {
                        "list": [

                        ]
                      }
                    }
           """
        sql = f"select * from {self.baseInfo.__tablename__} order by create_time asc"
        data = sql_execute_commit(sql)
        return json_response(data={"list": data})


class StudentResource(Resource):
    student = Student()
    studentLevel = StudentLevel()

    def get(self):
        """排行榜
           ---
            tags:
              - 学生端小程序
            parameters:
               - name: page
                 in: query
                 type: int
                 required: false
                 description: 页数
               - name: size
                 in: query
                 type: int
                 required: false
                 description: 条数
            responses:
              status:
                description:
                examples:
                  response: {
                     "data": {
                       "list": [

                       ]
                     }
                   }
          """
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 5))
        index = (page - 1) * size
        sql = f"select student.id, student.name, level.name as level_name from {self.student.__tablename__} as student left join {self.studentLevel.__tablename__}" \
            f" as level on student.level_id=level.id order by level.sort desc limit {index},{size}"
        data = sql_execute_commit(sql)
        return json_response(data={"list": data})


class EmployeeResource(Resource):
    employee = Employee()
    userInfo = UserInfo()

    def get(self):
        """查看老师信息
           ---
            tags:
              - 学生端小程序
            parameters:
               - name: teacher_id
                 in: query
                 type: int
                 required: false
                 description: 老师id
            responses:
              status:
                description:
                examples:
                  response: {
                     "data": {
                       "list": [

                       ]
                     }
                   }
          """
        teacher_id = request.args.get("teacher_id", "")
        sql = f"select emloyee.*, info.head_url, info.signature, `user`.nickname  from {self.employee.__tablename__} as emloyee left join {self.userInfo.__tablename__} as info on " \
            f" emloyee.user_id=info.user_id left join `user` as `user` on `user`.id=emloyee.user_id where emloyee.id='{teacher_id}'"
        data = sql_execute_commit(sql)
        data = data[0] if data else {}
        return json_response(data=data)


class LearnResource(Resource):
    student = Student()
    studentLevel = StudentLevel()
    packet = Packet()
    baseCourse = BaseCourse()
    InstrumentType = InstrumentType()
    employee = Employee()
    courseSign = CourseSign()
    packetSubject = PacketSubject()
    subject = Subject()
    commonResource = CommonResource()

    def get(self):
        """学习进度
          ---
           tags:
             - 学生端小程序
           parameters:
              - name: student_id
                in: query
                type: int
                required: false
                description: 学生id
           responses:
             status:
               description:
               examples:
                 response: {
                    "data": {
                      "able_info": [
                          {
                            "id": "1",
                            "name": "主题1"
                          },
                          {
                            "id": "2",
                            "name": "主题2"
                          }
                        ],
                        "learn_info": {
                          "learn_duration": "累计时长",
                          "learn_number": "累计上课次数/已用时长",
                          "total_duration": "总时长"
                        },
                        "student_info": {
                            "level_name": "等级",
                            "instrument_name": "乐器类型",
                            "teacher_name": "教师名",
                            "packet_name": "套餐名"
                        }
                    }
                  }
         """
        student_id = request.args.get("student_id", "")
        # 学员信息
        student_info_sql = f"select student.*, leve.name as level_name, packet.name as packet_name, instrument.name as instrument_name," \
            f" `user`.nickname as teacher_name from {self.student.__tablename__} as student left join {self.studentLevel.__tablename__} as leve " \
            f" on student.level_id=leve.id left join {self.packet.__tablename__} as packet on student.current_packet_id = " \
            f" packet.id left join {self.baseCourse.__tablename__} as base on base.id=packet.base_course_id left join " \
            f" {self.InstrumentType.__tablename__} as instrument on base.instrument_type_id=instrument.id left join " \
            f" {self.employee.__tablename__} as emloyee on emloyee.id=student.teacher_id left join `user` as `user` on" \
            f" `user`.id=emloyee.user_id where student.id='{student_id}'"
        student_info = sql_execute_commit(student_info_sql)
        if student_info:
            student_info = student_info[0]
        else:
            return json_response(data={}, message="找不见该学员信息", status=500)
        # 学习进度--只算正式课签到
        # 上课次数时长
        learn_number = self.commonResource.getStudentLearn(student_id)
        learn_duration = learn_number * 60
        # 能力值
        packet_id = student_info.get("current_packet_id", "")
        # able_sql = f"select subject.id, subject.name from {self.packetSubject.__tablename__} as packetSubject left join {self.subject.__tablename__}" \
        #     f" as subject on packetSubject.subject_id=subject.id where packetSubject.packet_id='{packet_id}'"
        # able = sql_execute_commit(able_sql)
        able = self.commonResource.getStudentAble(packet_id)
        result = {"student_info": student_info,
                  "learn_info": {"learn_number": learn_number, "learn_duration": learn_duration,
                                 "total_duration": student_info["all_class_hours"]}, "able_info": able}
        return json_response(data=result)
