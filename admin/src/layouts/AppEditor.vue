<template>
  <div class="app-wrapper">
    <EditorMenuBar />
    <el-row class="main">
      <HeaderBar title="应用编辑器" />
      <div class="main-container">
        <nuxt />
      </div>
    </el-row>
  </div>
</template>
<style lang="scss" scoped>
  .main-container {
    padding: 0;
    display: flex;
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace } from 'nuxt-property-decorator'
  import HeaderBar from '../components/layout/UserAdmin/HeaderBar.vue'
  import EditorMenuBar from '../components/layout/EditorMenuBar.vue'

  const app = namespace('app')

  @Component({
    components: {
      HeaderBar, EditorMenuBar
    }
  })
  export default class UserAdmin extends Vue {
    @app.Action('init') init:any

    @app.Getter currentOrg

    mounted () {
      this.init(this.currentOrg)
    }
  }
</script>
