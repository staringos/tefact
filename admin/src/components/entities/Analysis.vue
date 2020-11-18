<template>
  <div class="analysis-section">
    <div v-for="(field, i) in section.entity.entity_fields" class="analysis-field">
      <div class="number">{{section.entity.entity_data[field.key]}}</div>
      <div class="analysis-field-name">{{field.name}}</div>
    </div>
  </div>
</template>
<style lang="scss" scoped>
  .analysis-section {
    display: flex;

    .analysis-field {
      display: flex;
      width: 100px;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 30px;


      .number {
        font-weight: bold;
        font-size: 32px;
        margin-bottom: 20px;
      }

      .analysis-field-name {
        font-weight: 500;
        font-size: 18px;
      }
    }
  }
</style>
<script lang="ts">
  import { Vue, Component, Prop } from 'nuxt-property-decorator'
  import { EntityPageSection } from '~/services/common/entities/entities'

  @Component
  export default class AppItem extends Vue {
    @Prop() section!: EntityPageSection
  }
</script>
