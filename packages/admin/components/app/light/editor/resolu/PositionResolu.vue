<template>
  <BaseResolu title="位置大小" v-bind="$attrs">
    <div class="resolu-container" v-if="tmpNode">
      <div class="resolu-row">
        <div class="resolu-label">位置</div>
        <input type="number" class="resolu-input" v-model.number="tmpNode.config.x" @blur="handleSave" />
        <input type="number" class="resolu-input" v-model.number="tmpNode.config.y" @blur="handleSave" />
      </div>
      <div class="resolu-row">
        <div class="resolu-label">大小</div>
        <input type="number" class="resolu-input" v-model.number="tmpNode.config.w" @blur="handleSave" />
        <input type="number" class="resolu-input" v-model.number="tmpNode.config.h" @blur="handleSave" />
      </div>
    </div>
  </BaseResolu>
</template>
<style lang="scss" scoped>
  @import "./resolu";
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
  export default class PositionResolu extends ResoluBase {
    @Prop() sectionId

    mounted() {}
  }
</script>
