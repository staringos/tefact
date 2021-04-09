<template>
  <div id="app">
    <Editor v-if="target" v-model="target" />
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
import Mock from "./mock";
import getQueryVariable from "../../utils/src/getQueryParameters";

@Component({
  components: {
    Editor
  }
})
export default class App extends Vue {
  target = null;

  beforeMount() {
    const target = getQueryVariable("target");
    const key = target ? target : "page";
    this.target = Mock[key];
  }
}
</script>
