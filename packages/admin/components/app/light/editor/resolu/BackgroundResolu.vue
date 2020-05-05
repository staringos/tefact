<template>
  <BaseResolu title="背景设置" v-bind="$attrs">
    <div class="resolu-container" v-if="tmpNode">
      <div class="resolu-row">
        <div class="resolu-label">背景色</div>
        <el-color-picker v-model="tmpNode.config.style['background-color']" @change="handleSave" show-alpha></el-color-picker>
      </div>
    </div>
  </BaseResolu>
</template>
<style lang="scss">
  @import "./resolu";
</style>
<script lang="ts">
  import { Vue, Component } from "nuxt-property-decorator";
  import BaseResolu from '~/components/app/light/editor/resolu/BaseResolu.vue'
  import { BaseNodeModel } from "~/utils/entities/editor/node";
  import ResoluMixin from '~/components/app/light/editor/resolu/ResoluMixin'
  import ResoluBase from "~/components/app/light/editor/resolu/ResoluClass";

  @Component({
    components: {
      BaseResolu
    },
    mixins: [ ResoluMixin ]
  })
  export default class BackgroundResolu extends ResoluBase {
  }
</script>
