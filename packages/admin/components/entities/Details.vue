<template>
  <div class="details-section">
    <div class="params" v-if="!field.exists_type || field.exists_type.length === 0 || field.exists_type.indexOf('details') !== -1" v-for="(field, i) in entity.entity_fields" :key="i">
      <div class="params-title">{{field.name}}:</div>
      <div class="params-content">
        <DataDisplay :field="field" :data="entity.entity_data" v-if="entity.entity_data" />
      </div>
    </div>
  </div>
</template>
<style lang="scss" scoped>
  .details-section {
    display: flex;
    flex: 1;
    flex-wrap: wrap;
    align-content: flex-start;
    padding-left: 30px;

    .params {
      display: flex;
      flex: 0 0 50%;
      padding-bottom: 20px;

      .params-title {
        flex: 1;
        font-weight: 600;
      }

      .params-content {
        flex: 2;
      }
    }
  }

</style>
<script lang="ts">
  import { Component, Vue, Prop } from 'nuxt-property-decorator'
  import { Entity } from '@arrplat/common'
  import List from './List.vue'
  import DataDisplay from './DataDisplay.vue'

  @Component({
      components: { List, DataDisplay }
  })
  export default class PageSection extends Vue {
    @Prop() entity: Entity

    async mounted() {
      console.log('[mounted] page entity:', this.entity)
    }
  }
</script>
