<template>
    <!-- 注册页面 -->
    <div id="registerDiv" class="all">
        <div>
            <div class="spanClass" id="loginTitleDiv">
                <img src="@/assets/logo0.png" id="loginImg">
                <span id="loginTitle">Register</span>
            </div>
            <el-form ref="FormRef" :model="Form" status-icon :rules="rules" label-width="auto">
                <!-- 账号 -->
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="Form.username" />
                </el-form-item>
                <!-- 密码 -->
                <el-form-item label="密码" prop="password">
                    <el-input v-model="Form.password" type="password" show-password />
                </el-form-item>
                <!-- 确认密码 -->
                <el-form-item label="确认密码" prop="password2">
                    <el-input v-model="Form.password2" />
                </el-form-item>
                <!-- 邮箱 -->
                <!-- placeholder="" -->
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="Form.email" />
                </el-form-item>

                <!-- 底部按钮 -->
                <el-form-item>
                    <el-button type="primary" @click="submitForm(FormRef)" class="formButton" id="registerButton"
                        :loading="registerLoading">
                        注册
                    </el-button>
                    <el-button @click="resetForm(FormRef)" class="formButton">重置</el-button>
                </el-form-item>
            </el-form>
        </div>

        <div id="bottom">
            <el-button id="goVisitorsBotton" text primary type="primary" @click="router.push('/')">访客登陆</el-button>
            <el-button id="goLoginBotton" text primary type="primary" @click="router.push('/login')">返回登陆</el-button>
        </div>

    </div>


    <!-- 滑动验证框 -->
    <Vcode :show="vcodeShow" @success="vcodeSuccess" @close="vcodeClose" />

</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import Vcode from "vue3-puzzle-vcode";
import { reactive, ref } from 'vue'
import { register, getUser } from '@/request/api'

import type { FormInstance, FormRules } from 'element-plus'
const FormRef = ref<FormInstance>()

import { useRouter } from 'vue-router';
const router = useRouter()

// username验证
const usernameV = (rule: any, value: any, callback: any) => {
    const pattern = /^[a-zA-Z0-9]{3,15}$/
    if (value === '') {
        callback(new Error('用户名不能为空！'))
    }
    else if (!pattern.test(value)) {
        callback(new Error('要求3到15个字符，只能包含字母和数字'))
    } else {
        getUser(value).then(res => {
            if (res.data) {
                callback(new Error('用户名已存在！'))
            } else {
                callback()
            }
        }).catch(err => {
            console.log(err)
        })

    }
}

// password验证
const passwordV = (rule: any, value: any, callback: any) => {
    const pattern = /^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,}$/
    if (value === '') {
        callback(new Error('密码不能为空！'))
    } else if (!pattern.test(value)) {
        callback(new Error('要求至少8个字符，同时包含字母和数字'))
    } else {
        callback()
    }

}

// password二次验证
const password2V = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('确认密码不能为空！'))
    } else if (value !== Form.password) {
        callback(new Error("两次输入的密码不一致！"))
    } else {
        callback()
    }
}

// 邮箱验证
const emailV = (rule: any, value: any, callback: any) => {
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    // 如果为空，直接跳过
    if (!value) { callback() }
    // 如果不为空，验证是否正确
    else if (!pattern.test(value)) {
        callback(new Error('邮箱地址有误！'))
    } else {
        callback()
    }
}

const Form = reactive({
    username: '',
    password: '',
    password2: '',
    email: '',
})

const rules = reactive<FormRules<typeof Form>>({
    username: [{ validator: usernameV, trigger: 'blur' }],
    password: [{ validator: passwordV, trigger: 'blur' }],
    password2: [{ validator: password2V, trigger: 'blur' }],
    email: [{ validator: emailV, trigger: 'blur' }],
})

// 滑动验证码
let vcodeShow = ref(false)

// 注册按钮的加载状态
let registerLoading = ref(false)

// 通过验证码
async function vcodeSuccess(msg: any) {
    vcodeShow.value = false;
    registerLoading.value = true
    await register(Form).then(res => {
        if (res.data == "用户名已存在") {
            ElMessage.error("用户名已存在！")
            registerLoading.value = false
        } else {
            sessionStorage.setItem('username', Form.username);
            sessionStorage.setItem('isFirst', "true");
            router.push('/info')
        }
    }).catch(err => {
        ElMessage.error("注册失败，请重试！")
        console.log(err)
        registerLoading.value = false
    })
}

// 关闭验证码
function vcodeClose() {
    vcodeShow.value = false;
}

// 单击提交按钮后
const submitForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    // 如果通过数据验证
    formEl.validate((valid) => {
        if (valid) {
            vcodeShow.value = true
        }
    })
}

// 重置表单
const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
}



</script>

<style scoped>
.spanClass {
    margin-bottom: 15px;
}

.all {
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

.formButton {
    width: 135px;
}

#registerButton {
    margin-right: 18px;
}

#goVisitorsBotton {
    float: left;
    margin-left: -15px;
}

#goLoginBotton {
    float: right;
    margin-right: -15px;
}
</style>