<template>
  <div class="data-source-editor">
    <div class="data-source-tabs">
      <DataSourceTab />
      <DataBaseTab />
      <DataTableTab />
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
  import { Vue, Component, namespace } from 'nuxt-property-decorator'
  import DataSourceTab from "~/components/app/light/datasource/DataSourceTab.vue"
  import DataBaseTab from "~/components/app/light/datasource/DataBaseTab.vue"
  import DataTableTab from "~/components/app/light/datasource/DataTableTab.vue"
  import EntityPreview from "~/components/app/light/datasource/EntityPreview.vue"
  import EntityEditor from "~/components/app/light/datasource/EntityEditor.vue"

  const app = namespace('app')

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
    tableData: Object[] = [{
      date: '2016-05-03',
      name: '王小虎',
      address: '上海市普陀区金沙江路 1518 弄'
    }, {
      date: '2016-05-02',
      name: '王小虎',
      address: '上海市普陀区金沙江路 1518 弄'
    }, {
      date: '2016-05-04',
      name: '王小虎',
      address: '上海市普陀区金沙江路 1518 弄'
    }, {
      date: '2016-05-01',
      name: '王小虎',
      address: '上海市普陀区金沙江路 1518 弄'
    }, {
      date: '2016-05-08',
      name: '王小虎',
      address: '上海市普陀区金沙江路 1518 弄'
    }, {
      date: '2016-05-06',
      name: '王小虎',
      address: '上海市普陀区金沙江路 1518 弄'
    }, {
      date: '2016-05-07',
      name: '王小虎',
      address: '上海市普陀区金沙江路 1518 弄'
    }]

    @app.Action getAppDetails

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
