<template>
  <ul class="list">
    <li :class="`list-item ${item.id === active ? 'active' : ''}`" v-for="item in list" @click="handleItemClick(item.id)">
      {{item.name}}
      <div class="right-area">
        <slot name="right" :data="item"></slot>
      </div>
    </li>
  </ul>
</template>
<style lang="scss" scoped>
  @import "../theme/variables";

  .list {
    display: flex;
    width: 100%;
    flex-direction: column;
    overflow: auto;
    max-height: 100%;

    .list-item {
      width: 100%;
      height: 40px;
      line-height: 40px;
      padding-left: 20px;

      &:hover {
        background-color: $defaultHover;

        .right-area {
          display: block;
        }
      }

      &.active {
        background-color: $defaultHover;
        border-right: 3px solid $mainColor;
      }

      .right-area {
        float: right;
        display: none;
      }
    }
  }
</style>
<script lang="ts">
  import { Vue, Component, Prop, Watch } from 'nuxt-property-decorator'

  export interface ListEntity {
    id: string
    name: string
  }

  @Component({
    name: 'ArrList'
  })
  export default class List extends Vue {
    @Prop([Array]) list
    @Prop([String]) active

    handleItemClick(id) {
      this.$emit('update:active', id)
    }
  }
</script>
