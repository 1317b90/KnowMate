<template>
    <div id="all">
        <div id="loginDiv">
            <div class="spanClass" id="loginTitleDiv">
                <img src="@/assets/logo0.png" id="loginImg">
                <span id="loginTitle">知料 · 登录</span>
            </div>

            <el-input v-model="inputUsername" placeholder="请输入账号" :controls="false" :prefix-icon="User" size="large"
                maxlength="11" class="spanClass" />

            <el-input v-model="inputPassword" placeholder="请输入密码" @keyup.enter="onLogin" type="password" show-password
                :prefix-icon="Lock" size="large" class="spanClass" />

            <el-button type="primary" @click="onLogin" id="loginButton" size="large" class="spanClass"
                :loading="loginLoading">登 陆</el-button>
        </div>

        <div id="bottom">
            <el-button id="goVisitorsBotton" text primary type="primary" @click="router.push('/')">访客登陆</el-button>
            <el-button id="goRegisterBotton" text primary type="primary" @click="router.push('/register')">
                立即注册</el-button>
        </div>

    </div>
</template>

<script setup lang="ts">
import { User, Lock } from '@element-plus/icons-vue'
import { ref } from "vue"
import { ElMessage } from 'element-plus'
import { getUser } from '@/request/api'

import { useRouter } from 'vue-router';
const router = useRouter()

// 登陆之前，清除cookie
sessionStorage.clear()

let inputUsername = ref("")
let inputPassword = ref("")
let loginLoading = ref(false)
function onLogin() {
    if (inputUsername.value == "" || inputPassword.value == "") {
        ElMessage.error('账号或密码不能为空！')
    }
    else {
        loginLoading.value = true
        getUser(inputUsername.value).then(res => {
            if (res.data.password == inputPassword.value) {
                ElMessage.success('登录成功！')
                sessionStorage.setItem('username', inputUsername.value);
                // 如果是管理员
                if (inputUsername.value == 'admin') {
                    router.push('/Dashboard')
                } else {
                    router.push('/')
                }
            }
            else {
                ElMessage.error('密码错误！')
            }
        }).catch(err => {
            ElMessage.error('登录失败，' + err)
        }).finally(() => {
            loginLoading.value = false
        })
    }
}


</script>

<style scoped>
.spanClass {
    margin-bottom: 15px;
}

#all {
    width: 360px;
    border-radius: 10px;
    padding: 40px 40px 20px 40px;
    background-color: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(30px);
}

#loginTitleDiv {
    margin-left: 65px;
    margin-top: 10px;
    margin-bottom: 20px;
}

#loginImg {
    height: 31px;
    margin-right: 15px;
    float: left;
    margin-top: -5px;
}

#loginTitle {
    font-size: 21px;
    letter-spacing: 3px;
    font-weight: 350;
    line-height: 20px;
}

#loginButton {
    width: 280px;
}

#goVisitorsBotton {
    float: left;
    margin-left: -15px;
}

#goRegisterBotton {
    float: right;
    margin-right: -15px;
}
</style>