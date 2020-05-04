<template>
  <BaseResolu title="位置大小" v-bind="$attrs">
    <div class="resolu-container" v-if="tmpNode">
      <div class="resolu-row">
        <span>位置:</span>
        <input type="number" class="resolu-input" v-model.number="tmpNode.config.x" @blur="handleSave" />
        <input type="number" class="resolu-input" v-model.number="tmpNode.config.y" @blur="handleSave" />
      </div>
      <div class="resolu-row">
        <span>大小:</span>
        <input type="number" class="resolu-input" v-model.number="tmpNode.config.w" @blur="handleSave" />
        <input type="number" class="resolu-input" v-model.number="tmpNode.config.h" @blur="handleSave" />
      </div>
    </div>
  </BaseResolu>
</template>
<style lang="scss" scoped>
  @import "../../../../../assets/styles/variables";

  .resolu-container {
    height: 80px;
    display: flex;
    flex-direction: column;

    .resolu-row {
      margin-bottom: 10px;
    }
  }

  .resolu-input {
    background: $gray-02;
    border: 0;
    height: 30px;
    padding-left: 10px;

    &:focus {
      outline-offset: 0;
      outline: none;
      border: 0;
    }
  }
</style>
<script lang="ts">
  import { Vue, Component, Prop, Watch, namespace } from "nuxt-property-decorator";
  import BaseResolu from '~/components/app/light/editor/resolu/BaseResolu.vue'
  import ResoluMixin from '~/components/app/light/editor/resolu/ResoluMixin'
  import ResoluBase from "~/components/app/light/editor/resolu/ResoluClass";
  import { BaseNodeModel } from "~/utils/entities/editor/node";

  const editor = namespace('editor')

  @Component({
    components: { BaseResolu },
    mixins: [ ResoluMixin ]
  })
  export default class PositionResolu extends Vue {
    tmpNode: BaseNodeModel | null = null

    @Prop() sectionId
    @Prop() nodeType
    @editor.Action modifyNode

    // @Watch('tmpNode.config', { immediate: true, deep: true })
    handleSave() {
      console.log('this.nodeType:', this.nodeType)
      if (this.nodeType === 'page') {
        return
      }

      if (this.nodeType === 'section') {
        return
      }

      this.modifyNode({ sectionId: null, node: this.tmpNode })
    }

    mounted() {
      console.log("tmpNode:", this.tmpNode)
    }
  }
</script>
