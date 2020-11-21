<template>
  <div class="page-content">
    <Page :page="page" :pageId="page.id" :preview="true" />
  </div>
</template>
<style lang="scss">
  .page-content {
    width: 100%;
    height: auto;
    min-height: 100%;
  }
</style>
<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import Page from '~/components/app/light/editor/Page.vue'

@Component({
  components: {
    Page
  }
})
export default class AppItem extends Vue {
  @Prop(Object) page
}
</script>
