<template>
  <div class="data-source-editor">
    <div class="data-source-tabs">
      <DataSourceTab v-model="currentDataSource" />
<!--      <DataBaseTab />-->
      <DataTableTab v-model="currentTable" :tableList="tableList" />
    </div>
    <div class="entity-editor">
      <EntityEditor />
      <EntityPreview />
    </div>
  </div>
</template>
<style lang="scss" scoped>
  .data-source-editor {
    display: flex;
    flex-direction: row;
    flex: 1;

    .data-source-tabs {
      display: flex;
      flex-direction: column;
      width: 230px;
    }

    .entity-editor {
      flex: 1;
      flex-direction: column;
      display: flex;
    }
  }
</style>
<script lang="ts">
  import { Vue, Component, namespace, Watch } from 'nuxt-property-decorator'
  import DataSourceTab from "~/components/app/light/datasource/DataSourceTab.vue"
  import DataBaseTab from "~/components/app/light/datasource/DataBaseTab.vue"
  import DataTableTab from "~/components/app/light/datasource/DataTableTab.vue"
  import EntityPreview from "~/components/app/light/datasource/EntityPreview.vue"
  import EntityEditor from "~/components/app/light/datasource/EntityEditor.vue"

  const app = namespace('app')
  const dataSource = namespace('dataSource')

  @Component({
    layout: 'AppEditor',
    components: {
      EntityEditor,
      EntityPreview,
      DataTableTab,
      DataBaseTab,
      DataSourceTab,
    }
  })
  export default class DataSourceEditor extends Vue {
    id = ''
    currentDataSource = null
    currentTable = null
    tableList = []

    @app.Action getAppDetails
    @dataSource.Action getAllDataTable

    @Watch("currentDataSource")
    async onDataSourceChange() {
      const res = await this.getAllDataTable(this.currentDataSource);
      this.tableList = res.data.data
    }


    handleClick() {

    }

    handleRefresh() {
      this.refresh()
    }

    handleDataChanged() {

    }

    async refresh() {
    }

    async mounted() {
      this.refresh()
    }
  }
</script>
