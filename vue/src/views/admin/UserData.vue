<template>
  <el-table id="foodTable" :data="data" stripe :default-sort="{ prop: 'createtime', order: 'ascending' }">

    <el-table-column prop="username" label="账号" align="center" />
    <el-table-column prop="password" label="密码">
      <template #default="scope">
        <el-text truncated>{{ scope.row.password }}</el-text>
      </template>
    </el-table-column>
    <el-table-column prop="email" label="邮箱">
      <template #default="scope">
        <el-text truncated>{{ scope.row.email }}</el-text>
      </template>
    </el-table-column>

    <el-table-column prop="age" label="年龄" align="center" />
    <el-table-column prop="gender" label="性别" align="center" />

    <el-table-column prop="height" label="身高" align="center" />
    <el-table-column prop="weight" label="体重" align="center" />

    <el-table-column prop="allergy" label="过敏原">
      <template #default="scope">
        <el-text truncated>{{ scope.row.allergy }}</el-text>
      </template>
    </el-table-column>
    <el-table-column prop="allergyOther" label="其他过敏原" align="center" />

    <el-table-column prop="disease" label="病史">
      <template #default="scope">
        <el-text truncated>{{ scope.row.disease }}</el-text>
      </template>
    </el-table-column>

    <el-table-column prop="diseaseOther" label="其他病史" align="center" />

    <el-table-column prop="goals" label="体重目标" align="center" />

    <el-table-column prop="need" label="营养需求">
      <template #default="scope">
        <el-text truncated>{{ scope.row.need }}</el-text>
      </template>
    </el-table-column>

    <el-table-column prop="needOther" label="其他营养需求" align="center" />

    <el-table-column prop="createtime" label="注册时间" align="center" />

    <el-table-column label="操作" width="150">
      <template #header>
        <el-input v-model="searchInput" size="small" placeholder="搜索用户" @keyup.enter="searchFuntion" />
      </template>

      <template #default="scope">
        <el-button size="small" @click="handleEdit(scope.row)">
          编辑
        </el-button>
        <el-button size="small" type="danger" @click="handleDelete(scope.row)">
          删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>

  <!-- :pager-count="11" -->
  <el-pagination id="pagination" :page-size="pageSize" layout="total,prev, pager, next" :total="total"
    @current-change="currentChange" />

  <!-- 编辑抽屉 -->
  <!-- 为什么加上v-if？ 让抽屉重新渲染 -->
  <el-drawer v-model="isEdit" title="配料编辑" direction="rtl" v-if="isEdit">
    <editView :data="editData" />
  </el-drawer>

  <!-- 删除确认框 -->
  <el-dialog v-model="isDel" title="Warning" width="500" align-center>
    <span>确定删除{{ delName }}?</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="onDelCancel">取消</el-button>
        <el-button type="primary" @click="onDelVerify">
          确定
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, reactive } from "vue"
import { getUserTotal, getUserPage, getUser, delUser } from '@/request/api'
import type { userI } from '@/interfaces'
import type { TableColumnCtx, TableInstance } from 'element-plus'
import editView from './UserEditModel.vue'

// 一页的个数
let pageSize = 13

// 总页数
let total = ref(0)

// 显示数据
let data = reactive<userI[]>([])

// 获取总页数
getUserTotal().then(res => {
  total.value = res.data

}).catch(err => { })

// 获取数据函数
function getData(page: number = 0, ps: number = pageSize) {
  getUserPage(page, ps).then(res => {
    // 使用 splice 替换 data 数组的内容,防止响应失效
    data.splice(0, data.length, ...res.data)
  }).catch(err => {
    console.log(err)
  })
}

// 默认获取第一页数据
getData()

// 切换页码后
function currentChange(value: number) {
  getData(value)
}

// 搜索配料
let searchInput = ref()
function searchFuntion() {
  getUser(searchInput.value).then(res => {
    if (res.data) {
      data.splice(0, data.length, ...[res.data]);
    } else {
      ElMessage.error("该配料不存在！")
    }

  }).catch(err => { console.log(err) })
}


// 是否编辑？
let isEdit = ref(false)
// 编辑的数据

let editData: userI = reactive({
  username: "",
  password: null,
  email: null,
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
  createtime: ""
})

// 点击编辑后
function handleEdit(data: userI) {
  isEdit.value = true

  Object.assign(editData, data)
  // 部分数据为空，需转换为[]
  if (editData.allergy === null) {
    editData.allergy = []
  }
  if (editData.disease === null) {
    editData.disease = []
  }
  if (editData.need === null) {
    editData.need = []
  }
  console.log(editData)
}

// 是否删除？
let isDel = ref(false)
let delName = ref('')

// 点击删除后
function handleDelete(data: userI) {
  delName.value = data.username
  isDel.value = true
}

// 确认删除
function onDelVerify() {
  delUser(delName.value).then(res => {
    if (res.status == 200) {
      ElMessage.success("删除成功！")
      // 刷新页面
      window.location.reload()
    } else {
      ElMessage.error("删除失败，请重试！")
    }
  }).catch(err => {
    ElMessage.error("删除失败，请重试！")
    console.log(err)
  })
  isDel.value = false
}

// 取消删除
function onDelCancel() {
  isDel.value = false
}

</script>

<style scoped>
#foodTable {
  width: 85vw;
  height: 91vh;
}

#pagination {
  float: right;
  margin-top: 10px;
  margin-right: 50px;
}
</style>
