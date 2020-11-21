<template>
  <div class="app-wrapper">
    <HeaderBar direct="https://tefact.com" />
    <div class="main-container">
      <nuxt />
    </div>
  </div>
</template>
<style lang="scss" scoped>
.app-wrapper {
  flex-direction: column;

  .main-container {
    padding: 0;
  }
}
</style>
<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import HeaderBar from '../components/layout/UserAdmin/HeaderBar.vue'

@Component({
  components: {
    HeaderBar
  }
})
export default class UserAdmin extends Vue {}
</script>
