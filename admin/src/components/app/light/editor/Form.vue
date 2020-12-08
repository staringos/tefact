<template>
  <el-form class="form-page" :style="{width: config.w, height: config.h}">
    <FormItem v-for="(item, key) in form.config.items" :key="key" :item="item" />
    <el-form-item>
      <el-button type="primary" @click="handleSubmit">立即创建</el-button>
      <el-button>取消</el-button>
    </el-form-item>
  </el-form>
</template>
<style lang="scss">
.form-page {
  display: flex;
  flex-direction: column;
  flex: 1;
}
</style>
<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { FormModel } from '~/utils/entities/editor/form'
import FormItem from '~/components/app/light/editor/FormItem.vue'
import cloneDeep from 'lodash/cloneDeep'

@Component({
  components: { FormItem }
})
export default class Form extends Vue {
  @Prop() form!: FormModel
  @Prop() value!: any

  tmpValue = {}

  get config() {
    return this.form.config || {}
  }

  handleSubmit() {}

  handleFormChange() {
    const { config } = this.form

    if (this.value) {
      this.tmpValue = cloneDeep(this.value);
      return;
    }

    if (config && config.defaultForm) {
      this.tmpValue = cloneDeep(config.defaultForm)
    }
  }
}
</script>
