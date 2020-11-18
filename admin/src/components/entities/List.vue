<template>
  <div v-if="currentEntity" class="list-wrapper">
    <div class="list-header clearfix">
      <EntityButton type="add" :section="section" />
      <EntityModifier
        :baseQueryParams="baseQueryParams"
        :entityParams="currentEntityParams"
        :entityObj="currentEntity"
        :entityParamsStr="currentEntityParams"
        :sectionId="section ? section.id : null"
      />
    </div>
    <Search :section="section" v-if="hasSearch" :onSearch="handleSearch" :value="baseQueryParams.searchCondition ? baseQueryParams.searchCondition.value : {}" />
    <el-table
      :data="currentEntity.entity_data"
      border
      style="flex: 1;"
      @sort-change="handleSortChange"
      v-loading="loading"
    >
      <el-table-column
        v-for="(field, i) in currentEntity.entity_fields"
        v-if="field.exists_type.indexOf('list') !== -1"
        :key="i"
        :prop="field.key"
        :sortable="field.has_sort && 'custom'"
        :label="field.name">
        <template slot-scope="scope">
          <DataDisplay
            :refreshTable="refreshTable"
            :field="field"
            :data="scope.row"
            :baseQueryParams="baseQueryParams"
            :entityParams="entityParams"
            :section="section"
          />
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      background
      layout="prev, pager, next"
      @current-change="handlePageChanged"
      :page-size="baseQueryParams.page.size"
      v-if="currentEntity.page"
      :total="currentEntity.page.total_count">
    </el-pagination>
  </div>
</template>
<style lang="scss">
  .list-wrapper {
    display: flex;
    flex-direction: column;
    flex: 1;
    width: 100%;

    .list-header {
      .entity-modifier {
        float: right;
        margin-bottom: 20px
      }
    }
  }
</style>
<style lang="scss" scoped>
  .text {
    text-stroke: 1px #31261d;
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace, Prop, Watch } from 'nuxt-property-decorator'
  import { Entity, EntityPageSection } from '~/services/common/entities/entities'
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
    tmpEntity: Entity | null = null
    loading: boolean = false

    @Prop() entity!: Entity
    @Prop() section!: EntityPageSection
    @Prop() params: any
    @Prop() entityParams: any

    @Prop() entityId!: string | null
    @Prop() searchCondition!: string | null
    @Prop() orderCondition!: string | null

    @entities.Action getEntityData

    get currentEntityParams() {
      if (this.section) return this.section.entityParams
      return this.entityParams
    }

    get currentEntity() {
      if (this.entity) return this.entity
      return this.tmpEntity
    }

    get hasSearch() {
      if (!this.currentEntity) return false
      return this.currentEntity.entity_fields.filter(item => item.has_search).length > 0
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
        pageSectionId: this.section?.id,
        orgId: this.currentOrgIdGetter
      })
    }

    public handlePageChanged(page) {
      this.baseQueryParams.page.page = page
      this.refreshTable()
    }

    get searchParams() {
      return {}
    }

    get pageParams() {
      return {}
    }

    get orderParams() {
      return {}
    }

    @Watch("entityId")
    entityIdChange() {
      if (this.entityId) this.init()
    }

    public async init() {
      if (this.entity || !this.entityId) return

      this.loading = true
      const res = await this.getEntityData({
        id: this.entityId,
        search_params: this.searchParams,
        page_params: this.pageParams,
        order_params: this.orderParams
      });
      this.loading = false

      this.tmpEntity = res.data.data;
    }

    public mounted() {
      this.init()
    }
  }
</script>
