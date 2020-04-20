<template>
  <ul class="text-list">
    <li v-for="(attr, i) in attributes" :key="i">
      <span class="text-list-title">{{attr.key}}</span>
      <span class="value">{{attr.value}}</span>
    </li>
  </ul>
</template>
<style lang="scss" scoped>
  .text-list {
    width: 100%;
    margin-top: 20px;

    li {
      display: flex;
    }

    .text-list-title, .value {
      width: 100px;
      display: inline-block;
      font-size: 14px;
      font-weight: 400;
      color: rgba(23,23,37,1);
      line-height: 30px;
    }
  }
</style>
<script lang="ts">
  import { Component, Vue, Prop, Emit } from 'nuxt-property-decorator'

  @Component({
      name: 'ArrAttributeList'
  })
  export default class AttributeList extends Vue {
    @Prop([Array]) attributes
  }
</script>
