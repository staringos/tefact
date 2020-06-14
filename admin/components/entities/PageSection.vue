<template>
  <div class="page-section">
    <div class="title-bar">
      <h3 class="page-section-title">{{section.title}}</h3>
    </div>
    <Details :entity="section.entity" :pageSectionId="section.id"
      v-if="section.section_type === 'details' || section.section_type === 3"></Details>
    <Analysis :section="section" v-else-if="section.section_type === 'analysis' || section.section_type === 10" />
    <List :section="section" :entityParams="entityParams" :entity="section.entity"
          v-else-if="!section.section_type || section.section_type === 'list' || section.section_type === 9"></List>
  </div>
</template>
<style lang="scss">
  @import "../../assets/styles/variables";

  .page-section {
    .title-bar {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      align-items: center;
    }

    .page-section-title {
      margin-bottom: 20px;
      border-left: 5px solid $mainColor;
      padding-left: 10px;
      font-weight: 500;
    }

    margin-top: 20px;
    margin-bottom: 50px;
  }
</style>
<script lang="ts">
  import { Component, Vue, Prop } from 'nuxt-property-decorator'
  import { EntityPageSection } from '~/services/common'
  import { extractParams } from '~/utils'
  import List from './List.vue'
  import Details from './Details.vue'
  import Analysis from '~/components/entities/Analysis.vue';

  @Component({
    components: {Analysis, List, Details }
  })
  export default class PageSection extends Vue {
    @Prop() section: EntityPageSection = {} as any
    @Prop() params: any

    get entityParams () {
      let params = {}

      if (params && this.section.entity_params) {
        const extract = extractParams(this.section.entity_params, this.params)
        params = { ...extract }
      }
      return params
    }
  }
</script>
