<template>
  <div class="meeting-item">
    <h3>{{meeting.name}}</h3>
    <div class="meeting-details">
      <span>{{meeting.date}}</span>
      <span>{{meeting.long}}</span>
      <span>{{meeting.people}} 人</span>
    </div>
    <p>{{meeting.room.name}}</p>
  </div>
</template>
<style lang="scss" scoped>
  .meeting-item {
    display: block;
    width: 100%;
    height: 50px;
    border-bottom: 1px solid #333;

    .meeting-details {
      color: #999;
    }
  }

</style>
<script lang="ts">
  import { Component, Vue, Prop } from 'nuxt-property-decorator'
  import { Header, Button, Search } from 'mint-ui'
  import 'mint-ui/lib/style.css'

  console.log('Header:', Header, Button)

  @Component({
      components: { Header, Button, Search }
  })
  export default class UIndex extends Vue {
    @Prop() meeting
  }
</script>
