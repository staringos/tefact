<template>
  <div id="app">
    <Editor :target="target" />
  </div>
</template>

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
