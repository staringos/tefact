<template>
  <div id="app">
    <Editor v-model="target" />
  </div>
</template>
<style lang="scss" scoped>
#app {
  display: flex;
  flex: 1;
  height: 100%;
  width: 100%;
}
</style>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Editor from "./components/index.vue";
import TestJSON from "./mock/test.json";

@Component({
  components: {
    Editor
  }
})
export default class App extends Vue {
  target = TestJSON;
}
</script>
