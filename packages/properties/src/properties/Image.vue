<template>
  <BaseProperties title="图片设置" v-bind="$attrs">
    <span>This is Position </span>
  </BaseProperties>
</template>
<style lang="scss"></style>
<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import BaseProperties from "./Base.vue";

@Component({
  components: { BaseProperties },
})
export default class ImageProperties extends Vue {}
</script>
