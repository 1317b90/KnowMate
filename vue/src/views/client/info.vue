<template>
  <div id="all">
    <div id="firstAlert" v-if="isFirst">
      <h1>初次见面 欢迎使用知料！</h1>
      <el-text>为了能进行个性化的饮食推荐，需要收集您的部分信息。当然您也可以选择<a @click="router.push('/')">跳过</a>。</el-text>
    </div>

    <el-form ref="FormRef" :model="Form" status-icon :rules="rules" label-width="auto" label-position="left">
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

      <!-- 底部按钮 -->
      <el-form-item>
        <el-button type="primary" @click="submitForm(FormRef)" class="
      formButton" id="registerButton">
          确认
        </el-button>
        <el-button @click="resetForm(FormRef)" class="
      formButton">重置</el-button>

      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue"
import type { FormInstance, FormRules } from 'element-plus'
import type { userI } from '@/interfaces'
import { getUser,setUser } from '@/request/api'
import { useRouter } from 'vue-router';
const router = useRouter()
const username = sessionStorage.getItem('username')
const isFirst=sessionStorage.getItem('isFirst')
const FormRef = ref<FormInstance>()



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

})

let Form: userI = reactive({
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
  username:""
})


// 获取数据
async function getData() {
  if (username) {
    await getUser(username).then(res => {
      Object.assign(Form, res.data)
      // 部分数据为空，需转换为[]
      if(Form.allergy===null){
        Form.allergy=[]
      }
      if(Form.disease===null){
        Form.disease=[]
      }
      if(Form.need===null){
        Form.need=[]
      }
    }).catch(err => {
      console.log(err)
    })
  }

}

getData()

// 修改用户数据函数
async function onSetUser(data:userI) {
  await setUser(data).then(res=>{
    console.log(res)
    ElMessage.success("保存成功！")
  }).catch(err=>{
    ElMessage.error("保存失败，请重试！")
    console.log(err)
  })
}
// 单击提交按钮后
const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  // 如果通过验证
  formEl.validate((valid) => {
    if (valid) {
      console.log(Form)
      onSetUser(Form)
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
@media (min-width: 767px) {
  #all {
    width: 400px;
    padding: 30px;
    border-radius: 10px;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 0px 5px 0px;
  }
}


.formButton {
  width: 135px;
}

#registerButton {
  margin-right: 15px;
}
#firstAlert{
  margin-bottom: 20px;
}
</style>