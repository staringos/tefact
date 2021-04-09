<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="100%"
    height="100%"
    version="1.1"
  >
    <rect :style="getStyle()" width="100%" height="100%" />
  </svg>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import mixin from "./mixin";

@Component({
  mixins: [mixin],
})
export default class RectShape extends Vue {}
</script>
