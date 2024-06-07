<template>
  <loginView  v-if="loginPaths.includes($route.fullPath)" />
  <clientView  v-else-if="clientPaths.includes($route.fullPath)" />
  <adminView v-else-if="adminPaths.includes($route.fullPath)" />
  <el-text v-else>404</el-text>
</template>

<script setup lang="ts">
import clientView from './views/client/index.vue'
import loginView from './views/login/index.vue'
import adminView from './views/admin/index.vue'
import { ref } from 'vue'

const loginPaths = ["/login", "/register"]
const clientPaths = ["/home", "/parsing", "/search", "/info","/"]
const adminPaths = ["/FoodData","/FoodEdit","/UserData","/UserEdit","/AISetting"]

</script>

<style scoped></style>
