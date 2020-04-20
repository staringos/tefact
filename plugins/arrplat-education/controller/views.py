from flask_restful import Resource
from arrplat.common.auth_jwt_utils import user_required
from ..models.models import Employee, Campus, Course, BaseCourse, InstrumentType, Employee, CourseType, CampusClassroom, \
    Student, CourseSign, CourseLevel, Material, Business, Customer, Packet, PacketSubject, Subject, Essential, \
    SubjectEssential, StudentLevel, Order, BaseCourseCampus, StudentRemark, InstrumentUse
from extensions import db
from arrplat.common.utils import json_response, generate_uuid, sql_tuple_to_dict, sql_execute_commit
import pymysql, pendulum, datetime
from flask import request
import copy, time, json
from arrplat.common.auth_jwt_utils import user_required
from arrplat.common.store_utils import redis_0
from flask_jwt_extended import (
    create_access_token,
    get_current_user
)
from arrplat.config import redis_key


class CommonResource(Resource):
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
    studentLevel = StudentLevel()
    packet = Packet()
    InstrumentType = InstrumentType()
    packetSubject = PacketSubject()
    subject = Subject()

    # 获取学员能力值
    def getStudentAble(self, packet_id):
        able_sql = f"select subject.id, subject.name from {self.packetSubject.__tablename__} as packetSubject left join {self.subject.__tablename__}" \
            f" as subject on packetSubject.subject_id=subject.id where packetSubject.packet_id='{packet_id}'"
        able = sql_execute_commit(able_sql)
        return able

    # 获取学员已用课时(学习进度)
    def getStudentLearn(self, student_id):
        learn_sql = f"select count(1) as total from {self.courseSign.__tablename__} where sign_type=1 and student_id='{student_id}'"
        learn = sql_execute_commit(learn_sql)
        learn_number = 0 if not learn else learn[0].get("total", 0)
        return learn_number


class MaterialResource(Resource):
    material = Material()

    def get(self):
        """素材列表
           ---
            tags:
              - 课程表
            parameters:
               - name: teacher_employee_id
                 in: query
                 type: string
                 required: true
                 description: 老师id
               - name: org_id
                 in: query
                 type: string
                 required: true
                 description: 组织id
            responses:
               status:
                 description:
                 examples:
                   response: {
                      "data": {
                        "list": [
                          {
                            "id": "1",
                            "name": "素材1"
                          }
                        ]
                      },
                      "message": null,
                      "page": null
                    }
        """
        teacher_employee_id = request.args.get('teacher_employee_id', "")
        org_id = request.args.get('org_id', "")
        if teacher_employee_id != "" and org_id != "":
            data = Material.query.filter(Material.teacher_id == teacher_employee_id, Material.org_id == org_id).all()
        else:
            data = Material.query.filter().all()
        res = []
        for val in data:
            res.append({"id": val.id, "name": val.name})

        return json_response(data={"list": res})

    def getMaterialInfo(self, material_ids: list) -> dict:
        # 获取要点信息
        material_ids_str = str(tuple(material_ids)) if len(material_ids) > 1 else str(tuple(material_ids)).replace(
            ",", "")
        sql = f"select * from {self.material.__tablename__} where `id` in {material_ids_str}"
        data = sql_execute_commit(sql)
        res = {}
        for val in data:
            res[val["id"]] = val
        return res


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
    materialResource = MaterialResource()

    @user_required
    def get(self):
        """课程表列表页&当前课程信息
        ---
         tags:
            - 课程表
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
              description: 起始时间
            - name: course_id
              in: query
              type: string
              required: false
              description: 课程id
            - name: types
              in: query
              type: int
              required: false
              description: 查询类型  编辑时当前课程信息(edit_info)
            - name: org_id
              in: query
              type: string
              required: true
              description: 组织id
         responses:
           status:
             description:
             examples:
               response: {
                    "data": {
                    "list": [
                      {
                        "day_date": "2020-02-16",
                        "day_name": "星期一",
                        "day_time": 1581868800,
                        "values": [
                          {
                            "id": "8cb919558b744127bb538bb44fc32da5",
                            "list": [
                              {},
                              {
                                "apply_type": null,
                                "base_course_id": "113eb80d79f2437fae2a0193f99e9cf7",
                                "business_id": null,
                                "campus_id": "1",
                                "classroom_id": null,
                                "color": null,
                                "course_color": 0,
                                "course_name": "AAA",
                                "course_type": 1,
                                "create_time": null,
                                "customer_id": null,
                                "description": null,
                                "end_time": 1581904800,
                                "id": "1",
                                "intention": null,
                                "intention_remark": null,
                                "is_limit_student": null,
                                "material_id": null,
                                "update_time": null,
                                "name": null,
                                "nickname": "arrplat_8888",
                                "org_id": null,
                                "remark": null,
                                "sale_employee_id": null,
                                "start_time": 1581901200,
                                "status": null,
                                "subscript": null,
                                "teacher_employee_id": "8cb919558b744127bb538bb44fc32da5"
                              },
                              {},
                              {},
                              {},
                              {},
                              {},
                              {},
                              {},
                              {},
                              {},
                              {},
                              {}
                            ],
                            "name": "arrplat_8888"
                          }
                        ]
                      },
                      {
                        "day_date": "2020-02-17",
                        "day_name": "星期二",
                        "day_time": 1581955200,
                        "values": []
                      },
                      {
                        "day_date": "2020-02-18",
                        "day_name": "星期三",
                        "day_time": 1582041600,
                        "values": []
                      },
                      {
                        "day_date": "2020-02-19",
                        "day_name": "星期四",
                        "day_time": 1582128000,
                        "values": []
                      },
                      {
                        "day_date": "2020-02-20",
                        "day_name": "星期五",
                        "day_time": 1582214400,
                        "values": []
                      },
                      {
                        "day_date": "2020-02-21",
                        "day_name": "星期六",
                        "day_time": 1582300800,
                        "values": []
                      },
                      {
                        "day_date": "2020-02-22",
                        "day_name": "星期日",
                        "day_time": 1582387200,
                        "values": []
                      }
                    ]
                    },
                    "message": null,
                    "page": null
                    }
               """
        user = get_current_user()
        # 获取修改前的信息
        if request.args.get("types", "") == "edit_info" and request.args.get("course_id", "") != "":
            return json_response(data=self.getCourseInfo(request.args["course_id"]))
        # 存储用户查询记录
        campus_id = request.args.get('campus_id', "")
        org_id = request.args.get('org_id', "")
        teacher_employee_id = request.args.get("teacher_employee_id", "")
        instrument_type_id = request.args.get("instrument_type_id", "")
        redis_0.hset(redis_key["user_select_history"], user.id,
                     json.dumps({"campus_id": campus_id, "teacher_employee_id": teacher_employee_id,
                                 "instrument_type_id": instrument_type_id}))
        # 只给一个时间, 获取这周,默认当前本周时间
        start_time = pendulum.now().start_of("week").timestamp()
        if int(request.args.get("start_time", 0)) != 0:
            start_time = pendulum.from_timestamp(int(request.args["start_time"]), "Asia/Shanghai").start_of(
                "week").timestamp()
        end_time = start_time + 7 * 86400
        # 老师和课程都属于这个校区
        query = f"a.campus_id='{campus_id}' and c.campus_id='{campus_id}' and a.org_id='{org_id}'"
        query += f" and a.start_time > {int(start_time)}"
        query += f" and a.end_time < {int(end_time)}"
        # 查询老师
        campus_teacher_query = ""
        if teacher_employee_id != "":
            teacher_employee_id_tuple = str(tuple(teacher_employee_id.split(","))) if len(
                teacher_employee_id.split(",")) > 1 else str(tuple(teacher_employee_id.split(","))).replace(",", "")
            query += f" and a.teacher_employee_id in {teacher_employee_id_tuple}"
            campus_teacher_query += f" and a.id in {teacher_employee_id_tuple}"
        if instrument_type_id != "":
            instrument_type_id_tuple = str(tuple(instrument_type_id.split(","))) if len(
                instrument_type_id.split(",")) > 1 else str(tuple(instrument_type_id.split(","))).replace(",", "")
            query += f" and b.instrument_type_id in {instrument_type_id_tuple}"

        sql = f"select a.*, b.color as course_color,b.name as course_name, d.nickname, e.name as level_name, f.name as " \
            f" class_room_name from {self.course.__tablename__} as a left join {self.baseCourse.__tablename__} as b " \
            f" on a.base_course_id=b.id left join {self.employee.__tablename__} as c on a.teacher_employee_id=c.id " \
            f" left join `user` as d on c.user_id=d.id left join {self.courseLevel.__tablename__} as e on a.course_level_id=e.id " \
            f"left join {self.campusClassroom.__tablename__} as f on a.classroom_id=f.id where {query} order by a.start_time asc"
        data = sql_execute_commit(sql)
        week_day_list = []

        # 获取该校区所有的老师
        campus_teacher_sql = f"select a.*, c.nickname from {self.employee.__tablename__} as a  left join `user` as c on a.user_id=c.id  where a.is_teacher=1 and a.campus_id='{campus_id}' {campus_teacher_query}"
        campus_teacher = sql_execute_commit(campus_teacher_sql)
        teacher_id_name = {i["id"]: i["nickname"] for i in campus_teacher}

        if data:
            # 获取当前的日期格式
            # start = data[0]["start_time"]
            # 获取当前周的开始时间
            # week_start = pendulum.from_timestamp(start, "Asia/Shanghai").start_of("week").timestamp()
            # 获取所有的课程id
            course_id_str = str(tuple([i["id"] for i in data])) if len(
                [i["id"] for i in data]) > 1 else str(tuple([i["id"] for i in data])).replace(",", "")
            # 获取本周课程的约课数
            signSql = f"select count(1) as total, course_id from {self.courseSign.__tablename__} where course_id in {course_id_str} group by course_id having total >0 "
            sign_res = db.session.execute(signSql)
            db.session.commit()
            course_id_total = sign_res.fetchall()
            course_id_total = sql_tuple_to_dict(course_id_total)
            course_id_total_dic = {i["course_id"]: i["total"] for i in course_id_total}
        else:
            course_id_total_dic = {}
        week_start = start_time
        # 获取周时间列表
        for index, t in enumerate(["一", "二", "三", "四", "五", "六", "日"]):
            day_time = week_start + index * 86400
            day_name = f"星期{t}"
            # 获取每天的老师课程
            result = []
            day_course = {}
            # 老师本周对应的被约课数
            day_reserve = {}
            for x in data:
                if x["start_time"] >= day_time and x["end_time"] <= day_time + 86400:
                    if day_course.get(x["teacher_employee_id"], 0) == 0:
                        day_course[x["teacher_employee_id"]] = {}
                        day_reserve[x["teacher_employee_id"]] = 0
                    day_course[x["teacher_employee_id"]][x["start_time"]] = x
                    # 判断是否被约, 试听课默认+1
                    if x["course_type"] == 2:
                        day_reserve[x["teacher_employee_id"]] += 1
                    elif course_id_total_dic.get(x["id"], 0) > 0:
                        day_reserve[x["teacher_employee_id"]] += 1
            # 获取每天的时间段 8点开始
            day_start = day_time + 28800

            # 如果没有课程添加空日期
            # if not day_course:
            #     week_day_list.append({"day_name": day_name, "day_time": day_time,
            #                           "day_date": pendulum.from_timestamp(day_time,
            #                                                               "Asia/Shanghai").to_date_string(),
            #                           "values": {}})

            for teacher in list(teacher_id_name.keys()):
                teacher_course_list = []
                for x in range(13):
                    now = day_start + x * 3600
                    teacher_course_list.append({}) if day_course.get(teacher, {}).get(now,
                                                                                      0) == 0 else teacher_course_list.append(
                        day_course.get(teacher, {}).get(now, 0))
                # 前端需求一个老师返回一条
                week_day_list.append({"day_name": day_name, "day_time": day_time,
                                      "day_date": pendulum.from_timestamp(day_time,
                                                                          "Asia/Shanghai").to_date_string(),
                                      "values": {"teacher_name": teacher_id_name[teacher], "id": teacher,
                                                 "list": teacher_course_list,
                                                 "course_num": len(day_course.get(teacher, [])),
                                                 "reserve_num": day_reserve.get(teacher, 0)}})

        return json_response(data={"list": week_day_list})

    def getCourseInfo(self, course_id):
        # 编辑时获取课程信息
        sql = f"select course.*, base.name as course_name, coursetype.name as course_type_name,classroom.name as classroom_name,courseLevel.name as course_level_name, `user`.nickname as sale_employee_name, customer.name as customer_name, business.business_name as business_name  from {self.course.__tablename__} as course left join {self.baseCourse.__tablename__} as base on course.base_course_id=base.id left join {self.courseType.__tablename__} as coursetype on base.course_type_id=coursetype.id left join {self.campusClassroom.__tablename__} as classroom on course.classroom_id=classroom.id left join {self.courseLevel.__tablename__} as courseLevel on course.course_level_id=courseLevel.id left join {self.employee.__tablename__} as employe on course.sale_employee_id=employe.id left join `user` on employe.user_id=`user`.id left join {self.customer.__tablename__} as customer on course.customer_id=customer.id left join {self.business.__tablename__} as business on course.business_id=business.id where course.id='{course_id}' "
        data = sql_execute_commit(sql)
        # 处理
        if data:
            data = data[0]
            data["material_ids"] = data["material_id"].split(",") if data["material_id"] is not None and data[
                "material_id"] != "" else []
            return data
        else:
            return {}

    def post(self):
        """新建课程(正式/试听/占用)
          ---
          tags:
            - 课程表
          parameters:
            - name: data
              in: body
              type: string
              required: true
              enum: [{"is_limit_student": 1, "base_course_id": "113eb80d79f2437fae2a0193f99e9cf7", "campus_id":"1", "classroom_id":"0abb07bbe80d44c9b90bd9071a682b28","student_ids":["1"], "course_level_id": "1", "material_id": "", "remark":"小飞测试添加", "subscript":"测试", "course_type": 1, "start_time": 1582264800, "teacher_employee_id":"3","org_id":"", "business_id":"", "customer_id":"", "start_date": 0, "end_date":0, "week_day":"","start_hour":0, "org_id": ""}]
              description: 数据体
          responses:
            200:
              description:  成功
              examples:
                response: {"message": "ok"}
        """
        data = request.get_json()
        # 批量字段
        data["create_time"] = data["update_time"] = int(time.time())
        e = ""
        # 判断是批量还是单条
        if data.get("start_date", 0) == 0:
            e = self.addCourse(data)
            db.session.commit()
        elif data.get("start_date", 0) > 0 and data.get("end_date", 0) > 0 and data.get("week_day",
                                                                                        "") != "" and data.get(
            "start_hour", 0) > 0:
            # 批量插入, 求日期中间所有的时间段
            start_time_list = self.getDateTimeList(data)
            for start in start_time_list:
                data["start_time"] = start
                e = self.addCourse(data)
                if e:
                    break
            db.session.commit()

        if e:
            return json_response(message=f"数据添加失败，{e}", status=500)
        else:
            return json_response(message="添加成功")

    def addCourse(self, data):
        # 单条插入课程方法
        updates_field = ["student_ids", "start_date", "end_date", "week_day", "start_hour"]
        data_dic = copy.copy(data)
        # 走单条新增, 删除无用字段
        for field in updates_field:
            if data_dic.get(field, -1) != -1:
                del data_dic[field]
        try:
            data_dic["id"] = generate_uuid()
            data_dic["end_time"] = data_dic["start_time"] + 3600
            field_str = ",".join(data_dic.keys())
            value_str = ",".join([f"'{val}'" for val in data_dic.values()])
            insert_sql = f"INSERT INTO {self.course.__tablename__}({field_str}) VALUE({value_str})"
            print(insert_sql)
            db.session.execute(insert_sql)
            # 插入签到表 && 只有正式课添加学员
            if len(data.get("student_ids", [])) > 0 and data["course_type"] == 1:
                insert_list = []
                for student_id in data["student_ids"]:
                    uid = generate_uuid()
                    insert_list.append(
                        f"""('{uid}','{data_dic["id"]}','{data_dic["teacher_employee_id"]}','{student_id}', 7, 2)""")
                key_str = "(`id`,course_id, teacher_id, student_id, sign_type, apply_type)"
                val_str = ",".join(insert_list)
                sign_insert_sql = f"INSERT INTO {self.courseSign.__tablename__}{key_str} VALUES {val_str}"
                print(sign_insert_sql)
                db.session.execute(sign_insert_sql)
            elif data["course_type"] == 2:
                # 试听课插入商机id
                uid = generate_uuid()
                now_time = int(time.time())
                key_str = "(`id`,course_id, teacher_id, business_id, create_time, update_time)"
                val_str = f"""('{uid}','{data_dic["id"]}','{data_dic["teacher_employee_id"]}', '{data_dic[
                    "business_id"]}', {now_time}, {now_time})"""
                sign_insert_sql = f"INSERT INTO {self.courseSign.__tablename__}{key_str} VALUES {val_str}"
                print(sign_insert_sql)
                db.session.execute(sign_insert_sql)
        except Exception as e:
            return e
        return ""

    def getDateTimeList(self, data):
        # 获取时间段内所有的课程时间
        start_time_list = []
        start_date_time = int(pendulum.from_timestamp(data["start_date"], "Asia/Shanghai").start_of("week").timestamp())
        end_date_time = int(pendulum.from_timestamp(data["end_date"], "Asia/Shanghai").end_of("week").timestamp())
        start_hour = data["start_hour"]
        while start_date_time < end_date_time:
            # 判断每周几
            for week in data["week_day"].split(","):
                start_time_list.append(start_date_time + (int(week) - 1) * 86400 + start_hour * 3600)
            start_date_time += 7 * 86400
        return start_time_list

    def delete(self):
        """删除课程
           ---
            tags:
              - 课程表
            parameters:
                - name: data
                  in: body
                  type: string
                  required: true
                  enum: [{"course_id": "","start_date": 0, "end_date":0, "week_day":"","start_hour":0, "teacher_employee_id": ""}]
                  description: 数据体
            responses:
                   status:
                     description:
                     examples:
                       response: {
                          "data": null,
                          "message": "删除成功",
                          "page": null
                        }
        """
        # 判断批量删除还是单个删除
        data = request.get_json()
        if data.get("course_id", ''):
            try:
                del_course_sql = f"""DELETE FROM {self.course.__tablename__} where id ='{data["course_id"]}'"""
                db.session.execute(del_course_sql)
                del_sign_sql = f"""DELETE FROM {self.courseSign.__tablename__} where course_id ='{data["course_id"]}'"""
                db.session.execute(del_sign_sql)
                db.session.commit()
            except Exception as e:
                return json_response(message=f"数据删除失败，{e}", status=500)
        elif data.get("start_date", 0) > 0 and data.get("end_date", 0) > 0 and data.get("week_day",
                                                                                        "") != "" and data.get(
            "start_hour", 0) > 0 and data.get("teacher_employee_id", 0) != 0:
            # 批量删除, 先查找符合条件的id
            start_time_list = self.getDateTimeList(data)
            star_time_tuple = str(tuple(start_time_list)) if len(
                start_time_list) > 1 else str(tuple(start_time_list)).replace(",", "")
            teacher_employee_id = data["teacher_employee_id"]
            # 只删除正式课
            select_sql = f"SELECT id FROM {self.course.__tablename__} WHERE teacher_employee_id='{teacher_employee_id}' and course_type=1 and start_time in {star_time_tuple}"
            res = db.session.execute(select_sql)
            course_id_list = [i["id"] for i in sql_tuple_to_dict(res.fetchall())]
            if not course_id_list:
                return json_response(message="没有需要删除的课程")
            course_id_tuple = str(tuple(course_id_list)) if len(
                course_id_list) > 1 else str(tuple(course_id_list)).replace(",", "")
            # 删除课程和学员
            del_course_sql = f"""DELETE FROM {self.course.__tablename__} where id in {course_id_tuple}"""
            del_sign_sql = f"""DELETE FROM {self.courseSign.__tablename__} where course_id in {course_id_tuple}"""
            print(del_sign_sql, del_course_sql)
            try:
                db.session.execute(del_course_sql)
                db.session.execute(del_sign_sql)
                db.session.commit()
            except Exception as e:
                return json_response(message=f"数据添加失败，{e}", status=500)
        return json_response(message="删除成功")


class EmployeeResource(Resource):
    employee = Employee()
    campus = Campus()

    @user_required
    def get(self):
        """获取销售人员列表&校区对应老师
         ---
          tags:
            - 课程表
          parameters:
           - name: types
             in: query
             type: string
             required: true
             description: 查询的数据 人员数据(list),校区对应教师(campus), 单个人员(info)
           - name: org_id
             in: query
             type: string
             required: true
             description: 组织id
          responses:
            status:
              description:
              examples:
                response: {
                  "data": {
                    "list": [
                      {
                        "campus_id": "校区id",
                        "campus_name": "校区名字",
                        "values": [
                          {
                            "campus_id": "0ed62d02491c4fb884d881c09d0f28a7",
                            "create_time": "",
                            "id": "员工id",
                            "is_teacher": 1,
                            "level": "",
                            "update_time": "",
                            "name": "",
                            "nickname": "员工名字",
                            "org_id": "b0e6ddadb16946a9adfb653a78306f14",
                            "user_id": "292f2e9299e849079404b3a1f751c477"
                          }]}]}}
        """
        user = get_current_user()

        types = request.args.get('types', "")
        org_id = request.args.get('org_id', "")
        result = []
        if types == "list":
            sql = f"select a.*, b.nickname from {self.employee.__tablename__} as a left join  `user` as b on a.user_id=b.id where a.org_id='{org_id}'"
            result = sql_execute_commit(sql)
        elif types == "campus":
            sql = f"select a.*, b.name, c.nickname from {self.employee.__tablename__} as a left join {self.campus.__tablename__} as b on a.campus_id=b.id left join `user` as c on a.user_id=c.id  where a.is_teacher=1"
            data = sql_execute_commit(sql)
            dic = {}
            for x in data:
                if dic.get(x["campus_id"], 0) == 0:
                    dic[x["campus_id"]] = []
                dic[x["campus_id"]].append(x)
            for key, value in dic.items():
                name = value[0].get("name", "")
                campus_id = value[0].get("campus_id", "")
                result.append({"campus_name": name, "campus_id": campus_id, "values": value})
        elif types == "info":
            sql = f"select * from {self.employee.__tablename__} where user_id= '{user.id}'"
            data = sql_execute_commit(sql)
            data = data[0] if data else {}
            return json_response(data=data)

        return json_response(data={"list": result})


class BaseCourseResource(Resource):
    courseType = CourseType()
    baseCourse = BaseCourse()
    baseCourseCampus = BaseCourseCampus()

    def get(self):
        """获取课程种类及对应的课程名
            ---
             tags:
               - 课程表
             parameters:
               - name: org_id
                 in: query
                 type: string
                 required: true
                 description: 组织id
               - name: campus_id
                 in: query
                 type: string
                 required: true
                 description: 校区
             responses:
               status:
                 description:
                 examples:
                   response: {
                      "data": {
                        "list": [
                          {
                            "course_type_id": null,
                            "course_type_name": null,
                            "values": [
                              {
                                "class_minutes": null,
                                "class_points": null,
                                "color": 0,
                                "course_type_id": null,
                                "course_type_name": null,
                                "create_time": null,
                                "crowd_type": null,
                                "id": "113eb80d79f2437fae2a0193f99e9cf7",
                                "instrument_type_id": null,
                                "is_cancel": null,
                                "is_enabled": 1,
                                "is_formal": null,
                                "is_other": null,
                                "update_time": null,
                                "name": "AAA",
                                "org_id": "b0e6ddadb16946a9adfb653a78306f14",
                                "student_count": null
                              }]}
                        ]
                      }
                    }
               """
        org_id = request.args.get("org_id", "")
        campus_id = request.args.get("campus_id", "")
        # 课程需要关联校区
        sql = f"select a.*, b.name as course_type_name from " \
            f" {self.baseCourse.__tablename__} as a " \
            f" left join {self.courseType.__tablename__} as b on a.course_type_id=b.id" \
            f" left join {self.baseCourseCampus.__tablename__} as base on base.base_course_id=a.id" \
            f" where a.is_enabled=1 and a.org_id='{org_id}' and b.status=1 and base.campus_id='{campus_id}'"
        data = sql_execute_commit(sql)
        dic = {}
        for x in data:
            if dic.get(x["course_type_id"], 0) == 0:
                dic[x["course_type_id"]] = []
            dic[x["course_type_id"]].append(x)
        result = []
        for key, value in dic.items():
            course_type_name = value[0].get("course_type_name", "")
            course_type_id = value[0].get("course_type_id", "")
            result.append({"course_type_name": course_type_name, "course_type_id": course_type_id, "values": value})

        return json_response(data={"list": result})


class InstrumentTypeResource(Resource):
    def get(self):
        """获取乐器类型筛选列表
                ---
                 tags:
                   - 课程表
                 responses:
                   status:
                     description:
                     examples:
                       response: {
                          "data": {
                            "list": [
                              {
                                "id": "1",
                                "name": "钢琴"
                              }
                            ]
                          }
                        }
               """
        data = InstrumentType.query.filter().all()
        res = []
        for val in data:
            res.append({"id": val.id, "name": val.name})

        return json_response(data={"list": res})


class CampusClassroomResource(Resource):
    campusClassroom = CampusClassroom()
    campus = Campus()

    def get(self):
        """获取校区及对应的教室
            ---
            tags:
               - 课程表
            parameters:
               - name: org_id
                 in: query
                 type: string
                 required: true
                 description: 组织id
               - name: campus_id
                 in: query
                 type: string
                 required: true
                 description: 校区id
            responses:
               status:
                 description:
                 examples:
                   response: {
                      "data": {
                        "list": [
                           {
                            "campus_id": "1",
                            "campus_name": "上地校区",
                            "values": [
                              {
                                "campus_id": "1",
                                "campus_name": "上地校区",
                                "create_time": null,
                                "id": "0abb07bbe80d44c9b90bd9071a682b28",
                                "is_enabled": 1,
                                "update_time": null,
                                "name": "手动方式1",
                                "org_id": "b0e6ddadb16946a9adfb653a78306f14"
                              }]}
                        ]
                      }
                    }
        """
        org_id = request.args.get("org_id", "")
        sql = f"select a.*, b.name as campus_name  from {self.campusClassroom.__tablename__} as a left join {self.campus.__tablename__} " \
            f" as b on a.campus_id=b.id   where a.is_enabled=1 and a.org_id='{org_id}' and b.org_id='{org_id}'"
        campus_id = request.args.get("campus_id", "")
        if campus_id != "":
            sql += f" and campus_id='{campus_id}'"
        data = sql_execute_commit(sql)
        dic = {}
        for x in data:
            if dic.get(x["campus_id"], 0) == 0:
                dic[x["campus_id"]] = []
            dic[x["campus_id"]].append(x)
        result = []
        for key, value in dic.items():
            campus_name = value[0].get("campus_name", "")
            campus_id = value[0].get("campus_id", "")
            result.append({"campus_name": campus_name, "campus_id": campus_id, "values": value})

        return json_response(data={"list": result})


class StudentResource(Resource):
    student = Student()

    def get(self):
        """学员列表查询
           ---
            tags:
              - 课程表
            parameters:
               - name: name
                 in: query
                 type: string
                 required: false
                 description: 学员名
               - name: org_id
                 in: query
                 type: string
                 required: true
                 description: 组织id
            responses:
                   status:
                     description:
                     examples:
                       response: {
                          "data": {
                            "list": [
                              {
                                "id": "1",
                                "name": "小飞"
                              }
                            ]
                          }
                        }
        """
        org_id = request.args.get("org_id", "")
        query = f"org_id='{org_id}'"
        name = request.args.get('name', "")
        if name != "":
            query += f" and `name` like '%{name}%'"
        sql = f"select * from {self.student.__tablename__} where {query}"
        data = sql_execute_commit(sql)
        return json_response(data={"list": data})


class CourseLevelResource(Resource):
    courseLevel = CourseLevel()

    def get(self):
        """课程等级查询
           ---
            tags:
              - 课程表
            responses:
               status:
                 description:
                 examples:
                   response: {
                      "data": {
                        "list": [
                          {
                            "id": "1",
                            "name": "低"
                          }
                        ]
                      },
                      "message": null,
                      "page": null
                    }
        """
        data = CourseLevel.query.filter().all()
        res = []
        for val in data:
            res.append({"id": val.id, "name": val.name})

        return json_response(data={"list": res})


class EssentialResource(Resource):
    essential = Essential()

    def getEssentialInfo(self, essential_ids: list) -> dict:
        # 获取要点信息
        essential_ids_str = str(tuple(essential_ids)) if len(essential_ids) > 1 else str(tuple(essential_ids)).replace(
            ",", "")
        sql = f"select * from {self.essential.__tablename__} where `id` in {essential_ids_str}"
        data = sql_execute_commit(sql)
        res = {}
        for val in data:
            res[val["id"]] = val
        return res


class SubjectResource(Resource):
    subject = Subject()
    essential = Essential()
    subjectEssential = SubjectEssential()

    def getSubjectInfo(self, subject_ids: list) -> dict:
        # 获取课程信息
        subject_ids_str = str(tuple(subject_ids)) if len(subject_ids) > 1 else str(tuple(subject_ids)).replace(",",
                                                                                                               "")
        sql = f"select * from {self.subject.__tablename__} where `id` in {subject_ids_str}"
        data = sql_execute_commit(sql)
        res = {}
        for val in data:
            res[val["id"]] = val
        return res

    def getSubjectEssentialList(self, subject_ids: list):
        # 获取课程和主题的对应关系
        subject_ids_str = str(tuple(subject_ids)) if len(subject_ids) > 1 else str(tuple(subject_ids)).replace(",",
                                                                                                               "")
        sql = f"select a.id as subject_id, a.name as subject_name, c.id as essential_id, c.name as essential_name from {self.subject.__tablename__} as a left join {self.subjectEssential.__tablename__} as b on a.id=b.subject_id left join {self.essential.__tablename__} as c on b.essential_id=c.id where subject_id in {subject_ids_str}"
        data = sql_execute_commit(sql)
        dic = {}
        for x in data:
            if dic.get(x["subject_id"], 0) == 0:
                dic[x["subject_id"]] = []
            dic[x["subject_id"]].append(x)
        result = []
        for key, value in dic.items():
            subject_name = value[0].get("subject_name", "")
            subject_id = value[0].get("subject_id", "")
            result.append({"subject_name": subject_name, "subject_id": subject_id, "values": value})
        return result


class CustomerResource(Resource):
    customer = Customer()
    business = Business()

    def get(self):
        """客户商机查询
           ---
            tags:
               - 课程表
            parameters:
               - name: name
                 in: query
                 type: string
                 required: true
                 description: 客户名
               - name: phone
                 in: query
                 type: string
                 required: true
                 description: 客户手机号
               - name: org_id
                 in: query
                 type: string
                 required: true
                 description: 组织id
            responses:
               status:
                 description:
                 examples:
                   response: {
                      "data": {
                        "list": [
                          {
                            "customer_id": "1",
                            "customer_name": "小飞",
                            "values": [
                              {
                                "ages": null,
                                "business_id": "10010",
                                "business_name": "商机1",
                                "business_type": 1,
                                "campus_id": null,
                                "color": null,
                                "connect_employee_id": null,
                                "create_time": null,
                                "current_packet_id": null,
                                "has_arrived": null,
                                "has_basis": null,
                                "id": "1",
                                "instrument_type_id": null,
                                "intention": null,
                                "update_time": null,
                                "name": "小飞",
                                "org_id": null,
                                "phone": null,
                                "recommend_employee_id": null,
                                "remark": "测试",
                                "sex": null,
                                "source": null,
                                "status": null
                              }
                            ]
                          }
                        ]
                      },
                      "message": null,
                      "page": null
                    }
            """
        name = request.args.get('name', "")
        phone = request.args.get('phone', "")
        org_id = request.args.get("org_id", "")
        query = f"a.org_id='{org_id}'"
        if name != "" and phone != "":
            query += f" and a.`name` like '%{name}%' or a.`phone` like '%{phone}%'"
        elif name != "":
            query += f" and a.`name` like '%{name}%'"
        elif phone != "":
            query += f" and a.`phone` like '%{phone}%'"
        sql = f"select a.*, b.business_name, b.business_type, b.id as business_id from {self.customer.__tablename__} as a left join {self.business.__tablename__} as b on a.id=b.customer_id where {query}"
        print(sql)
        data = sql_execute_commit(sql)
        # 获取对应关系
        dic = {}
        for x in data:
            if dic.get(x["id"], 0) == 0:
                dic[x["id"]] = []
            dic[x["id"]].append(x)
        result = []
        for key, value in dic.items():
            customer_name = value[0].get("name", "")
            customer_id = value[0].get("id", "")
            result.append({"customer_name": customer_name, "customer_id": customer_id, "values": value})
        return json_response(data={"list": result})


class PacketResource(Resource):
    packet = Packet()
    packetSubject = PacketSubject()

    def getPacketInfo(self, packet_id):
        # 获取套餐信息
        query = "1=1" if packet_id == "" else f"a.id='{packet_id}'"
        sql = f"select a.*, b.subject_id from {self.packet.__tablename__} as a left join {self.packetSubject.__tablename__} as b on a.id=b.packet_id where {query}"
        data = sql_execute_commit(sql)
        return data


class CourseSignResource(Resource):
    courseSign = CourseSign()
    student = Student()
    business = Business()
    subjectResource = SubjectResource()
    essentialResource = EssentialResource()
    packetResource = PacketResource()
    studentLevel = StudentLevel()
    customer = Customer()
    course = Course()

    def get(self):
        """获取课程报名学员及状态&历史签到记录&学生详情签到记录
        ---
        tags:
          - 课程表
        parameters:
           - name: course_id
             in: query
             type: string
             required: false
             description: 课程id
           - name: student_id
             in: query
             type: string
             required: false
             description: 学生id
           - name: types
             in: query
             type: string
             required: true
             description: 请求类型 课程报名学员及状态(list), 学生历史签到记录(history_list), 学生详情签到记录(sign_list)

        responses:
           status:
             description:
             examples:
               response: {
                  "data": {
                    "list": [
                    ]
                  },
                  "message": null,
                  "page": null
                }
        """
        course_id = request.args.get('course_id', "")
        student_id = request.args.get('student_id', "")
        types = request.args.get('types', "")
        if types == "history_list":
            return json_response(data=self.getHistoryList(course_id, student_id))
        elif types == "sign_list":
            return json_response(data=self.getSignList(student_id))

        sql = f"select a.*, b.name as student_name, b.is_teach_plan, c.name as customer_name, course.course_type from {self.courseSign.__tablename__} as a left join {self.student.__tablename__} as b on a.student_id=b.id left join {self.course.__tablename__} as course on a.course_id=course.id left join {self.customer.__tablename__} as c on course.customer_id=c.id where a.course_id='{course_id}'"
        res = db.session.execute(sql)
        data = res.fetchall()
        # 转换
        data = sql_tuple_to_dict(data)
        db.session.commit()
        for x in data:
            x["sign_type_str"] = self.courseSign.sign_type_enum.get(x["sign_type"], "")
            # 试听课用客户名字
            if x["course_type"] == 2:
                x["student_name"] = x["customer_name"]
        return json_response({"list": data, "course_sign_type": self.courseSign.course_sign_type})

    def getHistoryList(self, course_id, student_id):
        # 获取历史签到
        sql = f"select sign.*, leve.name as level_name, leve.id as level_id, course.start_time " \
            f" from {self.courseSign.__tablename__} as sign " \
            f" left join {self.course.__tablename__} as course on sign.course_id=course.id " \
            f" left join {self.student.__tablename__} as student on sign.student_id=student.id " \
            f" left join {self.studentLevel.__tablename__} as leve on student.level_id=leve.id  " \
            f" where sign.course_id='{course_id}' and sign.student_id='{student_id}' order by sign.create_time desc"
        data = sql_execute_commit(sql)
        if data:
            return self.getHistortParse(data[0], student_id)
        return {}

    def getSignList(self, student_id):
        # 获取历史签到
        sql = f"select sign.*, leve.name as level_name, leve.id as level_id, course.start_time " \
            f" from {self.courseSign.__tablename__} as sign " \
            f" left join {self.course.__tablename__} as course on sign.course_id=course.id " \
            f" left join {self.student.__tablename__} as student on sign.student_id=student.id " \
            f" left join {self.studentLevel.__tablename__} as leve on student.level_id=leve.id  " \
            f" where sign.student_id='{student_id}' order by sign.create_time desc"
        data = sql_execute_commit(sql)
        sign_list = []
        for val in data:
            sign_list.append(self.getHistortParse(val, student_id))
        return {"sign_list": sign_list}

    def getHistortParse(self, data, student_id):
        if data.get("subject_essential_info", ""):
            subject_essential_info = eval(data["subject_essential_info"])
            # [{"主题id": "", values:[{"要点id":"", "status": 1}]}]
            # 获取主题名和要点名
            subject_ids = [i["subject_id"] for i in subject_essential_info]
            essential_ids = [j["essential_id"] for i in subject_essential_info for j in i["values"]]
            subject_name_dic = self.subjectResource.getSubjectInfo(subject_ids)
            essential_name_dic = self.essentialResource.getEssentialInfo(essential_ids)
            for subject in subject_essential_info:
                subject["subject_name"] = subject_name_dic.get(subject["subject_id"], "").get("name", "")
                for essential in subject["values"]:
                    essential["essential_name"] = essential_name_dic.get(essential["essential_id"], "").get("name", "")
                    essential["status"] = int(essential["status"])
        else:
            # 查询学生详情
            student_info = Student.query.filter(Student.id == student_id).first()
            # 获取学生对应的套餐主题
            subject = self.packetResource.getPacketInfo(student_info.current_packet_id)
            if not subject:
                return {}
            # 获取该学员对应的主题和要点
            subject_ids = [i["subject_id"] for i in subject]
            subject_essential_info = self.subjectResource.getSubjectEssentialList(subject_ids)
            # 添加默认的百分比和完成状态
            for subject_info in subject_essential_info:
                subject_info["percentage"] = "0"
                for essential_info in subject_info["values"]:
                    essential_info["status"] = 1
        # 拼接历史记录时间
        localtime = time.localtime(data["start_time"])
        start_hour = localtime.tm_hour
        history_sign_time = f'{time.strftime("%Y年%m月%d日", localtime)} {start_hour}:00-{start_hour + 1}:00课程的签到记录'
        return {"list": subject_essential_info, "student_info": data, "history_sign_time": history_sign_time}

    def post(self):
        """报名学生状态更改(正式/试听/占用)
          ---
          tags:
            - 课程表
          parameters:
            - name: data
              in: body
              type: string
              required: true
              enum: [{"id": "f900876963d546b1b3c11fab423d7730", "sign_type": 1, "course_type":1, "material_id": "素材id,多个分隔", "student_remark":"学生备注","teacher_remark":"老师备注", "subject_essential_info":"正式签到json串", "subject_remark":"主题要点", "subject_id":"主题id", "sign_student_level_id":"学生等级", "business_status":"试听状态"}]
              description: 数据体
          responses:
            200:
              description:  成功
              examples:
                response: {"message": "ok"}
        """
        data = request.get_json()
        if data.get("id", "") == "" or data.get("sign_type", "") == "" or data.get("course_type", "") == "":
            return json_response(message="没有数据id", status=400)
        # 获取数据信息
        signData = CourseSign.query.filter(CourseSign.id == data["id"]).first()

        # 需要更新的数据字段
        fields = ["material_id", "student_remark", "teacher_remark", "sign_type", "subject_remark",
                  "sign_student_level_id"]

        # 如果是正式课,
        if data.get("course_type", 0) == 1:
            # 查询学生详情
            student_info = Student.query.filter(Student.id == signData.student_id).first()
            # 判断是否为体系课签到
            if student_info.is_teach_plan == 1 and data["sign_type"] == 1:
                # 主题签到情况为一个json串
                fields.append("subject_essential_info")
                data["subject_essential_info"] = f'{data["subject_essential_info"]}'
        elif data.get("course_type", 0) == 2:
            # 试听课逻辑, 判断签到类型
            if data["sign_type"] != 1:
                #  非签到需要判断之前是否签到
                if signData.sign_type == 4:
                    # 之前是签到, 需要删除商机表的同步字段
                    update_business_sql = f"""update {self.business.__tablename__} set business_status=0, remark='' where id='{
                    signData.business_id}'"""
                    print(update_business_sql)
                    db.session.execute(update_business_sql)
            else:
                # 签到需要同步商机表
                update_business_sql = f"""update {self.business.__tablename__} set business_status={data[
                    "business_status"]}, remark='{data["teacher_remark"]}' where id='{
                signData.business_id}'"""
                print(update_business_sql)
                db.session.execute(update_business_sql)

        # 签到修改签到表
        sign_dic = ",".join([f"""{i}="{data.get(i, '')}" """ for i in fields])
        update_sql = f"""update {self.courseSign.__tablename__} set {sign_dic} where id='{data["id"]}'"""
        print(update_sql)
        db.session.execute(update_sql)
        db.session.commit()
        return json_response(data={}, message="成功")

    def getStudentsSignTotal(self, student_ids: list) -> dict:
        student_ids_str = str(tuple(student_ids)) if len(student_ids) > 1 else str(tuple(student_ids)).replace(",",
                                                                                                               "")
        sql = f"select count(1) as total, student_id from {self.subject.__tablename__} where sign_type=1 and student_id in {student_ids_str}"
        data = sql_execute_commit(sql)
        res = {}
        for val in data:
            res[val["student_id"]] = val["total"]
        return res


class StudentLevelResource(Resource):
    def get(self):
        """获取学员等级筛选列表
                ---
                 tags:
                   - 课程表
                 responses:
                   status:
                     description:
                     examples:
                       response: {
                          "data": {
                            "list": [
                              {
                                "id": "1",
                                "name": "钢琴"
                              }
                            ]
                          }
                        }
               """
        data = StudentLevel.query.filter().all()
        res = []
        for val in data:
            res.append({"id": val.id, "name": val.name})

        return json_response(data={"list": res})


class CourseTypeResource(Resource):
    def get(self):
        """课程类型筛选项
                ---
                 tags:
                   - 课程表
                 responses:
                   status:
                     description:
                     examples:
                       response: {
                          "data": {
                            "list": [
                              {
                                "id": "1",
                                "name": "钢琴"
                              }
                            ]
                          }
                        }
               """
        data = CourseType.query.filter().all()
        res = []
        for val in data:
            res.append({"id": val.id, "name": val.name})

        return json_response(data={"list": res})


class StudentDetailResource(Resource):
    student = Student()
    commonResource = CommonResource()
    studentRemark = StudentRemark()
    campus = Campus()
    studentLevel = StudentLevel()
    packet = Packet()
    instrumentType = InstrumentType()
    instrumentUse = InstrumentUse()
    employee = Employee()

    def get(self):
        """学员详情-学员信息
            ---
            tags:
              - 课程表
            parameters:
               - name: student_id
                 in: query
                 type: string
                 required: false
                 description: 学生id
            responses:
               status:
                 description:
                 examples:
                   response: {
                      "data": {
                      },
                      "message": null,
                      "page": null
                    }
            """
        query = "1=1"
        student_id = request.args.get('student_id', "")
        if student_id != "":
            query += f" and student.`id` = {student_id} "
        sql = f"select student.*, campus.name as campus_name, u.nickname as teacher_name, leve.name as level_name, " \
            f" packet.name as packet_name, type1.name as instrument_name, `use`.name as instrument_use_name" \
            f" from {self.student.__tablename__} as student" \
            f" left join {self.campus.__tablename__} as campus on student.campus_id=campus.id" \
            f" left join {self.employee.__tablename__} as emp on student.teacher_id=emp.id " \
            f" left join `user` as u on emp.user_id=u.id" \
            f" left join {self.studentLevel.__tablename__} as leve on student.level_id=leve.id " \
            f" left join {self.packet.__tablename__} as packet on student.current_packet_id=packet.id" \
            f" left join {self.instrumentType.__tablename__} as type1 on type1.id=student.instrument_type_id" \
            f" left join {self.instrumentUse.__tablename__} as `use` on `use`.id=student.instrument_use_id" \
            f" where {query}"
        data = sql_execute_commit(sql)
        if data:
            res_data = data[0]
            # 学员能力值(即主题列表)
            res_data["able"] = self.commonResource.getStudentAble(res_data.get("current_packet_id", ""))
            # 学员/教师备注
            remark_sql = f"select remark.*, u.nickname as teacher_name, student.name as student_name " \
                f" from {self.studentRemark.__tablename__} as remark" \
                f" left join {self.employee.__tablename__} as emp on remark.teacher_id=emp.id " \
                f" left join `user` as u on emp.user_id=u.id " \
                f" left join {self.student.__tablename__} as student on student.id=remark.student_id" \
                f" where student_id='{student_id}' order by create_time desc"
            res_data["remark_list"] = sql_execute_commit(remark_sql)
            # 学习进度
            learn_number = self.commonResource.getStudentLearn(student_id)
            res_data["last_learn_hour"] = res_data["all_class_hours"] - learn_number
            res_data["learn_hour"] = learn_number
            # 日志 --先不做
            res_data["log_list"] = {}
            # 剩余时间计算
            res_data["last_day"] = (
                pendulum.from_timestamp(res_data["end_time"], "Asia/Shanghai") - pendulum.now()).days
        else:
            res_data = {}

        return json_response(data=res_data)

    def post(self):
        """学员详情-学员信息修改
            ---
            tags:
              - 课程表
            parameters:
                - name: data
                  in: body
                  type: string
                  required: true
                  enum: [{"student_id": "1"}]
                  description: 数据体
            responses:
               status:
                 description:
                 examples:
                   response: {
                      "data": {
                      },
                      "message": null,
                      "page": null
                    }
            """
        data = request.get_json()
        student_id = data.get("student_id", "")
        del data["student_id"]
        if student_id == "":
            return json_response(data={}, message="没有学员信息", status=500)
        data["update_time"] = int(time.time())
        value_str = ",".join([f"{k}='{v}'" for k, v in data.items()])
        sql = f"update {self.student.__tablename__} set {value_str} where id='{student_id}'"
        db.session.execute(sql)
        db.session.commit()
        return json_response(data={}, message="修改成功")


class StudentCourseResource(Resource):
    courseSign = CourseSign()
    student = Student()
    studentLevel = StudentLevel()
    # customer = Customer()
    course = Course()
    courseType = CourseType()

    def get(self):
        """学员详情-课程记录
            ---
            tags:
              - 课程表
            parameters:
               - name: student_id
                 in: query
                 type: string
                 required: true
                 description: 学员id
               - name: sign_student_level_id
                 in: query
                 type: string
                 required: false
                 description: 学员约课等级
               - name: student_level_id
                 in: query
                 type: string
                 required: false
                 description: 学员等级
               - name: course_type_id
                 in: query
                 type: string
                 required: false
                 description: 课程类型
               - name: campus_id
                 in: query
                 type: string
                 required: false
                 description: 校区
               - name: teacher_id
                 in: query
                 type: string
                 required: false
                 description: 老师id
               - name: sign_type
                 in: query
                 type: string
                 required: false
                 description: 签到类型
            responses:
               status:
                 description:
                 examples:
                   response: {
                      "data": {
                        "list": [
                        ]
                      },
                      "message": null,
                      "page": null
                    }
            """
        student_id = request.args.get('student_id', "")
        sign_student_level_id = request.args.get('sign_student_level_id', "")  # 学员约课等级
        student_level_id = request.args.get('student_level_id', "")  # 学员等级
        course_type_id = request.args.get("course_type_id", "")  # 课程类型
        campus_id = request.args.get("campus_id", "")
        teacher_id = request.args.get("teacher_id", "")
        sign_type = int(request.args.get("sign_type", 0))
        query = ""
        query += f" and sign.sign_student_level_id='{sign_student_level_id}' " if sign_student_level_id != "" else ""
        query += f" and student.level_id='{student_level_id}' " if student_level_id != "" else ""
        query += f" and base_course.course_type_id='{course_type_id}' " if course_type_id != "" else ""
        query += f" and course.campus_id='{campus_id}' " if campus_id != "" else ""
        query += f" and course.teacher_employee_id='{teacher_id}' " if teacher_id != "" else ""
        query += f" and sign.sign_type={sign_type} " if sign_type != 0 else ""

        # 课程记录(以签到表为准)
        # sql = f" select sign.*, leve.name as level_name, leve.id as level_id, course.start_time from {self.courseSign.__tablename__} as sign left join {self.course.__tablename__} as course on sign.course_id=course.id left join {self.student.__tablename__} as student on sign.student_id=student.id left join {self.studentLevel.__tablename__} as leve on student.level_id=leve.id  where sign.student_id='{student_id}' order by sign.create_time desc "
        sql = '''
    select sign.create_time,sign.sign_student_level_id,sign.sign_type,sign.student_remark,sign.teacher_remark
    ,leve2.name as sign_level_name, sign.id, course.id as course_id, course.teacher_employee_id
    ,course.start_time,base_course.`name` as course_name, sign.apply_type
    ,course.campus_id,course.classroom_id,base_course.course_type_id,courseType.name as course_type_name
    ,campus.name as campus_name
    ,classroom.name as classroom_name
    ,`user`.`name` as teacher_name
    ,student.name as student_name,student.phone,student.all_class_hours
    ,leve.id as level_id,leve.name as level_name
    from edu_course_sign as sign
    left join edu_course as course on sign.course_id=course.id
    left join edu_base_course as base_course on base_course.id = course.base_course_id
    left join edu_student as student on sign.student_id=student.id
    left join edu_student_level as leve on student.level_id=leve.id
    left join edu_student_level as leve2 on sign.sign_student_level_id=leve2.id
    left join edu_employee as employee on employee.id = course.teacher_employee_id
    left join `user` on `user`.id = employee.user_id
    left join edu_campus as campus on campus.id = course.campus_id
    left join edu_campus_classroom as classroom on classroom.id = course.classroom_id
    left join edu_course_type as courseType on courseType.id = base_course.course_type_id
    where sign.student_id= '%s' and course.course_type=1 %s
    order by sign.create_time desc
'''
        data = sql_execute_commit(sql % (student_id, query))
        # 获取学员正式课签到次数
        learn_sql = f"select count(1) as total from {self.courseSign.__tablename__} where sign_type=1 and student_id='{student_id}'"
        learn = sql_execute_commit(learn_sql)
        # 上课次数时长
        learn_number = 0 if not learn else learn[0].get("total", 0)
        for val in data:
            # 剩余课时
            val["last_learn_hour"] = val["all_class_hours"] - learn_number
            # 约课方式
            val["apply_type_str"] = self.courseSign.apply_type_enum.get(val["apply_type"], "")
        return json_response(data={"list": data})


class OrderResource(Resource):
    order = Order()
    campus = Campus()
    employee = Employee()
    student = Student()
    instrumentType = InstrumentType()

    def get(self):
        """学员详情-消费记录
            ---
             tags:
               - 课程表
             parameters:
               - name: student_id
                 in: query
                 type: string
                 required: true
             responses:
               status:
                 description:
                 examples:
                   response: {
                      "data": {
                      }
                    }
           """
        student_id = request.args.get("student_id", "")
        sql = f"select ord.*,campus.name as campus_name, user1.name as audition_teacher_name," \
            f" user2.name as sale_name, type1.name as instrument_name, student.name as student_name, " \
            f"student.phone as student_phone," \
            f"student.sex as student_sex " \
            f" from {self.student.__tablename__} as student" \
            f" left join {self.order.__tablename__} as ord on student.order_id=ord.id" \
            f" left join {self.campus.__tablename__} as campus on ord.campus_id=campus.id" \
            f" left join {self.employee.__tablename__} as employee on ord.audition_teacher_employee_id=employee.id" \
            f" left join {self.employee.__tablename__} as employee2 on ord.sale_employee_id=employee2.id" \
            f" left join `user` as user1 on employee.user_id=user1.id" \
            f" left join `user` as user2 on employee2.user_id=user2.id" \
            f" left join {self.instrumentType.__tablename__} as type1 on  student.instrument_type_id=type1.id" \
            f" where student.id = '{student_id}'"
        data = sql_execute_commit(sql)
        data = data[0] if data else {}
        if data:
            # 字段对应
            data["pay_type_str"] = self.order.pay_type_enum.get(data["pay_type"], "")
            data["status_str"] = self.order.status_enum.get(data["status"], "")
            data["order_type_str"] = self.order.order_type_enum.get(data["order_type"], "")
            data["price"] = float(data["price"])
            data["student_sex_str"] = self.student.sex_enum.get(data["student_sex"], "")
        return data


class UserHistoryResource(Resource):

    @user_required
    def get(self):
        """获取用户上次搜索历史
           ---
            tags:
              - 课程表
            responses:
              status:
                description:
                examples:
                  response: {
                   }
          """
        user = get_current_user()
        data = redis_0.hget(redis_key["user_select_history"], user.id)
        if data is not None:
            return json_response(data=eval(str(data, "utf8")))
        else:
            return json_response(data={})


class StudentRemarkResource(Resource):
    studentRemark = StudentRemark()

    def post(self):
        """学员详情-老师学生备注添加
            ---
            tags:
              - 课程表
            parameters:
                - name: data
                  in: body
                  type: string
                  required: true
                  enum: [{"student_id": "1", "remark_type":1, "remark":"学生备注"}]
                  description: 数据体
            responses:
               status:
                 description:
                 examples:
                   response: {
                      "data": {
                      },
                      "message": null,
                      "page": null
                    }
            """
        inser_dic = request.get_json()
        student_id = inser_dic.get("student_id", "")
        if student_id == "":
            return json_response(data={}, message="没有学员信息", status=500)
        inser_dic["create_time"] = inser_dic["update_time"] = int(time.time())
        inser_dic["id"] = generate_uuid()
        field_str = ",".join(inser_dic.keys())
        value_str = ",".join([f"'{val}'" for val in inser_dic.values()])
        insert_sql = f"INSERT INTO {self.studentRemark.__tablename__}({field_str}) VALUE({value_str})"
        db.session.execute(insert_sql)
        db.session.commit()
        return json_response(data={}, message="新增成功")


class InstrumentUseResource(Resource):
    instrumentUse = InstrumentUse()

    def get(self):
        """乐器使用情况列表
           ---
            tags:
              - 课程表
            parameters:
               - name: teacher_employee_id
                 in: query
                 type: string
                 required: true
                 description: 老师id
            responses:
               status:
                 description:
                 examples:
                   response: {
                      "data": {
                        "list": [
                          {
                            "id": "1",
                            "name": "素材1"
                          }
                        ]
                      },
                      "message": null,
                      "page": null
                    }
        """
        teacher_employee_id = request.args.get('teacher_employee_id', "")
        org_id = request.args.get('org_id', "")
        if teacher_employee_id != "" and org_id != "":
            data = InstrumentUse.query.filter(InstrumentUse.teacher_id == teacher_employee_id).all()
        else:
            data = InstrumentUse.query.filter().all()
        res = []
        for val in data:
            res.append({"id": val.id, "name": val.name})

        return json_response(data={"list": res})
