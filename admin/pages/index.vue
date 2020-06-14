<template>
  <div class="container">
    <div>
      <h1 class="title">
        Tefact
      </h1>
      <h2 class="subtitle">
        An platform for union business system
      </h2>
    </div>
  </div>
</template>

<script lang="ts">
  import { Component, Vue, namespace, Watch } from 'nuxt-property-decorator'
  import Tools from '~/utils'
  const app = namespace('app')

  @Component({
      layout: 'UserAdmin'
  })
  export default class Index extends Vue {
    @app.Getter orgApps

    @Watch('orgApps')
    onAllAppsChanged() {
      this.jumpToFirstApp()
    }

    jumpToFirstApp() {
      const first = this.orgApps[0]
      first && Tools.gotoAppIndex(first, this.$router)
    }

    mounted() {
      this.jumpToFirstApp()
    }
  }
</script>

<style>
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
