<template>
  <div :class="{'slot-area': true, 'is-editing': !preview}" title="拖拽组件到这里">
    <p class="title" v-if="!preview && !child">插槽</p>
    <p class="desc" v-if="!preview && !child">拖拽组件到这里</p>
  </div>
</template>
<style lang="scss" scoped>
.slot-area {
  background-color: transparent;
  border: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  flex-direction: column;

  &.is-editing {
    background-color: #dce0e6;
    border: 1px dashed #9e9e9e;
    color: #9e9e9e;
  }

  .title {
    font-size: 12px;
  }

  .desc {
    font-size: 10px;
  }
}
</style>
<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component
export default class SlotArea extends Vue {
  @Prop() preview

  get child() {
    return null
  }
}
</script>
