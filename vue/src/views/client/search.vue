<template>
  <!-- 这个别删 删了不会换行 -->
  <el-space direction="vertical" alignment="normal">
    <el-input id="searchInput" v-model="searchFood" placeholder="请输入配料名称" @keyup.enter="onParsing">
      <template #append>
        <el-button :icon="Search" @click="onParsing" :loading="isParingIng">搜索</el-button>
      </template>
    </el-input>
    <showView v-if="isParing" :Food="parsingData" id="showDiv" />
  </el-space>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'

import type { foodI } from '@/interfaces';
import { parsing } from '@/request/api'
import showView from './show.vue'

// 获取cookies中的username，如果不存在，则赋值为访客
const username = sessionStorage.getItem('username') || '访客'
let searchFood = ref("")
let parsingData = ref<foodI>()
let isParingIng = ref(false)
let isParing = ref(false)

async function onParsing() {
  isParing.value = false
  if (searchFood.value == "") {
    ElMessage.error('配料名称不能为空!')
  } else {
    // 开始加载
    isParingIng.value = true

    // 解析配料
    await parsing(searchFood.value, username).then(res => {
      if (res.status === 200) {
        isParing.value = true
        parsingData.value = res.data
      }
    }).catch(err => {
      ElMessage.error('解析失败,请检查输入的配料名称后重试!')
      console.log(err)
    })
    isParingIng.value = false
  }

}

</script>

<style scoped>
@media (max-width: 767px) {
  .el-input {
    width: 90vw;
    margin-bottom: 10px
  }

  #showDiv {
    width: 90vw;
  }
}

@media (min-width: 767px) {
  .el-input {
    width: 500px;
    margin-bottom: 10px
  }

  #showDiv {
    width: 500px;
  }
}
</style>
