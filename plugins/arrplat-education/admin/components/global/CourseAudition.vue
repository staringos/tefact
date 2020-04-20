<!-- 添加占用弹窗 -->
<template>
  <el-dialog
    title="添加试听课"
    :visible.sync="dialogAddStk"
    width="40%"
    :before-close="handleStkClose">
    <el-form class="alert_add_stk" ref="addStk" :model="addAudition" label-width="80px">
      <el-form-item class="must-fill" label="选择客户">
        <el-autocomplete
          style="width: 80%"
          class="inline-input"
          v-model="addAudition.customer"
          :fetch-suggestions="selectCustomer"
          placeholder="请输入内容"
          :trigger-on-focus="false"
          @select="handleSelectBusiness">
        </el-autocomplete>
        <span @click="createCustomer" style="color: blue;cursor: pointer">新建客户</span>
      </el-form-item>
      <el-form-item class="must-fill" label="选择商机">
        <el-select
          @change="businessChange"
          v-model="addAudition.business"
          placeholder="请选择商机">
          <el-option
            v-for="(item,index) in addAudition.selectBusiness"
            :key="index"
            :label="item.business_name"
            :value="item.business_id">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item class="must-fill" label="试听时间">
        <el-input class="ty_input_class" v-model="addAudition.clickTime"></el-input>
      </el-form-item>
      <el-form-item class="must-fill" label="上课老师">
        <el-input class="ty_input_class" :disabled="true" v-model="addAudition.teacherSelectName"></el-input>
      </el-form-item>
      <el-form-item class="must-fill" label="上课校区">
        <el-input class="ty_input_class" :disabled="true" v-model="addAudition.campusSelect"></el-input>
      </el-form-item>
      <el-form-item label="上课教室">
        <el-select
          @change="classRoomChange"
          v-model="addAudition.classRoomFirst"
          placeholder="去选择上课的教室">
          <el-option
            v-for="(item,index) in addAudition.classRoomList"
            :key="index"
            :label="item.name"
            :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item class="must-fill" label="销售人员">
        <el-select
          @change="peopleListChange"
          v-model="addAudition.getPeople"
          placeholder="去选择销售人员">
          <el-option
            v-for="(item,index) in addAudition.getPeopleList"
            :key="index"
            :label="item.nickname"
            :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="备注">
        <el-input type="textarea" v-model="addAudition.getStkDesc"></el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
        <el-button @click="handleStkClose">取 消</el-button>
        <el-button type="primary" @click="handleStkTrue">确 定</el-button>
      </span>
  </el-dialog>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, Prop, Watch, Emit, namespace } from 'nuxt-property-decorator'
  import { infoRules } from '../../components/formRules'
  const edu = namespace('education')
  const app = namespace('app')
  @Component({})
  export default class CourseAudition extends Vue {
    @edu.Action curriculum
    @app.Getter currentOrgIdGetter
    @edu.Action getCustomer



    @Prop() dialogAddStkDatas: any
    @Prop() dataAddAudition: any

    dialogAddStk: boolean = false
    addAudition: any = {
      customer: '',  // 选择客户
      customerId: '', // 客户id
      business: '',  // 选择商机
      selectBusiness: [], // 商机数据list
      clickTime: '',  // 试听时间
      teacherSelectName: '', // 上课老师
      campusSelect: '',  // 上课校区
      classRoomFirst: '', // 选择上课教室
      classRoomList: '',  // 上课教室list
      getPeople: '',  // 选择销售人员
      getPeopleList: '',  // 销售人员list
      getStkDesc: ''   // 描述
    }
    org_id: string = ''
    data: any = {
      customer_id: '',
      business_id: '',
      start_time: '',
      sale_employee_id: '',
      remark: '',
      campus_id: '',
      customer_id: '',
    }


    async mounted(){

      // console.log(this.dialogAddStkDatas,'-------dialogAddStkData-----')
      // this.dialogAddStk = this.dialogAddStkDatas.flag
      // this.addAudition.clickTime = this.dialogAddStkDatas.time
      // this.addAudition.teacherSelectName = this.dialogAddStkDatas.teacher
      // this.addAudition.campusSelect = this.dialogAddStkDatas.campus


      this.org_id = this.currentOrgIdGetter
    }

    // 选择客户
    async selectCustomer(queryString, cb){
      const res = await this.getCustomer( {name: queryString, phone: queryString, org_id: this.org_id} )
      if(res.status == 200){
        let restaurants = res.data.data.list
        if(restaurants){
          for(var i =0;i < restaurants.length;i++){
            restaurants[i].value = restaurants[i].customer_name
          }
          cb(restaurants)
        }
      }
    }
    // 获取商机数据 & 客户id
    handleSelectBusiness(item){
      this.addAudition.customerId = item.customer_id
      this.addAudition.selectBusiness = item.values
      this.data.customer_id = this.addAudition.customerId
    }
    // 选择商机id
    businessChange(val){
      this.data.business_id = val
    }

    // 监听销售人员筛选id
    peopleListChange(val){
      this.dataAddAudition.sale_employee_id = val
    }
    // 上课教师
    classRoomChange(val){
      this.data.classroom_id = val
    }
    // 销售人员
    peopleListChange(val){
      this.data.sale_employee_id = val
    }
    createCustomer(val){
      console.log(val,'-------createCustomer--------')
    }

    // 添加试听课弹窗关闭
    handleStkClose(){
      this.$emit('add-audition','close')
    }

    // 时间戳处理
    time(){
      let str = this.dataAddAudition.clickTime.split(' ')
      str = str[0]+ ' ' + str[1].split('-')[0]
      return Date.parse(str)/1000

    }
    // 添加试听课弹窗确定
    handleStkTrue(){
      this.data.course_type = 2
      let startTime = this.time()
      this.data.start_time = startTime
      this.data.campus_id = this.dataAddAudition.campus_id
      this.data.remark = this.dataAddAudition.getStkDesc
      this.data.customer_id = this.dataAddAudition.customerId
      this.data.business_id = this.dataAddAudition.businessId
      this.data.sale_employee_id = this.dataAddAudition.sale_employee_id,

      console.log(this.data,'------------this.data-----')
      console.log(this.dataAddAudition,'------------this.dataAddAudition---999--')

      console.log({
        'customer_id': this.data.customer_id,
        'business_id': this.data.business_id,
        'start_time': this.data.start_time,
        'sale_employee_id': this.data.sale_employee_id,
      })
      if(this.data.customer_id == '' || this.data.business_id == '' || this.data.start_time == '' || this.data.sale_employee_id == ''){
        this.$message.error('请将数据填写完整');
        return false
      }
      console.log(this.data,'-----------000--------------')
      // this.$emit('add-audition',this.data);
    }
  }
</script>
