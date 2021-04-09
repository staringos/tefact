<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 1024 1024"
    width="100%"
    height="100%"
    version="1.1"
  >
    <path
      :style="getStyle()"
      d="M42.666667 896h938.666666L512 85.333333"
      fill=""
      p-id="6492"
    ></path>
  </svg>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import mixin from "./mixin";

@Component({
  mixins: [mixin],
})
export default class TriangleShape extends Vue {}
</script>
