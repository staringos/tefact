<template>
  <ul class="message-list">
    <li class="item" v-for="(message, i) in messages" :key="i" @click="() => handleReadMessage(message)">
      <div class="icon">
        <i class="el-icon-message"></i>
      </div>
      <div class="content">
        <h3 class="title">{{message.title}}</h3>
        <h4>{{message.content}}</h4>
      </div>
      <el-badge is-dot v-if="message.is_read === 0"></el-badge>
    </li>
  </ul>
</template>
<style lang="scss" scoped>
  @import "../../assets/styles/variables";
  .message-list {
    width: 350px;
    margin-bottom: 15px;
    max-height: 250px;
    overflow: auto;

    .item {
      width: 100%;
      height: 55px;
      margin-top: 10px;
      padding: 10px;
      display: flex;
      align-items: center;
      cursor: pointer;

      &:hover {
        background: $defaultHover;
      }

      .icon {
        width: 30px;
      }

      .content {
        flex-grow: 1;

        .title {
          font-size: 14px;
          font-weight: 700;
        }
      }
    }
  }
</style>
<script lang="ts">
  import { Component, Vue, namespace, Emit } from 'nuxt-property-decorator'
  import { Message } from '@arrplat/common'

  const user = namespace('user')

  @Component
  export default class MessageList extends Vue {
    page: number = 1
    page_size: number = 20
    messages: Message[] = []

    @user.Action getMessage
    @user.Action readMessage

    @Emit('onDataRefresh')
    async refreshList() {
      const res = await this.getMessage({ page: this.page, page_size: this.page_size, has_detail: 1 })
      const data = res.data.data
      this.messages = data.message_list
      return data.unread_count
    }

    async handleReadMessage(message) {
      if (message.is_read === 1) return

      const res = await this.readMessage(message.id)
      if (res.status === 200) {
        this.refreshList()
      }
    }

    mounted() {
      this.refreshList()
    }
  }
</script>
