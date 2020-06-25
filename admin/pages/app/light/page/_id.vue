<template>
  <div class="page-container">
    <Preview v-if="pageId" :id="pageId" @loaded="handleLoaded" />
  </div>
</template>
<style lang="scss">
  .page-container {
    display: flex;
    flex: 1;
    flex-direction: column;
  }
</style>
<script lang="ts">
  import { Vue, Component, namespace } from 'nuxt-property-decorator'
  import Page from '~/components/app/light/editor/Page.vue'
  import Preview from '~/components/app/light/Preview.vue'

  const app = namespace('app');

  @Component({
    layout: 'plugin',
    components: {
      Preview,
      Page
    }
  })
  export default class AppLightPage extends Vue {
    pageId: string | null = null

    @app.Action setCurrentAppId

    handleLoaded(app) {
      if (!app) return
      this.setCurrentAppId(app.application_id);
    }

    mounted() {
      this.pageId = this.$route.params.id
    }
  }
</script>
