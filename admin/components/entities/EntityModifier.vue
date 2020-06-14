<template>
  <div class="entity-modifier">
    <el-dialog
      title="提示"
      :visible.sync="modifyDialogGetter"
      width="50%"
      :before-close="handleClose">
      <el-form v-if="entity" ref="form" :model="form" :rules="rules" label-width="150px">
        <FieldFormItem :form="form" :entity="entity" @change="handleFormChange" where="modify" />
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
          <el-button @click="handleClose">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
<script lang="ts">
  import { Component, Vue, Prop, namespace, Watch, Emit } from 'nuxt-property-decorator'
  import { EntityPageSection, Entity } from '~/services/common'
  import { wrapParamsObject, findPrimaryKey } from '~/utils'
  import List from './List.vue'
  import DataDisplay from './DataDisplay.vue'
  import FieldFormItem from '~/components/entities/FieldFormItem.vue'

  const entities = namespace('entities')
  const app = namespace('app')

  @Component({
    components: {FieldFormItem, List, DataDisplay }
  })
  export default class EntityModifier extends Vue {
    // @Prop(EntityPageSection) section: EntityPageSection
    @Prop(Object) entityObj!: Entity
    @Prop(String) entityParamsStr: string | undefined
    @Prop(String) sectionId: string | undefined

    @Prop() entityParams: any
    @Prop() baseQueryParams: any
    @Prop() button: any
    @Prop(String) entityKey: string | undefined

    @entities.Action getEntityConfig
    @entities.Action pageModifier
    @entities.Action querySectionData
    @entities.Action toggleModifyDialog
    @app.Getter currentOrgIdGetter
    @entities.Getter modifyDialogGetter
    @entities.Getter modifyDataGetter

    entity!: Entity
    rules = {}
    form: any = {}

    handleFormChange (form) {
      this.form = { ...form }
    }

    async buildRules() {
      if (!this.entity) return

      const rules = {}
      const that = this
      await this.entity.entity_fields.map(field => {
        rules[field.key] = { validator: (rule, value, callback) => that.validator(rule, value, callback, field), trigger: 'blur' }
      })

      this.rules = rules
    }

    validator(rule, value, callback, field) {
      if (field.verify_require) {
        if (!value || value.length < 1)
          return callback(new Error(`请输入${field.name}！`));
      }

      if (field.verify_max && field.verify_max !== -1) {
        if (typeof value === 'string' && value.length > field.verify_max
            || typeof value === 'number' && value > field.verify_max) {
          return callback(new Error(`${field.name}字段最大${value === 'string' ? '长度' : '值'}为${field.verify_max}！`));
        }
      }

      if (field.verify_min && field.verify_min !== -1) {
        if (typeof value === 'string' && value.length < field.verify_min
            || typeof value === 'number' && value < field.verify_min) {
          return callback(new Error(`${field.name}字段最小${value === 'string' ? '长度' : '值'}为${field.verify_min}！`));
        }
      }

      if (field.verify_only) {}
      if (field.verify_pattern) {
        const reg = new RegExp(field.verify_pattern)
        if (!reg.test(value)) {
          return callback(new Error(`${field.name}字段格式错误，请输入正确的值！`));
        }
      }

      return callback()
    }

    async handleSubmit() {
      const $form = this.$refs['form'] as any

      $form.validate(async (valid) => {
        if (!valid) return
        this.submit()
      })
    }

    @Emit('onChanged')
    async submit() {
      let sendParams = { ...this.form }

      if (this.entityParamsStr) {
          const extract = wrapParamsObject(this.entityParamsStr, this.entityParams)
          if (extract) sendParams = { ...extract, ...sendParams }
      }

      const attr = { entityId: this.entity.id, params: sendParams } as any
      const primary = findPrimaryKey(this.entity.entity_fields) // this.section.entity.entity_fields.filter(res => res.is_primary)

      if (primary && (this.modifyDataGetter[primary] || sendParams[primary])) {  // If modify, add ID
          attr.dataId = this.modifyDataGetter[primary] ? this.modifyDataGetter[primary] : sendParams[primary] // To support the data exists in modifyData or entity_params
          delete sendParams[primary]
      }

      if (this.entity.has_connect_org) {
          attr.params.org_id = this.currentOrgIdGetter
      }

      const res = await this.pageModifier(attr)

      if (res.status === 200) {
        this.$message({ message: '操作成功', type: 'success' })
        this.handleClose()
        if (this.sectionId)
          this.querySectionData({ orgId: this.currentOrgIdGetter, pageSectionId: this.sectionId, ...this.baseQueryParams, params: this.entityParams })

        return { success: true, data: sendParams }
      }

      this.$message({ message: '修改失败', type: 'success' })
      this.toggleModifyDialog({ status: false })
      return { success: false, msg: res }
    }

    async handleClose() {
      this.toggleModifyDialog({ status: false })
      this.form = {}
    }

    @Watch('modifyDataGetter')
    onModifyDataChange() {
      const modifyData = this.modifyDataGetter
      const form = {}
      for (let key in modifyData) {
        const field = this.entity.entity_fields.filter(field => field.key === key)[0]

        if (!field || !field.exists_type || field.exists_type.indexOf('modify') === -1) continue
        const cur = modifyData[key]

        if (field.data_type === 'dict') {
          form[key] = cur + ''
          continue
        }

        if (typeof cur === 'object' && cur.key) {
          form[key] = cur.key
          continue
        }
        form[key] = cur
      }

      this.form = form
    }

    async initEntityConfig() {
      const res = await this.getEntityConfig(this.entityKey)
      this.entity = res.data.data
      this.buildRules()
    }

    @Watch('entityObj')
    handleEntityObjChange() {
      if (this.entityObj) {
        this.entity = this.entityObj
        this.buildRules()
      }
    }

    initForm() {
      if (this.entity) this.buildRules()
      if (this.entityObj) this.entity = this.entityObj
      if (!this.entityObj && this.entityKey) this.initEntityConfig()
    }

    mounted() {
      this.initForm()
    }
  }
</script>
