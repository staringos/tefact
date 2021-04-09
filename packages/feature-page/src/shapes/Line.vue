<template>
  <div width="100%" height="100%" :style="lineStyle"></div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import mixin from "./mixin";

@Component({
  mixins: [mixin],
})
export default class StarShape extends Vue {
  get lineStyle() {
    return {
      ...(this as any).style,
      width: "100%",
      height: "100%",
    };
  }
}
</script>
