<template>
  <div class="app-details-page" v-if="app">
    <ArrPanel class="app-details-container" v-if="app" border>
      <AppDetails :app="app" @change="handleDataChanged" />
    </ArrPanel>

    <ArrPanel class="app-number-container" v-if="app" border>
      <AppNumbers />
    </ArrPanel>
  </div>
</template>
<style lang="scss" scoped>
.app-details-page {
  display: flex;
  flex-direction: row;
  flex: 1;
  height: 230px;

  .app-details-container {
    flex: 1;
    padding-left: 50px;
  }

  .app-number-container {
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
  import AppNumbers from '~/components/app/light/AppNumbers.vue';

  const app = namespace('app')

  @Component({
    layout: 'AppEditor',
    mixins: [ AppDetailsMixin ],
    components: {
      AppDetailsMenu,
      AppDetails,
      MenuList,
      PageList,
      AppNumbers
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
      this.refresh()
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
