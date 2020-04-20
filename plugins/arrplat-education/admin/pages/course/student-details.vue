<template>
  <div class="student-details panel">
    <el-row>
      <el-col :span="24">
        <el-breadcrumb class="breadcrumb" separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">学员管理</el-breadcrumb-item>
          <el-breadcrumb-item>学员详情</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
      <el-col :span="12">
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-menu-item index="1">基础信息</el-menu-item>
          <el-menu-item index="2">课程记录</el-menu-item>
          <el-menu-item index="3">签到记录</el-menu-item>
          <el-menu-item index="4">消费记录</el-menu-item>
        </el-menu>
      </el-col>
      <el-col :span="12">
        <div class="capability">
          <span class="copywriting">学员能力值是否可见</span>
          <el-radio-group v-model="capability">
            <el-radio :label= 1>可见</el-radio>
            <el-radio :label= 2>不可见</el-radio>
          </el-radio-group>
        </div>
      </el-col>
    </el-row>
    <div class="box">
      <!-- 基础信息 -->
      <div class="information-box" v-if="activeIndex == '1'">
        <div class="information">
          <div class="info-top">
            <span class="info-title">基本信息</span>
            <div class="info-left">
              <el-form ref="form" :model="studentDetailObj" label-width="100px">
                <el-form-item label="学号">
                  <span>{{ studentDetailObj.number}}</span>
                </el-form-item>
                <el-form-item label="姓名">
                  <el-input v-if="textIndex == 1" v-model="studentDetailObj.name"></el-input>
                  <span class="def-text" v-else>{{ studentDetailObj.name}}</span>
                  <span :class="{ textSaveClass: (textIndex == 1),modify: (textIndex != 1)}" @click="modifyName(1,textIndex)">{{ textIndex == 1 ? textSave : textEdit }}</span>
                </el-form-item>
                <el-form-item label="手机">
                  <el-input v-if="textIndex == 2" v-model="studentDetailObj.phone"></el-input>
                  <span class="def-text" v-else>{{studentDetailObj.phone}}</span>
                  <span :class="{ textSaveClass: (textIndex == 2),modify: (textIndex != 2)}" @click="modifyPhone(2,textIndex)">{{ textIndex == 2 ? textSave : textEdit }}</span>
                </el-form-item>
                <el-form-item label="性别">
                  <el-radio-group v-model="studentDetailObj.sex">
                    <el-radio :label= 1>男</el-radio>
                    <el-radio :label= 2>女</el-radio>
                  </el-radio-group>
                </el-form-item>
                <el-form-item label="有无基础">
                  <el-radio-group v-model="studentDetailObj.has_basis">
                    <el-radio :label= 1>有</el-radio>
                    <el-radio :label= 2>无</el-radio>
                  </el-radio-group>
                </el-form-item>
                <el-form-item label="是否点评">
                  <el-radio-group v-model="studentDetailObj.has_comment">
                    <el-radio :label= 1>未点评</el-radio>
                    <el-radio :label= 2>已告知</el-radio>
                    <el-radio :label= 3>已点评</el-radio>
                  </el-radio-group>
                </el-form-item>
                <el-form-item label="报名时间">
                  <span>{{ studentDetailObj.apply_time | formatDate(2) }}</span>
                </el-form-item>
                <el-form-item label="报名校区">
                  <el-input v-if="textIndex == 3" v-model="studentDetailObj.campus_name"></el-input>
                  <span class="def-text" v-else>{{ studentDetailObj.campus_name}}</span>
                  <span :class="{ textSaveClass: (textIndex == 3),modify: (textIndex != 3)}" @click="modify(3)">{{ textIndex == 3 ? textSave : textEdit }}</span>
                </el-form-item>
                <el-form-item label="所属老师">
                  <el-select
                    v-if="textIndex == 4"
                    @change="changeUpdataTeacher"
                    class="selectTeacher"
                    v-model="detailEmployee"
                    placeholder="请选择">
                    <el-option
                      v-for="(item,index) in employee"
                      :key="index"
                      :label="item.nickname"
                      :value="item.id">
                    </el-option>
                  </el-select>
                  <span class="def-text" v-else>{{ studentDetailObj.teacher_name }}</span>
                  <span :class="{ textSaveClass: (textIndex == 4),modify: (textIndex != 4)}" @click="modifyTeacher(4,textIndex)">{{ textIndex == 4 ? textSave : textEdit }}</span>
                  <span>锁定老师</span>
                </el-form-item>
              </el-form>
            </div>
            <div class="info-right">
              <el-form ref="form" :model="form" label-width="100px">
                <el-form-item label="学员等级">
                  <el-select
                    v-if="textIndex == 5"
                    @change="changeUpdataLevel"
                    clearable
                    class="selectTeacher"
                    v-model="levelName"
                    placeholder="请选择">
                    <el-option
                      v-for="(item,index) in getStudentLevelList"
                      :key="index"
                      :label="item.name"
                      :value="item.id">
                    </el-option>
                  </el-select>
                  <span class="def-text" v-else>{{ studentDetailObj.level_name}}</span>
                  <span :class="{ textSaveClass: (textIndex == 5),modify: (textIndex != 5)}" @click="modifyLevel(5,textIndex)">{{ textIndex == 5 ? textSave : textEdit }}</span>
                </el-form-item>
                <el-form-item label="当前套餐">
                  <!--<el-input v-if="textIndex == 6" v-model="studentDetailObj.packet_name"></el-input>-->
                  <span class="def-text">{{ studentDetailObj.packet_name }}</span>
                  <!--<span :class="{ textSaveClass: (textIndex == 6),modify: (textIndex != 6)}" @click="modify(6)">{{ textIndex == 6 ? textSave : textEdit }}</span>-->
                </el-form-item>
                <el-form-item label="是否教学计划">
                  <el-radio-group v-model="studentDetailObj.is_teach_plan">
                    <el-radio :label= 1>是</el-radio>
                    <el-radio :label= 2>否</el-radio>
                  </el-radio-group>
                </el-form-item>
                <el-form-item label="乐器类型">
                  <el-select
                    v-if="textIndex == 7"
                    @change="instrumentChange"
                    clearable
                    class="selectTeacher"
                    v-model="selectInstrument"
                    placeholder="请选择">
                    <el-option
                      v-for="(item,index) in instrument"
                      :key="index"
                      :label="item.name"
                      :value="item.id">
                    </el-option>
                  </el-select>
                  <span class="def-text" v-else>{{ studentDetailObj.instrument_name }}</span>
                  <span :class="{ textSaveClass: (textIndex == 7),modify: (textIndex != 7)}" @click="modifyInstrument(7,textIndex)">{{ textIndex == 7 ? textSave : textEdit }}</span>
                </el-form-item>
                <el-form-item label="乐器使用情况">
                  <el-select
                    v-if="textIndex == 8"
                    @change="changeInstrumentUser"
                    class="selectTeacher"
                    v-model="instrument_use_name"
                    placeholder="请选择">
                    <el-option
                      v-for="(item,index) in instrumentUseList"
                      :key="index"
                      :label="item.name"
                      :value="item.id">
                    </el-option>
                  </el-select>
                  <span class="def-text" v-else>{{ studentDetailObj.instrument_use_name }}</span>
                  <span :class="{ textSaveClass: (textIndex == 8),modify: (textIndex != 8)}" @click="modifyInstrumentUse(8,textIndex)">{{ textIndex == 8 ? textSave : textEdit }}</span>
                </el-form-item>
              </el-form>
            </div>
            <div class="info-remarks" style="height: 440px;overflow: auto">
              <p class="info-title">修改记录</p>
              <el-form style="padding-left: 10px;border: 1px solid #eeeeee;margin-top: 10px" ref="form" :model="form" label-width="80px">
                <span style="font-size: 13px;margin-top: 10px">丁老师 2020-09-30 12:34:55</span>
                <p style="font-size: 14px;margin-top: 10px">修改了学员等级</p>
                <el-input style="width: calc(100% - 20px);margin-top: 10px" v-if="textIndex == 11" v-model="form.name"></el-input>
                <span class="def-text-remark" v-else>{{ form.name}}</span>
                <span style="margin-top: 10px" :class="{ textSaveClass: (textIndex == 11),modify: (textIndex != 11)}" @click="modify(11)">{{ textIndex == 11 ? textSave : textEdit }}</span>
              </el-form>
            </div>
          </div>
          <div class="info-center">
            <span class="info-title">课程信息</span>
            <div class="info-left">
              <el-form ref="form" :model="form" label-width="100px">
                <el-form-item label="是否可约课">
                  <el-radio-group v-model="studentDetailObj.is_enabled">
                    <el-radio :label= 1>是</el-radio>
                    <el-radio :label= 2>否</el-radio>
                  </el-radio-group>
                </el-form-item>
                <el-form-item label="总课时">
                  <el-input v-if="textIndex == 9" v-model="studentDetailObj.all_class_hours"></el-input>
                  <span class="def-text" v-else>{{ studentDetailObj.all_class_hours }}</span>
                  <span :class="{ textSaveClass: (textIndex == 9),modify: (textIndex != 9)}" @click="modifyAllHours(9,textIndex)">{{ textIndex == 9 ? textSave : textEdit }}</span>
                </el-form-item>
                <el-form-item label="已用课时">
                  <span>{{ studentDetailObj.learn_hour }}</span>
                </el-form-item>
                <el-form-item label="剩余课时">
                  <span>{{ studentDetailObj.last_learn_hour }}</span>
                </el-form-item>
                <el-form-item label="剩余课点">
                  {{ studentDetailObj.remainder_class_points }}
                </el-form-item>
                <el-form-item label="是否节课">
                  <el-radio-group v-model="studentDetailObj.is_end">
                    <el-radio :label= 2>未结课</el-radio>
                    <el-radio :label= 1>已结课</el-radio>
                  </el-radio-group>
                </el-form-item>
              </el-form>
            </div>
            <div class="info-right">
              <el-form ref="form" :model="form" label-width="100px">
                <el-form-item label="签到次数">
                  <span>{{ studentDetailObj.learn_hour }}</span>
                </el-form-item>
                <el-form-item label="到期时间">
                  <el-date-picker
                    v-model="studentEndTime"
                    type="datetime"
                    :disabled="endTimeDsiabled"
                    @change="changeEedTime"
                    placeholder="选择日期时间">
                  </el-date-picker>

                  <!--<el-input v-if="textIndex == 10" v-model="studentDetailObj.end_time"></el-input>-->
                  <!--<span class="def-text" v-else>{{ studentDetailObj.end_time }}</span>-->
                  <span :class="{ textSaveClass: (textIndex == 10),modify: (textIndex != 10)}" @click="modifyEndTime(10,textIndex)">{{ textIndex == 10 ? textSave : textEdit }}</span>
                </el-form-item>

                <el-form-item label="剩余天数">
                  <span>{{form.name}}</span>
                </el-form-item>
                <el-form-item label="是否冻结课程">
                  <el-radio-group v-model="studentDetailObj.is_locked">
                    <el-radio :label= 0>不冻结</el-radio>
                    <el-radio :label= 1>冻结</el-radio>
                  </el-radio-group>
                  <el-date-picker
                    v-model="form.region"
                    clearable
                    type="daterange"
                    range-separator="至"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期">
                  </el-date-picker>
                </el-form-item>

              </el-form>
            </div>
          </div>
          <div class="info-bottom">
            <div class="info-left" v-if="capability == 1">
              <span class="info-title">学员能力值</span>
              <div class="info-left-content">
                <el-tag
                  v-for="item in studentDetailObj.able"
                  :key="item.id"
                  :type="item.id"
                  effect="plain">
                  {{ item.name }}
                </el-tag>
              </div>
            </div>
            <div class="info-right">
              <el-button @click="createRemark" type="primary">新建备注</el-button>
              <el-table
                :data="remarkList"
                height="250"
                border
                style="width: 100%;margin-top: 10px">
                <el-table-column
                  prop="date"
                  label="备注类型"
                  width="150">
                  <template slot-scope="scope">
                    <span v-if="scope.row.remark_type == 1">学生备注</span>
                    <span v-else>老师备注</span>
                  </template>
                </el-table-column>
                <el-table-column
                  prop="remark"
                  label="备注内容"
                  width="180">
                </el-table-column>
                <el-table-column
                  prop="address"
                  label="时间"
                  width="200">
                  <template slot-scope="scope">
                    <span>{{ scope.row.create_time | formatDate(2)}}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  prop="name"
                  label="创建人">
                  <template slot-scope="scope">
                    <span v-if="scope.row.remark_type == 1">{{ scope.row.student_name }}</span>
                    <span v-else>{{ scope.row.teacher_name }}</span>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </div>
        <el-dialog
          title="提示"
          :visible.sync="alertCreateRemark"
          width="40%"
          :before-close="handleClose">
          <el-form ref="form" :model="createRemarkMsg" label-width="80px">
            <el-form-item label="备注类型">
              <el-radio-group v-model="createRemarkMsg.remark_type">
                <el-radio :label= 2>老师备注</el-radio>
                <el-radio :label= 1>学生备注</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="备注内容">
              <el-input type="textarea" v-model="createRemarkMsg.desc"></el-input>
            </el-form-item>
            <el-form-item v-if="createRemarkMsg.remark_type == 2" label="创建人">
              <el-select
                @change="changeCreateTeacher"
                clearable
                v-model="employeeSelect"
                placeholder="请选择"
                style="width: 100%">
                <el-option
                  v-for="(item,index) in employee"
                  :key="index"
                  :label="item.nickname"
                  :value="item.id">
                </el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
          <el-button @click="handleClose">取 消</el-button>
          <el-button type="primary" @click="handleTrue">确 定</el-button>
        </span>
        </el-dialog>
      </div>
      <!-- 课程记录 -->
      <div class="panels-second" v-if="activeIndex == '2'">
        <el-row>
          <el-col :span="8">
            <div class="user_select_con">
              <span class="user_select_title">学员等级：</span>
              <el-select
                @change="changeStudentLevel"
                clearable
                v-model="selectStudentLevel"
                placeholder="请选择">
                <el-option
                  v-for="item in getStudentLevelList"
                  :label="item.name"
                  :value="item.id">
                </el-option>
              </el-select>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="user_select_con">
              <span class="user_select_title">约课学员等级：</span>
              <el-select
                @change="changeStudent"
                clearable
                v-model="selectLevel"
                placeholder="请选择">
                <el-option
                  v-for="item in getStudentLevelList"
                  :label="item.name"
                  :value="item.id">
                </el-option>
              </el-select>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="user_select_con">
              <span class="user_select_title">课程种类：</span>
              <el-select
                @change="changeBaseCourse"
                clearable
                v-model="selectBaseCourse"
                placeholder="请选择">
                <el-option
                  v-for="item in baseCourselist"
                  :label="item.course_type_name"
                  :value="item.course_type_id">
                </el-option>
              </el-select>
            </div>
          </el-col>
        </el-row>
        <el-row class="row-bottom">
          <el-col :span="8">
            <div class="user_select_con">
              <span class="user_select_title">上课老师：</span>
              <el-select
                @change="changeTeacher"
                clearable
                v-model="employeeSelect"
                placeholder="请选择">
                <el-option
                  v-for="(item,index) in employee"
                  :key="index"
                  :label="item.nickname"
                  :value="item.id">
                </el-option>
              </el-select>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="user_select_con">
              <span class="user_select_title">状态：</span>
              <el-select
                @change="changeStatus"
                clearable
                v-model="selectStudentStatus"
                placeholder="请选择">
                <el-option
                  v-for="item in studentStatus"
                  :label="item.value"
                  :value="item.id">
                </el-option>
              </el-select>
            </div>
          </el-col>
        </el-row>
        <el-table
          :data="studentCourseList"
          key="studentCourseList"
          border
          height="450"
          class="second-table"
          style="width: 100%">
          <el-table-column
            fixed
            type="index"
            label="序号"
            width="50">
          </el-table-column>
          <el-table-column
            prop="create_time"
            label="预约时间"
            width="250">
            <template slot-scope="scope">
              {{ scope.row.create_time | formatDate(2) }}
            </template>
          </el-table-column>
          <el-table-column
            prop="start_time"
            label="课程时间"
            width="250">
            <template slot-scope="scope">
              {{ scope.row.start_time | formatDate(1) }}
            </template>
          </el-table-column>
          <el-table-column
            prop="student_name"
            label="姓名"
            width="120">
          </el-table-column>
          <el-table-column
            prop="phone"
            label="联系方式"
            width="120">
          </el-table-column>
          <el-table-column
            prop="course_name"
            label="课程名称"
            width="120">
          </el-table-column>
          <el-table-column
            prop="level_name"
            label="学员等级"
            width="120">
          </el-table-column>
          <el-table-column
            prop="sign_level_name"
            label="签到学员等级"
            width="120">
          </el-table-column>
          <el-table-column
            prop="last_learn_hour"
            label="剩余课时"
            width="120">
          </el-table-column>
          <el-table-column
            prop="course_type_name"
            label="预约的课程种类"
            width="120">
          </el-table-column>
          <el-table-column
            prop="apply_type_str"
            label="约课方式"
            width="120">
          </el-table-column>
          <el-table-column
            prop="campus_name"
            label="校区"
            width="120">
          </el-table-column>
          <el-table-column
            prop="classroom_name"
            label="教室"
            width="120">
          </el-table-column>
          <el-table-column
            prop="teacher_name"
            label="上课老师"
            width="120">
          </el-table-column>
          <el-table-column
            prop="teacher_remark"
            label="备注"
            width="300">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="状态"
            width="360">
            <template slot-scope="scope">
              <el-radio-group @change="signTypeClick(scope.row)" v-model="scope.row.sign_type">
                <el-radio :label= 7>未签到</el-radio>
                <el-radio :label= 1>已签到</el-radio>
                <el-radio :label= 2>取消预约</el-radio>
                <el-radio :label= 3>学生旷课</el-radio>
              </el-radio-group>
            </template>
          </el-table-column>
        </el-table>
        <el-dialog
          title=""
          :visible.sync="dialogStkShop"
          width="40%"
          :before-close="handleStkShopClose">
          <div slot="title">
            <span class="title-age">确认课程取消吗？</span>
          </div>
          <el-form v-if="dialogStkShop" :model="stkReason" :rules="infoRules" ref="stkReason" label-width="80px">
            <el-form-item prop="desc" label-width="100px" label="填写原因">
              <el-input type="textarea" v-model="stkReason.desc"></el-input>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="handleStkShopClose">取 消</el-button>
            <el-button type="primary" @click="handleStkShopTrue">确 定</el-button>
          </span>
        </el-dialog>
        <!-- 正式课体系课签到 -->
        <el-dialog
          title="签到"
          :visible.sync="dialogZskSign"
          width="40%"
          class="signZsk"
          :before-close="handleZskSignClose">
          <!-- 历史签到记录 -->
          <el-form class="alert_add_zsks" ref="addZsk" :model="historySignInList" label-width="80px">
            <el-form-item label-width="100px" label="选择主题">
              <el-select
                v-model="historyListArr"
                multiple
                disabled
                collapse-tags
                placeholder="选择主题（多选）">
                <el-option
                  v-for="item in historyList"
                  :key="item.subject_id"
                  :label="item.subject_name"
                  :value="item.subject_id">
                </el-option>
              </el-select>
            </el-form-item>
            <el-collapse class="zsk_sign_content" v-model="selectThemeHistoryList">
              <el-collapse-item title="" :name="item.subject_id"  v-for="(item,index) in historySelectlist">
                <div slot="title">
                  <div>
                    <span>{{item.subject_name}}</span>
                    <el-input style="width: 70px;color: green;" :disabled="true" v-model="item.percentage+'%'"></el-input>
                  </div>
                </div>
                <div v-for="(list,n) in item.values">
                  <div class="second_content">
                    <span class="second_content_title">{{list.essential_name}}</span>
                    <template>
                      <el-radio-group v-model="list.status" @change="changeSchedule(item)">
                        <el-radio disabled :label= '1'>未开始</el-radio>
                        <el-radio disabled :label= '2'>进行中</el-radio>
                        <el-radio disabled :label= '3'>已结束</el-radio>
                      </el-radio-group>
                    </template>
                  </div>
                </div>
              </el-collapse-item>
            </el-collapse>
            <el-form-item label-width="100px" label="回课备注1">
              <el-input :disabled="true" type="textarea" v-model="historySignInList.teacher_remark"></el-input>
            </el-form-item>
            <el-form-item label-width="100px" label="回课备注2">
              <el-input :disabled="true" type="textarea" v-model="historySignInList.student_remark"></el-input>
            </el-form-item>
            <el-form-item label-width="100px" label="选择素材">
              <el-select
                v-model="materialSelect"
                multiple
                disabled
                collapse-tags
                placeholder="全部">
                <el-option
                  v-for="(item,index) in materialList"
                  :key="index"
                  :label="item.name"
                  :value="item.id">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label-width="100px" label="学员等级">
              <el-select
                clearable
                disabled
                v-model="historySignInList.level_name"
                placeholder="上课学员是多选">
                <el-option
                  v-for="item in getStudentLevelList"
                  :label="item.name"
                  :value="item.id">
                </el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <!-- 签到记录 -->
          <el-form class="alert_add_zsks" ref="addZsk" :model="addCustomer" label-width="80px">
            <el-form-item label-width="100px" label="选择主题">
              <el-select
                v-model="historyListArr"
                multiple
                collapse-tags
                @change="changeTheme"
                placeholder="选择主题（多选）">
                <el-option
                  v-for="item in historyList"
                  :key="item.subject_id"
                  :label="item.subject_name"
                  :value="item.subject_id">
                </el-option>
              </el-select>
            </el-form-item>
            <el-collapse class="zsk_sign_content" v-model="selectThemeList">
              <el-collapse-item title="" :name="item.subject_id"  v-for="(item,index) in historySelectlist">
                <div slot="title">
                  <div>
                    <span>{{item.subject_name}}</span>
                    <el-input style="width: 70px;color: green;" :disabled="true" v-model="item.percentage+'%'"></el-input>
                    <span @click.stop.prevent="deleteContentList(item.subject_id)" style="color: red">删除</span>
                  </div>
                </div>
                <div v-for="(list,n) in item.values">
                  <div class="second_content">
                    <span class="second_content_title">{{list.essential_name}}</span>
                    <template>
                      <el-radio-group v-model="list.status" @change="changeSchedule(item)">
                        <el-radio :label= '1'>未开始</el-radio>
                        <el-radio :label= '2'>进行中</el-radio>
                        <el-radio :label= '3'>已结束</el-radio>
                      </el-radio-group>
                    </template>
                  </div>
                </div>
              </el-collapse-item>
            </el-collapse>
            <el-form-item label-width="100px" label="回课备注1">
              <el-input type="textarea" v-model="teacherRemark"></el-input>
            </el-form-item>
            <el-form-item label-width="100px" label="回课备注2">
              <el-input type="textarea" v-model="studentRemarks"></el-input>
            </el-form-item>
            <el-form-item label-width="100px" label="选择素材">
              <el-select
                @change="changeSelectMaterial"
                v-model="materialSelect"
                multiple
                collapse-tags
                placeholder="全部">
                <el-option
                  v-for="(item,index) in materialList"
                  :key="index"
                  :label="item.name"
                  :value="item.id">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label-width="100px" label="学员等级">
              <el-select
                clearable
                @change="changeStudentLevel"
                v-model="selectStudentLevel"
                placeholder="请选择学员等级">
                <el-option
                  v-for="item in getStudentLevelList"
                  :label="item.name"
                  :value="item.id">
                </el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="handleZskSignClose">取 消</el-button>
            <el-button type="primary" @click="handleZskSignTrue">确 定</el-button>
          </span>
        </el-dialog>
        <!-- 正式课非体系课签到 -->
        <el-dialog
          title="签到"
          :visible.sync="dialogZskNoSystem"
          width="40%"
          class="signZsk"
          :before-close="handleZskSignClose">
          <el-form class="alert_add_zsks" ref="addZsk" :model="addCustomer" label-width="80px">
            <el-form-item label-width="100px" label="选择主题">
              <el-select
                v-model="historyListArr"
                multiple
                collapse-tags
                @change="changeTheme"
                placeholder="选择主题（多选）">
                <el-option
                  v-for="item in historyList"
                  :key="item.subject_id"
                  :label="item.subject_name"
                  :value="item.subject_id">
                </el-option>
              </el-select>
            </el-form-item>
            <el-collapse class="zsk_sign_content" v-model="selectThemeList">
              <el-collapse-item title="" :name="item.subject_id"  v-for="(item,index) in historySelectlist">
                <div slot="title">
                  <div>
                    <span>{{item.subject_name}}</span>
                    <el-input style="width: 70px;color: green;" :disabled="true" v-model="item.percentage+'%'"></el-input>
                    <span @click.stop.prevent="deleteContentList(item.subject_id)" style="color: red">删除</span>
                  </div>
                </div>
                <div v-for="(list,n) in item.values">
                  <div class="second_content">
                    <span class="second_content_title">{{list.essential_name}}</span>
                    <template>
                      <el-radio-group v-model="list.status" @change="changeSchedule(item)">
                        <el-radio :label= '1'>未开始</el-radio>
                        <el-radio :label= '2'>进行中</el-radio>
                        <el-radio :label= '3'>已结束</el-radio>
                      </el-radio-group>
                    </template>
                  </div>
                </div>
              </el-collapse-item>
            </el-collapse>
            <el-form-item label-width="100px" label="课程素材">
              <el-select
                @change="changeSelectMaterial"
                v-model="materialSelect"
                multiple
                collapse-tags
                placeholder="全部">
                <el-option
                  v-for="(item,index) in materialList"
                  :key="index"
                  :label="item.name"
                  :value="item.id">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label-width="100px" label="回课备注1">
              <el-input type="textarea" v-model="teacherRemark"></el-input>
            </el-form-item>
            <el-form-item label-width="100px" label="回课备注2">
              <el-input type="textarea" v-model="studentRemarks"></el-input>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="handleZskSignClose">取 消</el-button>
            <el-button type="primary" @click="handleZskSignTrue">确 定</el-button>
          </span>
        </el-dialog>
      </div>
      <!-- 签到记录 -->
      <div class="panels-second" v-if="activeIndex == '3'">
        <div style="width: 100%;overflow: auto;height: 500px">
          <el-form class="alert_add_zsk" ref="addZsk" :model="historySignInList" label-width="80px">
            <el-form-item style="margin-bottom: 20px" v-for="item in historyListData">
              <el-form-item label-width="100px" label="选择主题">
                <el-select
                  v-model="historyListArrs"
                  multiple
                  disabled
                  collapse-tags
                  placeholder="选择主题（多选）">
                  <el-option
                    v-for="item in signHistoryList"
                    :key="item.subject_id"
                    :label="item.subject_name"
                    :value="item.subject_id">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-collapse class="zsk_sign_content" v-model="selectThemeHistoryList">
                <el-collapse-item title="" :name="item.subject_id"  v-for="(item,index) in historySelectlist">
                  <div slot="title">
                    <div>
                      <span>{{item.subject_name}}</span>
                      <el-input style="width: 70px;color: green;" :disabled="true" v-model="item.percentage+'%'"></el-input>
                    </div>
                  </div>
                  <div v-for="(list,n) in item.values">
                    <div class="second_content">
                      <span class="second_content_title">{{list.essential_name}}</span>
                      <template>
                        <el-radio-group v-model="list.status" @change="changeSchedule(item)">
                          <el-radio disabled :label= '1'>未开始</el-radio>
                          <el-radio disabled :label= '2'>进行中</el-radio>
                          <el-radio disabled :label= '3'>已结束</el-radio>
                        </el-radio-group>
                      </template>
                    </div>
                  </div>
                </el-collapse-item>
              </el-collapse>
              <el-form-item label-width="100px" label="回课备注1">
                <el-input :disabled="true" type="textarea" v-model="item.teacher_remark"></el-input>
              </el-form-item>
              <el-form-item label-width="100px" label="回课备注2">
                <el-input :disabled="true" type="textarea" v-model="item.student_remark"></el-input>
              </el-form-item>
              <el-form-item label-width="100px" label="选择素材">
                <el-select
                  v-model="materialSelect"
                  multiple
                  disabled
                  collapse-tags
                  placeholder="全部">
                  <el-option
                    v-for="(item,index) in materialList"
                    :key="index"
                    :label="item.name"
                    :value="item.id">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label-width="100px" label="学员等级">
                <el-select
                  clearable
                  disabled
                  v-model="item.level_name"
                  placeholder="上课学员是多选">
                  <el-option
                    v-for="item in getStudentLevelList"
                    :label="item.name"
                    :value="item.id">
                  </el-option>
                </el-select>
              </el-form-item>
            </el-form-item>
          </el-form>
        </div>

      </div>
      <!-- 消费记录 -->
      <div class="panels-second" v-if="activeIndex == '4'">
        <el-table
          :data="getOrderList"
          key="getOrderList"
          border
          height="450"
          class="table"
          style="width: 100%">
          <el-table-column
            fixed
            type="index"
            label="序号"
            width="50">
          </el-table-column>
          <el-table-column
            prop="id"
            label="订单编号"
            width="120">
          </el-table-column>
          <el-table-column
            prop="status_str"
            label="订单状态"
            width="120">
          </el-table-column>
          <el-table-column
            prop="student_name"
            label="名称"
            width="120">
          </el-table-column>
          <el-table-column
            prop="student_phone"
            label="联系方式"
            width="300">
          </el-table-column>
          <el-table-column
            prop="stuent_sex_str"
            label="性别"
            width="120">

          </el-table-column>
          <el-table-column
            prop="campus_name"
            label="所属校区"
            width="120">
          </el-table-column>
          <el-table-column
            prop="sale_name"
            label="销售顾问"
            width="120">
          </el-table-column>
          <el-table-column
            prop="create_time"
            label="创建时间"
            width="200">
            <template slot-scope="scope">
              {{ scope.row.create_time | formatDate(2) }}
            </template>
          </el-table-column>
          <el-table-column
            prop="order_type_str"
            label="订单类型"
            width="300">
          </el-table-column>
          <el-table-column
            prop="category"
            label="订单二级类目"
            width="120">
          </el-table-column>
          <el-table-column
            prop="pay_price"
            label="订单金额"
            width="120">
          </el-table-column>
          <el-table-column
            prop="pay_type_str"
            label="支付方式"
            width="120">
          </el-table-column>
          <el-table-column
            prop="status_remark"
            label="订单异常原因"
            width="120">
          </el-table-column>
          <el-table-column
            prop="audition_teacher_name"
            label="试听老师"
            width="300">
          </el-table-column>
          <el-table-column
            prop="instrument_name"
            label="乐器类型"
            width="300">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="100">
            <template slot-scope="scope">
              <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>

</template>
<script lang="ts">
  import { Component, Vue, namespace } from 'nuxt-property-decorator'
  import { infoRules } from '../../components/formRules'
  const edu = namespace('education')
  const app = namespace('app')

  @Component({
    layout: 'plugin',
    filters:{
      formatDate: function (value,type) {
        if(!value){
          return
        }
        let date = new Date(value*1000)
        let y = date.getFullYear()
        let MM = date.getMonth() + 1
        MM = MM < 10 ? ('0' + MM) : MM
        let d = date.getDate()
        d = d < 10 ? ('0' + d) : d
        let h = date.getHours()
        let next_h = h < 10 ? ('0' + (h+1)) : (h+1)
        h = h < 10 ? ('0' + h) : h
        let m = date.getMinutes()
        m = m < 10 ? ('0' + m) : m
        let s = date.getSeconds()
        s = s < 10 ? ('0' + s) : s
        if(type == 1){
          return y + '-' + MM + '-' + d + ' ' + h + ':' + m + '-' + next_h + ':' + m
        }else if(type == 2){
          return y + '-' + MM + '-' + d + ' ' + h + ':' + m
        }
      }
    }
  })
  export default class UIndex extends Vue {
    value = new Date()
    @edu.Action getCourseSignList
    @edu.Action getCourseSignLists
    @edu.Action studentDetail
    @edu.Action studentCourse
    @edu.Action studentLevel
    @app.Getter currentOrgIdGetter
    @edu.Action baseCourse
    @edu.Action getCampus
    @edu.Action getOrder
    @edu.Action studentRemark
    @edu.Action studentUpdate
    @edu.Action getInstrumentType
    @edu.Action instrumentUse
    @edu.Action getClassSign
    @edu.Action material


    async mounted() {
      this.org_id = this.currentOrgIdGetter
      // 学生详情
      this.getStudentDetail()
      //  课程等级
      this.getStudentLevel()
      //  乐器类型
      this.getInstrument()
    }


    async update(data){
      data.student_id = this.studentId
      const res = await this.studentUpdate(data)
      if(res.status == 200){
        this.getStudentDetail()
      }
    }

    modifyFlag(val){
      if(this.textIndex == val){
        this.textIndex = 0
      }else{
        this.textIndex = val
      }
    }
    modifyName(val,type){
      this.modifyFlag(val)
      if(type == 1){
        let data = {
          name: this.studentDetailObj.name
        }
        this.update(data)
      }
    }
    modifyPhone(val,type){
      this.modifyFlag(val)
      if(type == 2){
        let data = {
          phone: this.studentDetailObj.phone
        }
        this.update(data)
      }
    }
    modifyTeacher(val,type){
      this.modifyFlag(val)
      if(type == 0){
        this.employeeSelect = this.studentDetailObj.teacher_name
        this.changeTeacherId = this.studentDetailObj.teacher_id
      }
      if(type == 4){
        let data = {
          teacher_id: this.changedetailTeacherId
        }
        this.update(data)
      }
    }

    modifyLevel(val,type){
      this.modifyFlag(val)
      if(type == 0){
        this.changeStudentId = this.studentDetailObj.level_id
        this.levelName = this.studentDetailObj.level_name
      }
      if(type == 5){
        let data = {
          level_id: this.changeStudentId
        }
        this.update(data)
      }
    }

    // 乐器类型
    modifyInstrument(val,type){
      this.modifyFlag(val)
      if(type == 0){
        this.instrumentTypeId = this.studentDetailObj.instrument_id
        this.selectInstrument = this.studentDetailObj.instrument_name
      }
      if(type == 7){
        let data = {
          instrument_type_id: this.instrumentTypeId
        }
        this.update(data)
      }
    }

    // 乐器使用情况
    modifyInstrumentUse(val,type){
      this.modifyFlag(val)
      if(type == 0){
        this.instrument_use_id = this.studentDetailObj.instrument_use_id
        this.instrument_use_name = this.studentDetailObj.instrument_use_name
      }
      if(type == 8){
        let data = {
          instrument_use_id: this.instrument_use_id
        }
        this.update(data)
      }
    }
    // 全部课时
    modifyAllHours(val,type){
      this.modifyFlag(val)
      if(type == 9){
        let data = {
          all_class_hours: this.studentDetailObj.all_class_hours
        }
        this.update(data)
      }
    }

    // 到期时间
    modifyEndTime(val,type){

      this.modifyFlag(val)
      if(type == 0){
        this.endTimeDsiabled = false
      }else{
        let data = {
          end_time: this.studentEndTime/1000
        }
        this.update(data)
        this.endTimeDsiabled = true
      }
    }

    changeEedTime(val){
      this.studentEndTime = Date.parse(val)
    }


    // 学员等级筛选
    changeUpdataLevel(val){
      this.changeStudentId = val
    }

    async getInstrument(){
      const instrument = await this.getInstrumentType({org_id: this.org_id})
      if(instrument.status == 200 && instrument.data.data.list && instrument.data.data.list.length>0){
        this.instrument = instrument.data.data.list
      }
    }


    // 监听乐器类型
    instrumentChange(val){
      this.instrumentTypeId = val;
    }

    modify(val,type){
      if(this.textIndex == val){
        this.textIndex = 0
      }else{
        this.textIndex = val
      }
    }

    changeUpdataTeacher(val){
      this.changedetailTeacherId = val
      // 乐器使用情况
      this.getInstrumentUse()
    }

    // 学生详情(0)
    async getStudentDetail(){
      const res = await this.studentDetail({'student_id': this.studentId})
      this.studentDetailObj = res.data.data
      this.campus_id = this.studentDetailObj.campus_id
      this.capability = this.studentDetailObj.show_student_value
      this.remarkList = this.studentDetailObj.remark_list
      this.changedetailTeacherId = this.studentDetailObj.teacher_id
      this.instrument_use_name = this.studentDetailObj.instrument_use_name
      this.instrument_use_id = this.studentDetailObj.instrument_use_id
      this.studentEndTime = this.studentDetailObj.end_time*1000
      this.is_teach_plan = this.studentDetailObj.is_teach_plan
      // 上课老师
      this.getSchool()
      // 乐器使用情况
      this.getInstrumentUse()
    }
    createRemark(){
      this.alertCreateRemark = true
    }
    // 切换老师
    changeCreateTeacher(val){
      this.changeTeacherId = val
    }
    // 切换乐器使用情况
    changeInstrumentUser(val){
      this.instrument_use_id = val
    }
    handleClose(){
      this.alertCreateRemark = false
    }
    async handleTrue(){
      let data = {
        remark: this.createRemarkMsg.desc,
        remark_type: this.createRemarkMsg.remark_type,
        student_id: this.studentId
      }
      if(this.changeTeacherId){
        data['teacher_id'] = this.changeTeacherId
      }
      const res = await this.studentRemark(data)
      this.handleClose()
      this.getStudentDetail()
    }

    // 乐器使用情况
    async getInstrumentUse(){
      const res = await this.instrumentUse({'teacher_employee_id': this.changedetailTeacherId})
      if(res.status == 200){
        this.instrumentUseList = res.data.data.list
      }
    }




    // 课程记录(1)
    async getStudentCourse(){
      const res = await this.studentCourse({'student_id': this.studentId, 'sign_student_level_id': this.changeStudentId, 'student_level_id': this.changeStudentLevelId, 'course_type_id': this.changeBaseCourseId, 'teacher_id': this.changeTeacherId, 'sign_type': this.changeStatusId})
      this.studentCourseList = res.data.data.list
    }
    signTypeClick(val){
      this.itemId = val.id
      this.teacherEmployeeId = val.teacher_employee_id
      this.course_id = val.course_id
      console.log(val,'-----------------')
      if(val.sign_type == 2){
        this.signType = 2
        this.dialogStkShop = true
      }else if(val.sign_type == 3){
        this.signType = 3
        this.dialogStkShop = true
      }else if(val.sign_type == 1){
        this.getMaterial()
        this.getSignLists()
        if(this.is_teach_plan == 1){
          // 体系课签到
          this.dialogZskSign = true
        }else{
          // 非体系课签到
          this.dialogZskNoSystem = true
        }
      }
    }
    handleStkShopClose(){
      this.dialogStkShop = false
      this.dialogZskSign = false
      this.getStudentCourse()
    }


    // 试听课无意向到店原因提交
    handleStkShopTrue(){
      if(!this.stkReason.desc){
        return false
      }
      let data:any = {
        teacher_remark: this.stkReason.desc,
        sign_type: this.signType,
        course_type: 1,
        id: this.itemId
      }
      this.signIn(data)
    }

    // 签到方法
    async signIn(data){
      data.org_id = this.org_id
      const res = await this.getClassSign(data)
      if(res.status == 200){
        this.handleStkShopClose()
        console.log('签到成功:',res)
      }
    }

    // 正式课签到学员等级
    async getStudentLevel(){
      const res = await this.studentLevel({org_id: this.org_id})
      if(res.status == 200){
        this.getStudentLevelList = res.data.data.list
      }
    }

    // 正式课签到取消
    handleZskSignClose(){
      this.dialogZskSign = false
      this.dialogZskNoSystem = false

      this.materialSelect = []
      this.studentRemarks = ''
      this.teacherRemark = ''
      this.selectStudentLevel = ''
    }
    // 监测进度百分比
    changeSchedule(list){
      let data = list.values
      var count = 0
      var len = data.length
      for(var i=0;i<data.length;i++){
        if(data[i].status == 1){
          count += 0
        }else if(data[i].status == 2){
          count += 100/len/2
        }else if(data[i].status == 3){
          count += 100/len
        }
      }
      list.percentage = count

      for(var i=0;i<this.signPostData.length;i++){
        if(this.signPostData[i].subject_id == list.subject_id){
          this.signPostData[i] = list
        }
      }
    }

    // 主题筛选 多选
    changeTheme(val){
      this.historySelectlist = []
      if(val.length == 0){
        return false
      }
      for(var i=0;i<val.length;i++){
        for(var j=0;j<this.historyList.length;j++){
          if(val[i] == this.historyList[j].subject_id){
            this.historySelectlist.push(this.historyList[j])
          }
        }
      }
    }
    // 正式课签到主题删除
    deleteContentList(val){
      for(var j=0;j<this.historySelectlist.length;j++){
        if(val == this.historySelectlist[j].subject_id){
          this.historySelectlist.splice(j, 1);
        }
      }
      for(var j=0;j<this.historyListArr.length;j++){
        if(val == this.historyListArr[j]){
          this.historyListArr.splice(j, 1);
        }
      }
    }

    // 正式课签到确定
    handleZskSignTrue(){
      let data = {
        "subject_essential_info": this.signPostData,
        "id": this.itemId,
        "sign_type": 1,
        "sign_student_level_id": this.changeStudentLevelId,
        "course_type": 1,
        "material_id": this.materialSelectList,
        "student_remark": this.studentRemarks,
        "teacher_remark": this.teacherRemark
      }
      console.log('签到参数：',data)
      this.signIn(data)
    }


    // 历史签到记录
    async getSignLists(){
      const res = await this.getCourseSignLists({'org_id': this.org_id,'course_id': this.course_id,'student_id': this.studentId,'types': 'history_list'})
      this.historySelectlist = []
      if(res.status == 200){
        this.historyList = res.data.data.list
        this.signPostData = res.data.data.list
        this.historySignInList = res.data.data.student_info
        for(var i=0;i<this.historyList.length;i++){
          if(this.historyList[i].percentage != '0'){
            this.historySelectlist.push(this.historyList[i])
          }
        }
      }
    }

    // 获取素材列表
    async getMaterial(){
      const res = await this.material({org_id: this.org_id ,teacherEmployeeId: this.teacherEmployeeId})
      if(res.status == 200){
        this.materialList = res.data.data.list
        console.log('获取素材列表:',this.materialList)
      }
    }



    // 课程种类
    async getBaseCourse(){
      const res = await this.baseCourse({org_id: this.org_id,campus_id: this.campus_id})
      if(res.status == 200){
        this.baseCourselist = res.data.data.list
      }
    }
    // 获取教师
    async getSchool(){
      const res = await this.getCampus({types: 'campus', org_id: this.org_id})
      if(res.status == 200 && res.data.data.list){
        this.campus = res.data.data.list
        if(this.campus.length > 0){
          for(var i=0;i<this.campus.length;i++){
            if(this.campus[i].campus_id == this.campus_id){
              this.employee = this.campus[i].values
            }
          }
        }
      }
    }
    //学员等级监听
    changeStudentLevel(val){
      this.changeStudentLevelId = val
      this.getStudentCourse()
    }
    // 约课学员学员等级监听
    changeStudent(val){
      this.changeStudentId = val
      this.getStudentCourse()
    }
    // 课程种类监听
    changeBaseCourse(val){
      this.changeBaseCourseId = val
      this.getStudentCourse()
    }
    // 上课老师监听
    changeTeacher(val){
      this.changeTeacherId = val
      this.getStudentCourse()
    }
    // 状态监听
    changeStatus(val){
      if(val == ''){
        val = 0
      }
      this.changeStatusId = val
      this.getStudentCourse()
    }




    // 历史签到记录(2)
    async getSignList(){
      const res = await this.getCourseSignList({'student_id': this.studentId,'types': 'sign_list','org_id': this.org_id})
      this.historyListData = []
      if(res.status == 200){
        this.signHistoryList = res.data.data.sign_list
        this.signHistoryList.forEach(item=>{
          this.historyListData.push(item.student_info)
        })
        console.log(this.historyListData,'-------this.historyList------')
      }
    }



    handleSelect(tab, event) {
      this.activeIndex = event[0]
      if(tab == 1){
        //  学生详情
        this.getStudentDetail()
        //  课程等级
        this.getStudentLevel()
      } else if (tab == 2){
        // 上课老师
        this.getSchool()
        // 课程种类
        this.getBaseCourse()
        //  课程等级
        this.getStudentLevel()
        //  课程记录
        this.getStudentCourse()
        //  签到记录
        this.getSignList()
      } else if (tab == 3){
        //  签到记录
        this.getSignList()
      } else if (tab == 4){
        this.order()
      }

      console.log(tab, event);
    }
    handleClick(val) {
      console.log(val);
    }

    // 消费记录(3)
    async order(){
      const res = await this.getOrder({'student_id': this.studentId})
      console.log(res)
      if(res.status == 200){
        this.getOrderList = []
        this.getOrderList.push(res.data)
      }
    }
    changeSelectMaterial(val){
      let str:string = val.toString()
      this.materialSelectList = str
    }





    org_id:string = ''
    capability: number =  1 // 能力值是否可见
    activeIndex: string = '1'
    //  基础信息(0)
    studentId:string = '1'
    studentDetailObj: any = {}   // 学生详情
    textEdit: string = '修改'
    textSave: string = '保存'
    textIndex: number = 0
    remarkList: any = [] // 签到记录
    alertCreateRemark: boolean = false // 创建弹窗
    levelName: string = '' // 学员等级
    instrument: any = [] // 乐器类型
    selectInstrument: string = '' //选择乐器类型str
    instrumentTypeId: string = '' //选择乐器类型id
    instrumentUseList: any = [] // 乐器使用情况list
    instrument_use_name: string = '' // 乐器使用情况name
    instrument_use_id: string = '' // 乐器使用情况id
    studentEndTime: number = 0 // 到期时间
    endTimeDsiabled: boolean = true  // 是否禁用时间空间
    is_teach_plan: number = 1 // 教学计划
    dialogZskNoSystem: boolean = false
    dialogZskSign: boolean = false



    // 课程记录(1)
    infoRules:any = infoRules
    studentCourseList:any = []
    campus_id: string = ''
    selectBaseCourse:string = ''
    campus: any = []
    employee: any = []
    employeeSelect: string = ''
    detailEmployee: string = ''
    studentStatus: any = [
      {
        id: 7,
        value: '未签到'
      },{
        id: 1,
        value: '已签到'
      },{
        id: 2,
        value: '取消预约'
      },{
        id: 3,
        value: '学生旷课'
      }]
    selectStudentStatus: string = ''
    changeStudentLevelId: string = '' //学员等级监听id
    changeStudentId: string = '' // 约课学员等级监听id
    changeBaseCourseId: string = '' // 课程种类监听
    changeTeacherId: string = '' // 上课老师监听
    changedetailTeacherId: string = '' // 上课老师监听
    changeStatusId: number = 0 // 状态监听
    getOrderList: any = [] // 消费记录
    signType: number = 1
    selectThemeList:any = [] // 正式课签到已选择主题
    historyList: any = []
    itemId: string = '' // id

    createRemarkMsg: any = {
      remark_type: 2,
      desc: '',
    } //新建备注
    dialogStkShop: boolean = false
    stkReason: any = {
      desc: ''
    }
    studentRemarks: string = ''
    teacherRemark: string = ''
    addCustomer: any = {} // 正式课签到
    materialSelectList: string = '' // 正式课签到选择素材list
    studentLevelId: string = ''   // 正式课选择学员等级id
    historyListArr: any = []
    teacherEmployeeId: string = ''
    course_id: string = ''






    // 签到记录(2)
    historyListArrs: any = []
    selectThemeHistoryList: any = []
    materialSelect: any = []
    materialList: any = []
    getStudentLevelList: any = []
    selectStudentLevel: string = ''
    selectLevel: string = ''
    form: any =  {
      name: '丁老师',
      region: '1',
      date1: '',
      date2: '',
      delivery: false,
      type: [],
      resource: '',
      desc: ''
    }

    // 课程记录
    value: string = ''
    // 签到记录
    historySelectlist: any = []
    signHistoryList: any = []
    signPostData: any = []
    historyListData: any = []
    historySignInList: any = {}
    baseCourselist: any = []
  }
</script>
<style lang="scss">
  .student-details{
    width: 100%;
  }
  .breadcrumb{
    height: 40px;
    line-height: 40px;
    font-size: 16px;
    margin-top: 10px;
    padding-left: 20px;
  }
  .el-menu-demo {
    .el-radio{
      margin-right: 10px;
    }
  }
  .def-text{
    display: inline-block;
    width: 60%;
  }
  .def-text-remark{
    display: block;
    line-height: 40px;
    margin-top: 10px
  }
  .capability{
    width: 100%;
    float: right;
    height: 60px;
    line-height: 60px;
    text-align: right;
    padding-right: 10px;
    border-bottom: solid 1px #e6e6e6;
    .copywriting{
      margin-right: 10px;
      color: #909399;
      font-size: 14px;
    }
  }
  .modify{
    color: blue;
    cursor: pointer;
  }
  .textSaveClass{
    color: #67c23a;
    cursor: pointer;
  }

  .el-form-item{
    margin-bottom: 10px;
  }
  .el-radio{
    margin-right: 10px;
  }
  .course{
    width: 100%;
  }
  .box{
    overflow: hidden;
    width: 100%;
  }
  .panel{
    background-color: #fff;
    -webkit-box-flex: 1;
    flex: 1;
    display: -webkit-box;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    flex-direction: column;
    margin: 15px;
    border: 1px solid #e2e8f0;
    padding: 15px;
    overflow: hidden;
  }
  .panels{
    background-color: #fff;
    -webkit-box-flex: 1;
    flex: 1;
    display: -webkit-box;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    flex-direction: column;
    margin: 15px;
    border: 1px solid #e2e8f0;
    padding: 15px;
    width: 100%;
  }

  .information-box{
    width: 100%;
    height: 100%;
    overflow: auto;
    .information{
      background-color: #fff;
      -webkit-box-flex: 1;
      flex: 1;
      display: -webkit-box;
      display: flex;
      -webkit-box-orient: vertical;
      -webkit-box-direction: normal;
      flex-direction: column;
      margin: 15px;
      border: 1px solid #e2e8f0;
      padding: 15px;
    }
    .info-top{
      width: 100%;
      .info-title{
        width: 100%;
        height: 30px;
        line-height: 30px;
        font-size: 16px;
        color: #666666;
        display: block;
      }
      .el-input{
        width: 60%;
      }
      .info-left{
        width: 40%;
        float: left;
      }
      .info-right{
        width: 40%;
        float: left;
      }
      .info-remarks{
        width: 19%;
        float: right;
      }
    }
    .info-center{
      width: 100%;
      .info-title{
        width: 100%;
        height: 30px;
        line-height: 30px;
        font-size: 16px;
        color: #666666;
        display: block;
      }
      .el-input{
        width: 60%;
      }
      .info-left{
        width: 50%;
        float: left;
      }
      .info-right{
        width: 50%;
        float: right;
      }
    }
    .info-bottom{
      display: flex;
      .info-left{
        width: 40%;
      }
      .info-right{
        width: 60%;
      }
      .info-left-content{
        width: 90%;
        padding: 10px;
        float: left;
        margin-top: 10px;
      }
    }
  }

  .panels-second{
    margin-top: 15px;
    width: 100%;
  }
  .user_select_con{
    display: flex;
    .user_select_title{
      text-align: right;
      width: 100px;
      font-size: 14px;
      color: #606266;
      line-height: 32px;
      -ms-flex-negative: 0;
      flex-shrink: 0;
    }
    .el-select{
      width: 70%;
    }
  }
  .table{
    margin-top: 10px;
    .cell{
      text-align: center;
    }
  }
  .row-bottom{
    margin-top: 10px;
  }
  .second-table{
    margin-top: 10px;
  }
  .second-table .cell{
    text-align: center !important;
  }
  .alert_add_zsk{
    width: 50%;
  }
  .alert_add_zsk .el-form-item .el-form-item{
    margin-bottom: 20px;
  }
  .selectTeacher .el-input{
    width: 100% !important;
  }


  .alert_add_zsks .el-select,.alert_add_zsks .el-autocomplete{
    width: 100%;
  }
  .alert_add_zsks .el-input,.alert_add_zsks .el-textarea,.alert_add_zsks .el-date-editor{
    width: 90%;
  }
  .alert_add_zsks .el-form-item{
    margin-bottom: 10px;
  }
  .alert_add_zsks .week .el-checkbox{
    margin-right: 5px;
  }
</style>
