<template>
  <div class="app-editor-page" v-if="app">
    <ArrPanel class="page-item" v-if="app.menus" border>
      <MenuList @refresh="handleRefresh" :appId="app.id" :menus="app.menus" :pages="app.pages" :onChange="(value) => handleDataChanged('menus', value)" />
    </ArrPanel>
    <ArrPanel class="page-item" v-if="app" border>
      <PageList @refresh="handleRefresh" :appId="app.id" :pages="app.pages" :entities="app.entities" :onChange="(value) => handleDataChanged('pages', value)" />
    </ArrPanel>
  </div>
</template>
<style lang="scss" scoped>
  @import '../../../../assets/styles/app-edit.scss';

  .app-editor-page {
    .app-menu {
      flex-direction: column;
    }

    .app-attributes {
      display: flex;
    }
  }
</style>
<script lang="ts">
  import { Vue, Component, namespace } from 'nuxt-property-decorator'
  import AppDetails from "~/components/app/light/AppDetails.vue";
  import MenuList from "~/components/app/light/MenuList.vue";
  import PageList from "~/components/app/light/PageList.vue";
  import AppDetailsMenu from '~/components/app/light/AppDetailsMenu.vue';

  const app = namespace('app')

  @Component({
    layout: 'AppEditor',
    components: {
      AppDetailsMenu,
      AppDetails, MenuList, PageList
    }
  })
  export default class AppMenuPage extends Vue {
    id = ''
    app = {}

    @app.Action getAppDetails

    handleRefresh() {
      this.refresh()
    }

    handleDataChanged() {

    }

    async refresh() {
      this.id = this.$route.params.id
      const res = await this.getAppDetails(this.id)
      this.app = res.data.data
    }

    async mounted() {
      this.refresh()
    }
  }
</script>
