<template>
  <Page v-if="currentPage" :page="currentPage" :pageId="id" :preview="true" />
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, namespace, Prop, Emit, Watch } from 'nuxt-property-decorator'
  import Page from '~/components/app/light/editor/Page.vue'

  const editor = namespace('editor')

  @Component({
    components: { Page }
  })
  export default class PagePreview extends Vue {
    currentPage = null
    @Prop(String) id!: string

    @editor.Action getPageDetails


    @Emit('loaded')
    async init() {
      if (!this.id) return
      let loading = this.$loading({ fullscreen: true })
      this.currentPage = await this.getPageDetails(this.id)
      loading.close()

      return this.currentPage
    }

    @Watch('id')
    async handleIdChanged() {
      await this.init()
    }

    async mounted() {
      await this.init()
    }
  }
</script>
