<template>

    <el-form ref="FormRef" :model="Form" status-icon :rules="rules" label-width="auto" label-position="left">
        <!-- 年龄 -->
        <el-form-item label="用户名" prop="username">
            <el-input v-model="Form.username" />
        </el-form-item>
        <!-- 年龄 -->
        <el-form-item label="密码" prop="password">
            <el-input v-model="Form.password" />
        </el-form-item>
        <!-- 年龄 -->
        <el-form-item label="邮箱" prop="email">
            <el-input v-model="Form.email" />
        </el-form-item>
        <el-divider />
        <!-- 年龄 -->
        <el-form-item label="年龄" prop="age">
            <el-input v-model.number="Form.age" type="number" />
        </el-form-item>

        <!-- 性别 -->
        <el-form-item label="性别" prop="gender">
            <el-radio-group v-model="Form.gender">
                <el-radio value="男">男</el-radio>
                <el-radio value="女">女</el-radio>
            </el-radio-group>
        </el-form-item>

        <!-- 身高 -->
        <el-form-item label="身高/cm" prop="height">
            <el-input v-model.number="Form.height" type="number" />
        </el-form-item>

        <!-- 体重 -->
        <el-form-item label="体重/kg" prop="weight">
            <el-input v-model.number="Form.weight" type="number" />
        </el-form-item>
        <el-divider />
        <!-- 过敏原 -->
        <el-form-item label="过敏原" prop="allergy">
            <el-checkbox-group v-model="Form.allergy">
                <el-checkbox value="蛋白质" label="蛋白质" />
                <el-checkbox value="海鲜" label="海鲜" />
                <el-checkbox value="坚果" label="坚果" />
                <el-checkbox value="豆制品" label="豆制品" />
                <el-checkbox value="其他" label="其他" />
            </el-checkbox-group>
            <el-input v-if="Form.allergy.includes('其他')" v-model="Form.allergyOther" size="small" />
        </el-form-item>

        <!-- 过敏原 -->
        <el-form-item label="病史" prop="disease">
            <el-checkbox-group v-model="Form.disease">
                <el-checkbox value="糖尿病" label="糖尿病" />
                <el-checkbox value="高血压" label="高血压" />
                <el-checkbox value="心脏病" label="心脏病" />
                <el-checkbox value="肠胃敏感" label="肠胃敏感" />
                <el-checkbox value="肾病" label="肾病" />
                <el-checkbox value="其他" label="其他" />
            </el-checkbox-group>
            <el-input v-if="Form.disease.includes('其他')" v-model="Form.diseaseOther" size="small" />
        </el-form-item>

        <!-- 目标 -->
        <el-form-item label="体重目标" prop="goals">
            <el-radio-group v-model="Form.goals">
                <el-radio value="增重">增重</el-radio>
                <el-radio value="减肥">减肥</el-radio>
                <el-radio value="无">无</el-radio>
            </el-radio-group>
        </el-form-item>

        <!-- 营养需求 -->
        <el-form-item label="营养需求" prop="need">
            <el-checkbox-group v-model="Form.need">
                <el-checkbox value="高蛋白" label="高蛋白" />
                <el-checkbox value="低碳水化合物" label="低碳水化合物" />
                <el-checkbox value="低脂饮食" label="低脂饮食" />
                <el-checkbox value="其他" label="其他" />
            </el-checkbox-group>

            <el-input v-if="Form.need.includes('其他')" v-model="Form.needOther" size="small" />
        </el-form-item>

        <!-- 宗教习惯 -->
        <el-form-item label="宗教习惯" prop="muslim">
            <el-checkbox v-model="Form.muslim">清真</el-checkbox>
        </el-form-item>

        <!-- 底部按钮 -->
        <el-form-item>
            <div id="formButton">
                <!-- 编辑按钮 -->
                <el-button v-if="editStatus === 'edit'" type="primary" @click="saveForm(FormRef)">
                    保存
                </el-button>

                <!-- 增加按钮 -->
                <el-button v-else type="primary" @click="addForm(FormRef)">
                    增加
                </el-button>
                <el-button @click="resetForm(FormRef)">重置</el-button>
            </div>


        </el-form-item>
    </el-form>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue"
import type { FormInstance, FormRules } from 'element-plus'
import type { userI } from '@/interfaces'
import { setUser, addUser, getUser } from '@/request/api'

const FormRef = ref<FormInstance>()


let Form: userI = reactive({
    username: "",
    password: null,
    email: "",
    age: null,
    gender: null,
    height: null,
    weight: null,
    allergy: [],
    allergyOther: null,
    disease: [],
    diseaseOther: null,
    goals: null,
    need: [],
    needOther: null,
    createtime: "",
    muslim: false
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

// username验证
const usernameV = (rule: any, value: any, callback: any) => {
    const pattern = /^[a-zA-Z0-9]{3,15}$/
    if (value === '') {
        callback(new Error('用户名不能为空！'))
    }
    else if (!pattern.test(value)) {
        callback(new Error('要求3到15个字符，只能包含字母和数字'))
    } else {
        if (editStatus.value == "add") {
            getUser(value).then(res => {
                if (res.data) {
                    callback(new Error('该用户名已存在！'))
                } else {
                    callback()
                }
            }).catch(err => {
                console.log(err)
            })
        } else {
            callback()
        }


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

// age验证
const ageV = (rule: any, value: any, callback: any) => {
    if (value < 0) {
        callback(new Error('年龄不能为负！'))
    }
    else if (value > 150) {
        callback(new Error('你个老不死的！'))
    } else {
        callback()
    }
}

const rules = reactive<FormRules<typeof Form>>({
    age: [{ validator: ageV, trigger: 'blur' }],
    password: [{ validator: passwordV, trigger: 'blur' }],
    username: [{ validator: usernameV, trigger: 'blur' }],

})


// 单击保存按钮后
const saveForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    // 如果通过数据验证
    formEl.validate((valid) => {
        if (valid) {
            const submitData = {
                password: Form.password,
                email: Form.email,
                age: Form.age,
                gender: Form.gender,
                height: Form.height,
                weight: Form.weight,
                allergy: Form.allergy,
                allergyOther: Form.allergyOther,
                disease: Form.disease,
                diseaseOther: Form.diseaseOther,
                goals: Form.goals,
                need: Form.need,
                needOther: Form.needOther,
                muslim: Form.muslim,
            }
            setUser(Form.username, submitData).then(res => {
                if (res.status == 200) {
                    propsData.refreshData(Form)
                    ElMessage.success("保存成功！")
                } else {
                    console.log(res)
                    ElMessage.error("保存失败，请重试")
                }
            }).catch(err => {
                console.log(err)
                ElMessage.error("保存失败，请重试")
            })
        }
    })
}

// 单击增加按钮后
const addForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    // 如果通过数据验证
    formEl.validate((valid) => {
        if (valid) {
            Form.createtime = new Date().toISOString()
            const submitData = {
                password: Form.password,
                email: Form.email,
                age: Form.age,
                gender: Form.gender,
                height: Form.height,
                weight: Form.weight,
                allergy: Form.allergy,
                allergyOther: Form.allergyOther,
                disease: Form.disease,
                diseaseOther: Form.diseaseOther,
                goals: Form.goals,
                need: Form.need,
                needOther: Form.needOther,
                muslim: Form.muslim,
            }
            addUser(Form.username, submitData).then(res => {
                if (res.status == 200) {
                    ElMessage.success("增加成功！")
                } else {
                    ElMessage.error("增加失败，请重试")
                }
            }).catch(err => {
                console.log(err)
                ElMessage.error("增加失败，请重试")
            })
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