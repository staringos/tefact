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
      d="M512 0c282.781538 0 512 229.218462 512 512S794.781538 1024 512 1024s-512-229.218462-512-512S229.218462 0 512 0z"
      p-id="5586"
    ></path>
  </svg>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import mixin from "./mixin";

@Component({
  mixins: [mixin],
})
export default class CircleShape extends Vue {}
</script>
