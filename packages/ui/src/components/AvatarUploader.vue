<template>
  <el-upload
    class="avatar-uploader"
    :action="actionUrl"
    :show-file-list="false"
    :on-success="handleAvatarSuccess"
    :before-upload="beforeAvatarUpload">
    <el-avatar :size="size" :src="link"></el-avatar>
  </el-upload>
</template>
<script lang="ts">
  import { Avatar, Upload } from 'element-ui'
  import { Component, Prop, Vue, Emit } from 'nuxt-property-decorator'

  @Component({
    components: {
      [Avatar.name]: Avatar, [Upload.name]: Upload
    }
  })
  export default class AvatarUploader extends Vue {
    @Prop([String]) link?: string
    @Prop({ default: 12 }) size?: number
    @Prop([Function]) onUpload?: Function
    @Prop([String]) actionUrl?: string

    @Emit('onChange')
    handleAvatarSuccess(e) {
      return 'http://' + e[0]
    }

    beforeAvatarUpload(e) {
      console.log('beforeAvatarUpload e:', e)

    }
  }
</script>
