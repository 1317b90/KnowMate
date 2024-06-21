<template>
    <el-form ref="FormRef" :model="Form" status-icon :rules="rules" label-width="auto">
        <!-- 配料名称 -->
        <el-form-item label="配料名称" prop="name">
            <el-input v-model="Form.name" />
        </el-form-item>

        <!-- 类型 -->
        <el-form-item label="配料类型" prop="type">
            <el-input v-model="Form.type" />
        </el-form-item>

        <!-- 简介 -->
        <el-form-item label="配料简介" prop="intro">
            <el-input v-model="Form.intro" autosize type="textarea" />
        </el-form-item>

        <!-- 作用 -->
        <el-form-item label="配料作用" prop="effect">
            <el-input v-model="Form.effect" autosize type="textarea" />
        </el-form-item>

        <!-- 健康影响类别 -->
        <el-form-item label="健康影响类别" prop="harmType">
            <el-radio-group v-model="Form.harmType">
                <el-radio value="有害">有害</el-radio>
                <el-radio value="有益">有益</el-radio>
                <el-radio value="不确定">不确定</el-radio>
            </el-radio-group>
        </el-form-item>
        <!-- 健康影响说明 -->
        <el-form-item label="健康影响说明" prop="harmReason">
            <el-input v-model="Form.harmReason" autosize type="textarea" />
        </el-form-item>

        <!-- 不适宜人群 -->
        <el-form-item label="不适宜人群" prop="out">
            <el-input v-model="Form.out" autosize type="textarea" />
        </el-form-item>


        <!-- 法规标准 -->
        <!-- <el-form-item label="法规标准" prop="ruler">
            <el-input v-model="Form.out" autosize type="textarea" />
        </el-form-item> -->

        <!-- 宗教 -->
        <el-form-item label="清真" prop="religion">
            <el-radio-group v-model="Form.religion">
                <el-radio value="符合清真饮食">符合清真饮食</el-radio>
                <el-radio value="不确定" label="uncertain">不确定</el-radio>
                <el-radio value="不符合清真饮食">不符合清真饮食</el-radio>
            </el-radio-group>
        </el-form-item>


        <!-- 底部按钮 -->
        <el-form-item>
            <div id="formButton">
                <!-- 编辑按钮 -->
                <el-button v-if="editStatus === 'edit'" type="primary" @click="saveForm(FormRef)" :loading="subLoading">
                    保存
                </el-button>

                <!-- 增加按钮 -->
                <el-button v-else type="primary" @click="addForm(FormRef)" :loading="subLoading">
                    增加
                </el-button>

                <el-button @click="resetForm(FormRef)">重置</el-button>
            </div>

        </el-form-item>
    </el-form>
</template>

<script lang="ts" setup>
import { ref, reactive } from "vue"

import type { FormInstance, FormRules } from 'element-plus'
import type { foodI } from '@/interfaces'
import { addFood, getFood, setFood } from '@/request/api'

const Form: foodI = reactive({
    "type": "",
    "effect": "",
    "harmReason": "",
    "ruler": [],
    "modiftime": "",
    "harmType": "不确定",
    "name": "",
    "intro": "",
    "out": "",
    "createtime": "",
    "religion": "uncertain"
})
// 模版的状态，默认为编辑
let editStatus = ref("edit")

const propsData = defineProps(['data', 'refreshData'])
// 如果父模版传入数据，则是编辑
if (propsData.data) {
    Object.assign(Form, propsData.data)
} else {
    // 如果没有传入，则为新增数据
    editStatus.value = "add"
}

const FormRef = ref<FormInstance>()

// username验证
const nameV = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('不能为空！'))
    } else {
        // 如果是增加数据时
        if (editStatus.value == "add") {
            getFood(value).then(res => {
                if (res.data) {
                    callback(new Error('该配料已存在！'))
                } else {
                    callback()
                }
            }).catch(err => { console.log(err) })
        } else { callback() }

    }
}

const rules = reactive<FormRules<typeof Form>>({
    name: [{ validator: nameV, trigger: 'blur' }],
})

// submit按钮的加载状态
let subLoading = ref(false)

// 单击保存按钮后
const saveForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    // 如果通过数据验证
    formEl.validate((valid) => {
        if (valid) {
            Form.modiftime = new Date().toISOString()
            setFood(Form).then(res => {
                if (res.status == 200) {
                    propsData.refreshData(Form)
                    ElMessage.success("保存成功！")
                } else {
                    ElMessage.error("保存失败，请重试")
                }
            }).catch(err => { console.log(ElMessage.error("保存失败，请重试")) })
        }
    })
}

// 单击增加按钮后
const addForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    // 如果通过数据验证
    formEl.validate((valid) => {
        if (valid) {
            const now = new Date();
            Form.createtime = now.toISOString()
            Form.modiftime = now.toISOString()

            addFood(Form).then(res => {
                if (res.status == 200) {
                    ElMessage.success("增加成功！")
                } else {
                    ElMessage.error("增加失败，请重试")
                }
            }).catch(err => { console.log(ElMessage.error("增加失败，请重试")) })
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
    width: 100%;
    display: flex;
    justify-content: flex-end;
}
</style>