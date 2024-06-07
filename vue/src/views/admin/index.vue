<template>
  <div class="common-layout">
    <el-container>
      <el-aside id="aside">
        <el-menu id="menu" :default-openeds="['2', '3']" :default-active="$route.fullPath" active-text-color="#DAED05"
          background-color="#545c64" text-color="#fff" class="el-menu-vertical-demo" :collapse="isCollapse"
          @open="handleOpen" @close="handleClose" :router="true">
          <el-menu-item index="1">
            <img id="logoImg" src="@/assets/logoText.png" alt="Element logo" />
          </el-menu-item>

          <el-sub-menu index="2">
            <template #title><el-icon>
                <Food />
              </el-icon>配料管理</template>
            <el-menu-item index="FoodData">配料数据</el-menu-item>
            <el-menu-item index="FoodEdit">增加配料</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="3">
            <template #title><el-icon>
                <User />
              </el-icon>用户管理</template>
            <el-menu-item index="UserData">用户数据</el-menu-item>
            <el-menu-item index="UserEdit">增加用户</el-menu-item>
          </el-sub-menu>

          <el-menu-item index="AISetting">
            <el-icon>
              <Cpu />
            </el-icon>AI设置
          </el-menu-item>

          <el-menu-item index="/login" id="adminOut"><el-icon>
              <Close />
            </el-icon>退出后台</el-menu-item>
        </el-menu>

      </el-aside>
      <el-main>
        <RouterView />
      </el-main>
    </el-container>
  </div>

</template>

<script setup lang="ts">
import { ref } from "vue"
import { RouterLink, RouterView } from 'vue-router'

import {
  Food,
  User,
  Close,
  Cpu
} from '@element-plus/icons-vue'

const isCollapse = ref(false)
const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}

</script>

<style scoped>
#aside {
  width: 180px;
}

#menu {
  height: 100vh;
  width: 180px;
}

#logoImg {
  width: 120px;
}

#adminOut {
  margin-top: 50vh;
}
</style>
