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
      d="M512 271.232C376.32 67.712 104.96 186.8288 104.96 408.5248c0 149.98016 135.50592 256.95232 237.44 337.60256 105.92768 83.79904 135.68 101.76 169.6 135.68 33.92-33.92 62.27456-53.66272 169.6-135.68 103.39328-78.97088 237.44-189.25568 237.44-339.21024C919.04 186.8288 647.68 67.712 512 271.232"
      p-id="4853"
    ></path>
  </svg>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import mixin from "./mixin";

@Component({
  mixins: [mixin],
})
export default class StarShape extends Vue {}
</script>
