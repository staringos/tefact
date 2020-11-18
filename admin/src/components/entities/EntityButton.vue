<template>
  <div class="entity-modifier">
    <el-button
      v-if="section.section_type === 9 && section.has_add_btn"
      @click="handleOpen"
      type="primary" round size="small"
    >{{button && button.name ? button.name : '添加'}}</el-button>
  </div>
</template>
<script lang="ts">
  import { Component, Vue, Prop, namespace, Watch } from 'nuxt-property-decorator'
  import { EntityPageSection } from '~/services/common/entities/entities'
  import List from './List.vue'
  import DataDisplay from './DataDisplay.vue'

  const entities = namespace('entities')
  const app = namespace('app')

  @Component({
    components: { List, DataDisplay }
  })
  export default class EntityButton extends Vue {
    @Prop() section!: EntityPageSection
    @Prop() data: any
    @Prop({ default: 'add' }) type: 'add' | 'modify' | undefined
    @Prop() button: any

    @entities.Action toggleModifyDialog

    async handleOpen() {
      this.toggleModifyDialog({ status: true, data: this.data })
    }
  }
</script>
