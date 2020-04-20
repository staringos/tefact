<template>
  <ArrPanel v-if="currentPageGetter" :title="currentPageGetter.title" border>
    <div class="page-wrapper" :style="`flex-direction: ${currentPageGetter.direction === 2 ? 'column' : 'row'}`">
      <PageSection :params="params" :section="section" :key="i" v-for="(section, i) in currentPageGetter.page_section"></PageSection>
    </div>
  </ArrPanel>
</template>
<style lang="scss">
  .page-wrapper {
    width: 100%;
    display: flex;
    flex-direction: row;
  }
</style>
<script lang="ts">
import { Component, Vue, namespace, Watch } from 'nuxt-property-decorator'
import { EntityPage } from '@arrplat/common'
import PageSection from '~/components/entities/PageSection.vue'

const entities = namespace('entities')
const app = namespace('app')

@Component({
  components: { PageSection },
  layout: 'plugin'
})
export default class Page extends Vue {
  @entities.Action getPageData
  @entities.Getter currentPageGetter

  @app.Action setCurrentAppId
  @app.Getter currentOrgIdGetter
  params: any = {}

  @Watch('$route.params')
  onParamsChange() {
    console.log('this.$route.params:', this.$route.params)
    this.refreshPage()
  }

  async refreshPage() {
    let key = this.$route.params.key
    this.params = this.$route.query
    if (!key) return

    const loading = this.$loading({
        lock: true,
        text: '加载中...',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
    })

    await this.getPageData({ key, params: this.params, orgId: this.currentOrgIdGetter })

    loading.close()
  }

  async mounted() {
    this.refreshPage()
  }
}
</script>
