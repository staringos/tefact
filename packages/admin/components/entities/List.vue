<template>
  <div>
    <div class="list-header clearfix">
      <EntityButton type="add" :section="section" />
      <EntityModifier :baseQueryParams="baseQueryParams" :entityParams="entityParams" :entityObj="section.entity" :entityParamsStr="section.entity_params" :sectionId="section.id" />
    </div>
    <Search :section="section" v-if="hasSearch" :onSearch="handleSearch" :value="baseQueryParams.searchCondition ? baseQueryParams.searchCondition.value : {}" />
    <el-table
      :data="entity.entity_data"
      border
      style="width: 100%;"
      @sort-change="handleSortChange">
      <el-table-column
        v-for="(field, i) in entity.entity_fields"
        v-if="field.exists_type.indexOf('list') !== -1"
        :key="i"
        :prop="field.key"
        :sortable="field.has_sort && 'custom'"
        :label="field.name">
        <template slot-scope="scope">
          <DataDisplay :refreshTable="refreshTable" :field="field" :data="scope.row" :baseQueryParams="baseQueryParams" :entityParams="entityParams" :section="section" />
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      background
      layout="prev, pager, next"
      @current-change="handlePageChanged"
      :page-size="baseQueryParams.page.size"
      v-if="entity.page"
      :total="entity.page.total_count">
    </el-pagination>
  </div>
</template>
<style lang="scss">
  .list-header {
    .entity-modifier {
      float: right;
      margin-bottom: 20px
    }
  }
</style>
<style lang="scss" scoped>
  .text {
    text-stroke: 1px #31261d;
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace, Prop } from 'nuxt-property-decorator'
  import { Entity, EntityPageSection } from '@arrplat/common'
  import DataDisplay from '~/components/entities/DataDisplay.vue'
  import EntityModifier from '~/components/entities/EntityModifier.vue'
  import EntityButton from '~/components/entities/EntityButton.vue'
  import Search from './Search.vue'

  const entities = namespace('entities')
  const app = namespace('app')

  @Component({
    components: { DataDisplay, EntityModifier, EntityButton, Search }
  })
  export default class List extends Vue {
    @Prop() entity: Entity
    @Prop() section: EntityPageSection
    @Prop() params: any
    @Prop() entityParams: any

    get hasSearch() {
      return this.entity.entity_fields.filter(item => item.has_search).length > 0
    }

    baseQueryParams = {
      page: {
          page: 1,
          size: 20
      },
      searchCondition: null as any,
      sort: null as any
    }

    @entities.Action querySectionData
    @app.Getter currentOrgIdGetter

    public handleSortChange(column, prop, order)  {
      console.log('column:', column, 'prop:', prop, 'order:', order)
      this.baseQueryParams.sort = {
        "field_name": column.prop,
        "order": column.order === 'ascending' ? 'asc' : 'desc'
      }
      this.refreshTable()
    }

    public handleSearch(condition) {
      const params = this.baseQueryParams
      params.searchCondition = condition
      return this.refreshTable()
    }

    public refreshTable() {
      this.querySectionData({
          ...this.baseQueryParams,
          pageSectionId: this.section.id,
          orgId: this.currentOrgIdGetter
      })
    }

    public handlePageChanged(page) {
      this.baseQueryParams.page.page = page
      this.refreshTable()
    }
  }
</script>
