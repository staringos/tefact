<template>
  <el-row style="background: #e2e3e6; padding: 20px;">
    <el-col :span="5">
      <el-input v-model="value.name" placeholder="按钮名" v-if="hasName"></el-input>
    </el-col>
    <el-col :span="5">
      <el-select v-model="value.type" placeholder="按钮类型">
        <el-option v-for="item in ButtonType" :key="item.key" :label="item.value" :value="item.key"></el-option>
      </el-select>
    </el-col>
    <el-col :span="5">
      <el-input v-model="value.link" placeholder="按钮链接" v-if="value.type !== 'dialog-list' && value.type !== 'dialog-details'"></el-input>
    </el-col>
    <el-col :span="5" v-if="value.type === 'dialog-list' || value.type === 'dialog-details'">
      <el-select v-model="value.entity_key" placeholder="弹框Entity">
        <el-option v-for="item in entities" :key="item.key" :label="item.name" :value="item.key"></el-option>
      </el-select>
    </el-col>
    <el-col :span="5" v-if="value.type === 'dialog-list' || value.type === 'dialog-details'">
      <el-input v-model="value.entity_params" placeholder="Entity参数"></el-input>
    </el-col>
  </el-row>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, Prop, Watch, Emit } from 'nuxt-property-decorator'
  import { Constants } from '~/services/common'

  @Component
  export default class ButtonForm extends Vue {
    @Prop(Array) entities
    @Prop(Boolean) hasName
    @Prop({ default: {} as any }) value

    ButtonType = Constants.entities.ButtonType

    @Watch('value')
    @Emit('input')
    valueChanged() {
      return this.value
    }
  }
</script>
