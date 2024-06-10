<template>
  <div class="common-layout">
    <el-container>
      <el-aside id="aside">
        <el-menu id="menu" :default-openeds="['2', '3']" :default-active="$route.fullPath" background-color="#001529"
          text-color="#fff" :router="true" >

          <el-menu-item index="1" id="logoMenu">
            <img id="logoImg" src="@/assets/logoText.png" alt="Element logo" />
          </el-menu-item>

          <el-menu-item index="/Dashboard">
            <el-icon>
              <Menu />
            </el-icon>仪 表 盘
          </el-menu-item>

          <el-sub-menu index="2">
            <template #title><el-icon>
                <Food />
              </el-icon>配料管理</template>
            <el-menu-item index="/FoodData">配料数据</el-menu-item>
            <el-menu-item index="/FoodEdit">增加配料</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="3">
            <template #title><el-icon>
                <User />
              </el-icon>用户管理</template>
            <el-menu-item index="/UserData">用户数据</el-menu-item>
            <el-menu-item index="/UserEdit">增加用户</el-menu-item>
          </el-sub-menu>

          <el-menu-item index="/LogData">
            <el-icon>
              <Tickets />
            </el-icon>解析记录
          </el-menu-item>

          <el-menu-item index="/AISetting">
            <el-icon>
              <Operation />
            </el-icon>AI 设置
          </el-menu-item>

          <el-menu-item index="/login" id="adminOut"><el-icon>
              <Close />
            </el-icon>退出后台</el-menu-item>
        </el-menu>

      </el-aside>
      <el-main id="main">
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
  Operation,
  Menu,
  Tickets
} from '@element-plus/icons-vue'



</script>

<style scoped>
/* 左侧栏 */
#aside {
  height: 100vh;
  width: 180px;
}

/* 左侧导航 */
#menu {
  height: 100vh;
  width: 180px;
}

/* logo图片 */
#logoImg {
  width: 120px;
}
#logoMenu{
  height: 80px;
}
/* 被选中的导航 */
.el-menu-item.is-active {
  background-color: rgba(153, 197, 108, 0.4) !important;
  color: rgba(254, 248, 0, 0.9);
  border-radius: 10px;
  margin:0px 10px 0px 10px;
}

/* 主要内容 */
#main {
  width: 85vw;
  height: 100vh;

}
</style>
