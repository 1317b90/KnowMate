<template>
  <!-- <el-container> -->
  <!-- <el-header> -->
  <el-menu id="menu" :default-active="$route.fullPath" class="el-menu-demo" mode="horizontal" :router=true
    :ellipsis="false">
    <!-- 这里是知料 -->
    <el-menu-item id="logoMenu" index="/">
      <img id="logoMenuImg" src="@/assets/logo.png" />
    </el-menu-item>

    <el-menu-item index="/parsing"><el-icon>
        <Aim />
      </el-icon>配料表识别</el-menu-item>
    <el-menu-item index="/search"><el-icon>
        <Search />
      </el-icon>配料搜索</el-menu-item>
    <el-menu-item index="/chat"><el-icon>
        <ChatRound />
      </el-icon>配料问答</el-menu-item>


    <div class="flex-grow" />

    <!-- 用户编辑 -->
    <el-sub-menu index="2" v-if="username">
      <template #title><el-icon>
          <User />
        </el-icon></template>
      <el-menu-item-group :title="username">

        <el-menu-item index="/info">资料修改</el-menu-item>
        <el-menu-item v-if="username == 'admin'" index="/Dashboard">后台管理</el-menu-item>
        <el-menu-item index="/login">退出</el-menu-item>
      </el-menu-item-group>
    </el-sub-menu>

    <el-menu-item index="/login" v-else>登陆</el-menu-item>
  </el-menu>
  <!-- </el-header> -->

  <div id="clientMain">
    <RouterView />
  </div>

  <!-- </el-main> -->

  <!-- </el-container> -->
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { User } from '@element-plus/icons-vue'
import { Aim, Search, ChatRound } from '@element-plus/icons-vue'
const username = sessionStorage.getItem('username')
</script>

<style scoped>
/* 头部区域 */
.el-header {
  padding: 0px;

}

/* app内所有内容 */
.el-container {
  width: 100vw;
}


/* 导航栏 */
#menu {
  width: 100vw;
  box-shadow: rgba(0, 0, 0, 0.18) 0px 0px 4px 0px;
  border-bottom: 0px;
}

/* 让用户编辑在最右边 */
.flex-grow {
  flex-grow: 1;
}

/* 桌面设备样式 */
@media (min-width: 768px) {

  /* 导航栏图标 */
  #logoMenuImg {
    width: 110px;
  }
}

/* 移动设备样式 */
@media (max-width: 767px) {
  #logoMenu {
    display: none;
  }
}

/* 主要内容区域 */
#clientMain {
  width: 100vw;
  min-height: calc(100vh - 60px);
  display: flex;
  justify-content: center;
  /* padding-top: 20px; */
  /* padding-bottom: 20px; */
  /* background-color: #e8edf0; */
  background-color: #f5f7fa;
}
</style>
