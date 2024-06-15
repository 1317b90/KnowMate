<template>
    <div id="all">
        <div id="loginDiv">
            <div class="spanClass" id="loginTitleDiv">
                <img src="@/assets/logo0.png" id="loginImg">
                <span id="loginTitle">Login</span>
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
import { login } from '@/request/api'

import { useRouter } from 'vue-router';
const router = useRouter()

// 登陆之前，清除cookie
sessionStorage.clear()

let inputUsername = ref("")
let inputPassword = ref("")
let loginLoading = ref(false)
async function onLogin() {
    if (inputUsername.value == "" || inputPassword.value == "") {
        ElMessage.error('账号或密码不能为空！')
    }
    else {
        loginLoading.value = true
        await login(inputUsername.value, inputPassword.value).then(res => {
            if (res.data == "登陆成功") {
                // 如果是管理员
                if (inputUsername.value == 'admin') {
                    router.push('/Dashboard')
                } else {
                    // 保存账号到cookie
                    sessionStorage.setItem('username', inputUsername.value);
                    router.push('/')
                }
            } else if (res.data == "账号或密码错误") {
                ElMessage.error('账号或密码错误，请检查后重试！')
            } else if (res.data == "用户不存在") {
                ElMessage.error('用户不存在，请先注册！')
            } else {
                ElMessage.error('出错了，请重试！')
            }
        }).catch(err => {
            ElMessage.error('出错了，请重试！')
            console.log(err)
        })
        loginLoading.value = false
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
    padding: 30px 30px 20px 30px;
    background-color: #b2b3b440;
}

#loginTitleDiv {
    margin-left: 80px;
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
    font-size: 27px;
    letter-spacing: 3px;
    font-weight: 350;
    line-height: 20px;
}

#loginButton {
    width: 300px;
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