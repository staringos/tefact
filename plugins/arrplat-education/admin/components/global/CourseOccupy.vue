<!-- 添加占用弹窗 -->
<template>
    <el-dialog
      title="确认把该时间段设置为占用吗？"
      :visible.sync="dialogAddZy"
      width="40%"
      :before-close="handleAddZyClose">
      <el-form v-if="dialogAddZy" :model="addOccupy" :rules="infoRules" ref="addOccupy" class="alert_add_zsk" label-width="80px">
        <el-form-item prop="desc" label-width="100px" label="占用原因">
          <el-input type="textarea" v-model="addOccupy.desc"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
            <el-button @click="handleAddZyClose">取 消</el-button>
            <el-button type="primary" @click="handleAddZyTrue">确 定</el-button>
          </span>
    </el-dialog>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, Prop, Watch, Emit, namespace } from 'nuxt-property-decorator'
  import { infoRules } from '../../components/formRules'
  const edu = namespace('education')
  @Component({})
  export default class CourseOccupy extends Vue {
    @edu.Action curriculum
    @Prop() dialogAddZy: boolean
    infoRules: any = infoRules
    addOccupy: any = {
      desc : ''
    }

    // 添加占用弹窗关闭
    handleAddZyClose(){
      this.addOccupy.type = 'close'
      this.$emit('occupy-close',this.addOccupy);
    }
    // 添加占用弹窗确定
    handleAddZyTrue(){
      if(this.addOccupy.desc  == ''){
        return false
      }
      this.addOccupy.type = 'true'
      this.$emit('occupy-close',this.addOccupy);
    }
  }
</script>
