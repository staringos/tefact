<template>
  <div class="app-wrapper">
    <AppBar />
    <el-row class="main">
      <HeaderBar />
      <div class="main-container">
        <nuxt />
      </div>
    </el-row>
  </div>
</template>
<style lang="scss" scoped>
  .main-container {
    padding: 0;
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace } from 'nuxt-property-decorator'
  import HeaderBar from '../components/layout/UserAdmin/HeaderBar.vue'
  import AppBar from '../components/layout/UserAdmin/AppBar.vue'

  const app = namespace('app')

  @Component({
      components: {
        HeaderBar, AppBar
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
