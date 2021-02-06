<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" />
    <Editor />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Editor from "./components/index.vue";

@Component({
  components: {
    Editor
  }
})
export default class App extends Vue {}
</script>
