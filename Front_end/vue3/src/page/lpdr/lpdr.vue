<template>
  <div class="ordering">
    <el-upload
    class="upload-demo"
    drag
    action="http://127.0.0.1:5000/upload"
    multiple
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      Drop file here or <em>click to upload</em>
    </div>
    <template #tip>
      <div class="el-upload__tip">
        jpg/png files with a size less than 500kb
      </div>
    </template>
  </el-upload>
  </div>

</template>

<script lang="ts" setup>
import { UploadFilled } from '@element-plus/icons-vue'
</script>

<style scoped>

</style>