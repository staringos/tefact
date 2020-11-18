<template>
  <div v-if="data">
    <div v-if="field.type === 2">
      <template v-for="(button, i) in data[field.key]">
        <el-button :key="i" size="small"
         v-if="button.button_type !== 1 && button.button_type !== 5"
         :type="button.button_type === 2 ? 'danger' : 'default'" round @click="handleBtnClick(button, data)"
        >{{button.name}}</el-button>
        <EntityButton :key="i" :button="button" :type="button.button_type === 1 ? 'modify' : 'add'"
          v-if="button.button_type === 1 || button.button_type === 5" :section="section"
          :data="data"
        />
      </template>
    </div>
    <a v-else-if="field.has_link" :href="wrapParams(field.link_address, data)">
      <DataDisplayValue :field="field" :data="data" />
    </a>
    <DataDisplayValue v-else :field="field" :data="data" />
  </div>
</template>
<script lang="ts">
  import { Component, Vue, Prop, namespace } from 'nuxt-property-decorator'
  import { EntityField } from '~/services/common/entities/entities'
  import List from './List.vue'
  import EntityModifier from './EntityModifier.vue'
  import EntityButton from './EntityButton.vue'
  import DataDisplayValue from './DataDisplayValue.vue'
  import { wrapParams, findPrimaryKey } from '~/utils'
  import { Confirm } from '~/components/ui'

  const entities = namespace('entities')
  const app = namespace('app')

  @Component({
    components: { List, EntityModifier, EntityButton, DataDisplayValue }
  })
  export default class DataDisplay extends Vue {
    @Prop() field!: EntityField
    @Prop() data: any
    @Prop() baseQueryParams: any
    @Prop() entityParams: any
    @Prop() section: any
    @Prop() refreshTable: any

    @app.Getter currentOrgIdGetter
    @entities.Action deleteRowData

    wrapParams = wrapParams

    public async handleBtnClick(button, row) {
      if (button.button_type === 2) {
        const primary = findPrimaryKey(this.section.entity.entity_fields)
        const id = this.data[primary]
        if (!id) return this.$message.error('实体对象没有设置主键，请联系系统管理员')

        return Confirm.deleteConfirm(this, '部门', () => this.deleteRowData({ id, orgId: this.currentOrgIdGetter, entityId: this.section.entity.id }))
            .then(() => this.refreshTable())
      }

      let link = button.link
      if (!link) this.$router.push(link)

      link = wrapParams(link, row)
      this.$router.push(link)
    }

    async mounted() {
    }
  }
</script>
