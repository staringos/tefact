<template>
  <div class="app-details-page" v-if="app">
<!--    <AppDetailsMenu :app="app" />-->
    <div class="app-attributes">
      <ArrPanel v-if="app.menus" border>
        <MenuList @refresh="handleRefresh" :appId="app.id" :menus="app.menus" :pages="app.pages" :onChange="(value) => handleDataChanged('menus', value)" />
      </ArrPanel>
      <ArrPanel v-if="app" border>
        <PageList @refresh="handleRefresh" :appId="app.id" :pages="app.pages" :entities="app.entities" :onChange="(value) => handleDataChanged('pages', value)" />
      </ArrPanel>
    </div>
  </div>
</template>
<style lang="scss" scoped>
  .app-details-page {
    display: flex;
    flex-direction: row;
    height: 100%;

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
      console.log("refresh res:", res);
      this.app = res.data.data
    }

    async mounted() {
      console.log("mmmmmounted");
      this.refresh()
    }
  }
</script>
