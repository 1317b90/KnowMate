<template>
    <div id="aiAll">

        <div id="aiForm">
            <h3 style="text-align: center; margin-bottom: 15px;">AI 设置</h3>
            <el-form ref="FormRef" :model="Form" status-icon :rules="rules" label-width="auto">
                <!-- api_key -->
                <el-form-item label="api_key" prop="api_key">
                    <el-input v-model="Form.api_key" />
                </el-form-item>
                <el-form-item label="web_search" prop="web_search">
                    <el-switch v-model.number="Form.web_search" active-text="模型启用网络搜索" />
                </el-form-item>
                <!-- top_p -->
                <el-form-item label="top_p" prop="top_p">
                    <el-slider v-model.number="Form.top_p" show-input step="0.1" max="1" />
                </el-form-item>

                <!-- temperature -->
                <el-form-item label="temperature" prop="temperature">
                    <el-slider v-model.number="Form.temperature" show-input step="0.1" max="1" />
                </el-form-item>

                <!-- max_tokens -->
                <el-form-item label="max_tokens" prop="max_tokens">
                    <el-slider v-model="Form.max_tokens" show-input max="1350" />
                </el-form-item>

                <!-- role -->
                <el-form-item label="role" prop="role">
                    <el-input v-model="Form.role" autosize type="textarea" />
                </el-form-item>

                <!-- 底部按钮 -->
                <el-form-item id="formButton">
                    <el-button type="primary" @click="saveForm(FormRef)" class="formButton" id="registerButton"
                        :loading="subLoading">
                        保存
                    </el-button>
                    <el-button @click="resetForm(FormRef)" class="formButton">重置</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>

</template>

<script lang="ts" setup>
import { ref, reactive } from "vue"

import type { FormInstance, FormRules } from 'element-plus'


const FormRef = ref<FormInstance>()

const Form = reactive({
    "api_key": "28698839aff97f518ef798ee22384d74.zrQb5Xa9s7QicZMP",
    "web_search": true,
    "top_p": 0.7,
    "temperature": 0.01,
    "role": "你是一个食品配料方面的专家，拥有广泛的食品科学知识和营养学背景。你的任务是为用户提供食品配料相关的专业、准确、具体、有见地的解释和建议，帮助他们理解和解析食品配料表。",
    "max_tokens": 1024
})

const api_keyV = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('不能为空！'))
    } else {
        callback()
    }
}

const rules = reactive<FormRules<typeof Form>>({
    api_key: [{ validator: api_keyV, trigger: 'blur' }],
})

// submit按钮的加载状态
let subLoading = ref(false)

// 单击保存按钮后
const saveForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    // 如果通过数据验证
    formEl.validate((valid) => {
        if (valid) {

            ElMessage.success("保存成功！")
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
#formButton {
    margin-left: 350px;
}

#aiAll {
    width: 100%;
    display: flex;
    justify-content: center;
}

#aiForm {
    width: 550px;
    padding: 30px;
    border-radius: 10px;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 0px 5px 0px;
}
</style>