<template>
  <div class="app-details-page" v-if="app">
    <AppDetailsMenu :app="app"/>
    <ArrPanel class="app-details-container" v-if="app" border>
      <AppDetails :app="app" :onChange="(value) => handleDataChanged(null, value)" />
    </ArrPanel>
  </div>
</template>
<style lang="scss" scoped>
.app-details-page {
  display: flex;
  flex-direction: row;
  height: 100%;
  flex: 1;

  .app-details-container {
    flex: 1;
  }

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
  import AppDetailsMixin from "~/components/app/light/AppDetailsMixin";
  import MenuList from "~/components/app/light/MenuList.vue";
  import PageList from "~/components/app/light/PageList.vue";
  import AppDetailsMenu from '~/components/app/light/AppDetailsMenu.vue';

  const app = namespace('app')

  @Component({
    layout: 'AppEditor',
    mixins: [ AppDetailsMixin ],
    components: {
      AppDetailsMenu,
      AppDetails, MenuList, PageList
    }
  })
  export default class AppItem extends Vue {
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
