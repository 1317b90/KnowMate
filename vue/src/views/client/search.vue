<template>
  <div class="search-container">
    <div v-show="!isParing" class="search-title">
      <h1>配料搜索</h1>
      <p>输入配料名称，了解更多信息</p>
    </div>
    <el-space direction="vertical" alignment="normal">
      <div class="search-box">
        <el-input id="searchInput" v-model="searchFood" placeholder="请输入配料名称" @keyup.enter="onParsing"
          :prefix-icon="Search" class="custom-input">
          <template #append>
            <el-button type="primary" @click="onParsing" :loading="isParingIng" class="search-button">
              搜索
            </el-button>
          </template>
        </el-input>
      </div>
      <showView v-if="isParing" :Food="parsingData" id="showDiv" />
    </el-space>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'

import type { foodI } from '@/interfaces';
import { parsing } from '@/request/api'
import showView from './show.vue'

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
    isParingIng.value = true
    await parsing(searchFood.value, username).then(res => {
      if (res.status === 200) {
        isParing.value = true
        parsingData.value = res.data
      }
    }).catch(err => {
      ElMessage.error('解析失败,' + err)
      console.log(err)
    })
    isParingIng.value = false
  }
}
</script>

<style scoped>
.search-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
}

.search-title {
  text-align: center;
  margin-bottom: 30px;
}

.search-title h1 {
  font-size: 2.5em;
  color: #2c3e50;
  margin-bottom: 10px;
  font-weight: 600;
}

.search-title p {
  color: #7f8c8d;
  font-size: 1.1em;
}

.search-box {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  margin-bottom: 20px;
}

.custom-input :deep(.el-input__wrapper) {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 8px;
}

.custom-input :deep(.el-input__inner) {
  height: 40px;
  font-size: 16px;
}

.search-button {
  height: 40px;
  padding: 0 20px;
  font-size: 16px;
}

/* 修改搜索按钮样式 */
.custom-input :deep(.el-input-group__append) {
  padding: 0;
  border: none;
  background-color: transparent;
}

.custom-input :deep(.el-input-group__append .el-button) {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  margin: 0;
  height: 100%;
}

@media (max-width: 767px) {
  .search-box {
    width: 90vw;
  }

  #showDiv {
    width: 90vw;
  }

  .search-title h1 {
    font-size: 2em;
  }
}

@media (min-width: 767px) {
  .search-box {
    width: 500px;
  }

  #showDiv {
    width: 500px;
  }
}
</style>
