export default (request) => {
  return {
    getCampus: (types, org_id) => request({
      url: `/edu/employee?types=${types}&org_id=${org_id}`,
      method: 'get',
    }),
    getInstrumentType: (org_id) => request({
      url: `/edu/instrumentType?org_id=${org_id}`,
      method: 'get',
    }),
    getCourse: (org_id ,campusId, teacherEmployeeId, instrumentTypeId, startTime) => request({
      url: `/edu/course?campus_id=${campusId}&org_id=${org_id}&teacher_employee_id=${teacherEmployeeId}&instrument_type_id=${instrumentTypeId}&start_time=${startTime}`,
      method: 'get',
    }),
    getEditAudition: (org_id, course_id, types) => request({
      url: `/edu/course?course_id=${course_id}&types=${types}&org_id=${org_id}`,
      method: 'get',
    }),
    curriculum: (data) => request({
      url: `/edu/course`,
      method: 'post',
      data
    }),
    getCustomer: (name, phone, org_id) => request({
      url: `/edu/customer?phone=${phone}&name=${name}&org_id=${org_id}`,
      method: 'get',
    }),
    campusClassroom: (org_id, campus_id) => request({
      url: `/edu/campusClassroom?campus_id=${campus_id}&org_id=${org_id}`,
      method: 'get',
    }),
    baseCourse: (org_id, campus_id) => request({
      url: `/edu/baseCourse?org_id=${org_id}&campus_id=${campus_id}`,
      method: 'get',
    }),
    courseLevel: (org_id) => request({
      url: `/edu/courseLevel?org_id=${org_id}`,
      method: 'get',
    }),
    material: (org_id, teacherEmployeeId) => request({
      url: `/edu/material?teacherEmployeeId=${teacherEmployeeId}&org_id=${org_id}`,
      method: 'get',
    }),
    student: (org_id, name) => request({
      url: `/edu/student?name=${name}&org_id=${org_id}`,
      method: 'get',
    }),
    deleteCourse: (data) => request({
      url: `/edu/course`,
      method: 'delete',
      data
    }),
    courseSign: (org_id, course_id) => request({
      url: `/edu/courseSign?course_id=${course_id}&org_id=${org_id}`,
      method: 'get',
    }),
    getClassSign: (data) => request({
      url: `/edu/courseSign`,
      method: 'post',
      data
    }),
    getCourseSignList: (student_id, types, org_id) => request({
      url: `/edu/courseSign?student_id=${student_id}&types=${types}&org_id=${org_id}`,
      method: 'get',
    }),
    getCourseSignLists: (org_id, course_id, student_id, types) => request({
      url: `/edu/courseSign?org_id=${org_id}&course_id=${course_id}&student_id=${student_id}&types=${types}`,
      method: 'get',
    }),
    studentLevel: (org_id) => request({
      url: `/edu/studentLevel?org_id=${org_id}`,
      method: 'get',
    }),
    studentDetail: (student_id) => request({
      url: `/edu/studentDetail?student_id=${student_id}`,
      method: 'get',
    }),
    studentCourse: (student_id, sign_student_level_id, student_level_id, course_type_id, teacher_id, sign_type) => request({
      url: `/edu/studentCourse?student_id=${student_id}&sign_student_level_id=${sign_student_level_id}&student_level_id=${student_level_id}&course_type_id=${course_type_id}&teacher_id=${teacher_id}&sign_type=${sign_type}`,
      method: 'get',
    }),
    getOrder: (student_id) => request({
      url: `/edu/order?student_id=${student_id}`,
      method: 'get',
    }),
    userHistory: () => request({
      url: `/edu/userHistory`,
      method: 'get',
    }),
    studentRemark: (data) => request({
      url: `/edu/studentRemark`,
      method: 'post',
      data
    }),
    studentUpdate: (data) => request({
      url: `/edu/studentDetail`,
      method: 'post',
      data
    }),
    instrumentUse: (teacher_employee_id) => request({
      url: `/edu/instrumentUse?teacher_employee_id=${teacher_employee_id}`,
      method: 'get',
    }),
  }
}
