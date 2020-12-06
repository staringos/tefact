<template>
  <div class="container">
    <div>
      <h1 class="title">
        Tefact
      </h1>
      <h2 class="subtitle">
        Build your application without code!
      </h2>
      <p>
        <el-button type="primary" plain>
          <a href="/auth?register">免费注册</a>
        </el-button>
        <el-button type="info" plain>
          <a href="/auth">去登录</a>
        </el-button>
      </p>
      <p class="loading">
        <i class="el-icon-loading"></i>
      </p>
    </div>
  </div>
</template>

<script lang="ts">
  import { Component, Vue, namespace, Watch } from 'nuxt-property-decorator'
  import Tools from '~/utils'
  const app = namespace('app')

  @Component({})
  export default class Index extends Vue {
    @app.Getter orgApps
    @app.Action('init') init:any

    @Watch('orgApps', { immediate: true })
    onAllAppsChanged() {
      this.jumpToFirstApp()
    }

    jumpToFirstApp() {
      const first = this.orgApps[0]
      if (first)
        return Tools.gotoAppIndex(first, this.$router)
    }

    mounted() {
      this.init()
    }
  }
</script>

<style lang="scss" scoped>
/* Sample `apply` at-rules with Tailwind CSS
.container {
  @apply min-h-screen flex justify-center items-center text-center mx-auto;
}
*/
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;

  a {
    text-decoration: none;
    color: inherit;
  }

  .el-icon-loading {
    text-align: center;
    font-size: 52px;
  }

  .loading {
    margin-top: 22px;
  }
}

.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}
</style>
