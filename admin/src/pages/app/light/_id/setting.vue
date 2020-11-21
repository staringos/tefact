<template>
  <div class="app-details-page" v-if="app">
    <ArrPanel class="app-details-container" v-if="app" border>
      <AppDetails :app="app" @change="handleDataChanged" />
    </ArrPanel>
  </div>
</template>
<style lang="scss" scoped>
.app-details-page {
  display: flex;
  flex-direction: row;
  flex: 1;
  height: 230px;
}
</style>
<script lang="ts">
import { Vue, Component, namespace } from 'nuxt-property-decorator'

@Component({
  layout: 'AppEditor'
})
export default class AppItem extends Vue {

}
</script>
