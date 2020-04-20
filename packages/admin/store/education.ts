import { VuexModule, Action, Module } from 'vuex-module-decorators';
import { service } from '~/utils'

@Module({
  name: 'education',
  stateFactory: true,
  namespaced: true,
})
class Education extends VuexModule {
  @Action({ rawError: true })
  public getCampus({types, org_id}) {
    return service.education.getCampus(types, org_id)
  }
  @Action({ rawError: true })
  public getInstrumentType({org_id}) {
    return service.education.getInstrumentType(org_id)
  }
  @Action({ rawError: true })
  public getCourse({org_id, campusId, teacherEmployeeId, instrumentTypeId, startTime}) {
    return service.education.getCourse(org_id, campusId, teacherEmployeeId, instrumentTypeId, startTime)
  }
  @Action({ rawError: true })
  public getEditAudition({org_id, course_id, types}) {
    return service.education.getEditAudition(org_id, course_id, types)
  }

  @Action({ rawError: true })
  public curriculum(data) {
    return service.education.curriculum(data)
  }
  @Action({ rawError: true })
  public getCustomer({name, phone, org_id}) {
    return service.education.getCustomer(name, phone, org_id)
  }
  @Action({ rawError: true })
  public campusClassroom({org_id, campus_id}) {
    return service.education.campusClassroom(org_id, campus_id)
  }
  @Action({ rawError: true })
  public baseCourse({ org_id, campus_id }) {
    return service.education.baseCourse(org_id, campus_id)
  }
  @Action({ rawError: true })
  public courseLevel({org_id}) {
    return service.education.courseLevel(org_id)
  }
  @Action({ rawError: true })
  public material({org_id ,teacherEmployeeId}) {
    return service.education.material(org_id ,teacherEmployeeId)
  }
  @Action({ rawError: true })
  public student({org_id, name}) {
    return service.education.student(org_id, name)
  }
  @Action({ rawError: true })
  public deleteCourse(data) {
    return service.education.deleteCourse(data)
  }
  @Action({ rawError: true })
  public courseSign({org_id, course_id}) {
    return service.education.courseSign(org_id, course_id)
  }
  @Action({ rawError: true })
  public getClassSign(data) {
    return service.education.getClassSign(data)
  }
  @Action({ rawError: true })
  public getCourseSignList({student_id, types, org_id}) {
    return service.education.getCourseSignList(student_id, types, org_id)
  }
  @Action({ rawError: true })
  public getCourseSignLists({org_id, course_id, student_id, types}) {
    return service.education.getCourseSignLists(org_id, course_id, student_id, types)
  }

  @Action({ rawError: true })
  public studentLevel({org_id}) {
    return service.education.studentLevel(org_id)
  }
  @Action({ rawError: true })
  public studentDetail({student_id}) {
    return service.education.studentDetail(student_id)
  }
  @Action({ rawError: true })
  public studentCourse({student_id, sign_student_level_id, student_level_id, course_type_id, teacher_id, sign_type}) {
    return service.education.studentCourse(student_id, sign_student_level_id, student_level_id, course_type_id, teacher_id, sign_type)
  }
  @Action({ rawError: true })
  public getOrder({student_id}) {
    return service.education.getOrder(student_id)
  }
  @Action({ rawError: true })
  public userHistory() {
    return service.education.userHistory()
  }
  @Action({ rawError: true })
  public studentRemark(data) {
    return service.education.studentRemark(data)
  }
  @Action({ rawError: true })
  public studentUpdate(data) {
    return service.education.studentUpdate(data)
  }
  @Action({ rawError: true })
  public instrumentUse({ teacher_employee_id }) {
    return service.education.instrumentUse(teacher_employee_id)
  }
}

export default Education
