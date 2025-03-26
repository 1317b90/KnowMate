<template>
  <el-table id="foodTable" :data="data" stripe :default-sort="{ prop: 'createtime', order: 'ascending' }">
    <!-- 表格列定义保持不变 -->
    <el-table-column type="expand">
      <!-- 展开详情内容保持不变 -->
      <template #default="props">
        <div class="detailsDiv">
          <div class="detailsDivv" v-if="props.row.allergy.length > 0">
            <h4>过敏原：</h4>
            <ul>
              <li v-for="allergy in props.row.allergy">{{ allergy }}</li>
              <li v-if="props.row.allergyOther">{{ props.row.allergyOther }}</li>
            </ul>
          </div>

          <div class="detailsDivv" v-if="props.row.disease.length > 0">
            <h4>病史：</h4>
            <ul>
              <li v-for="disease in props.row.disease">{{ disease }}</li>
              <li v-if="props.row.diseaseOther">{{ props.row.diseaseOther }}</li>
            </ul>
          </div>

          <div class="detailsDivv" v-if="props.row.need.length > 0">
            <h4>营养需求：</h4>
            <ul>
              <li v-for="need in props.row.need">{{ need }}</li>
              <li v-if="props.row.needOther">{{ props.row.needOther }}</li>
            </ul>
          </div>
        </div>
      </template>
    </el-table-column>

    <!-- 其他表格列保持不变 -->
    <el-table-column prop="username" label="账号" align="center" />
    <el-table-column prop="password" label="密码" align="center">
      <template #default="scope">
        <el-text truncated>{{ scope.row.password }}</el-text>
      </template>
    </el-table-column>
    <el-table-column prop="email" label="邮箱" align="center">
      <template #default="scope">
        <el-text truncated>{{ scope.row.email }}</el-text>
      </template>
    </el-table-column>

    <el-table-column prop="age" label="年龄" align="center" />

    <el-table-column prop="gender" label="性别" align="center" :filters="[
    { text: '男', value: '男' },
    { text: '女', value: '女' }
  ]" :filter-method="onFilter">
      <template #default="scope">
        <el-tag v-if="scope.row.gender == '女'" type="warning">{{ scope.row.gender }}</el-tag>
        <el-tag v-else-if="scope.row.gender == '男'">{{ scope.row.gender }}</el-tag>
      </template>
    </el-table-column>

    <el-table-column prop="height" label="身高" align="center" />
    <el-table-column prop="weight" label="体重" align="center" />

    <el-table-column prop="goals" label="体重目标" align="center" :filters="[
    { text: '增重', value: '增重' },
    { text: '减肥', value: '减肥' }
  ]" :filter-method="onFilter">
      <template #default="scope">
        <span v-if="scope.row.goals == '增重'" class="upSpan">↑ {{ scope.row.goals }}</span>
        <span v-else-if="scope.row.goals == '减肥'" class="downSpan">↓ {{ scope.row.goals }}</span>
      </template>
    </el-table-column>

    <el-table-column prop="religion" label="清真" align="center">
      <template #default="props">
        <el-icon v-if="props.row.religion" color="#529b2e">
          <Select />
        </el-icon>
        <el-icon v-else color="#b1b3b8">
          <SemiSelect />
        </el-icon>
      </template>
    </el-table-column>

    <el-table-column prop="createtime" width="200" label="注册时间" align="center" sortable />

    <el-table-column label="操作" width="150">
      <template #header>
        <el-input v-model="searchInput" size="small" placeholder="搜索用户" @keyup.enter="searchFuntion" />
      </template>

      <template #default="scope">
        <el-button size="small" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
        <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-pagination id="pagination" :page-size="pageSize" :current-page="currentPage" layout="total, prev, pager, next"
    :total="total" @current-change="currentChange" />

  <el-drawer v-model="isEdit" title="用户编辑" direction="rtl" size="30%" v-if="isEdit">
    <editView :data="editData" :refreshData="refreshData" />
  </el-drawer>

  <el-dialog v-model="isDel" title="Warning" width="500" align-center>
    <span>确定删除{{ delName }}?</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="onDelCancel">取消</el-button>
        <el-button type="primary" @click="onDelVerify">确定</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, reactive } from "vue"
import { getUsers, getUser, delUser } from '@/request/api'
import type { userI } from '@/interfaces'
import type { TableColumnCtx, TableInstance } from 'element-plus'
import editView from './UserEditModel.vue'

import {
  Select,
  CloseBold,
  SemiSelect
} from '@element-plus/icons-vue'

// 分页相关参数
const pageSize = 17
const currentPage = ref(1)
const total = ref(0)
const data = reactive<userI[]>([])

// 获取数据函数
function getData(page: number = 1) {
  getUsers(page - 1, pageSize).then(res => {
    // 更新总数和数据
    total.value = res.data.total
    data.splice(0, data.length, ...res.data.data)
  }).catch(err => {
    console.log(err)
    ElMessage.error('获取数据失败')
  })
}

// 默认获取第一页数据
getData()

// 切换页码
function currentChange(value: number) {
  currentPage.value = value
  getData(value)
}

// 搜索用户
const searchInput = ref('')
function searchFuntion() {
  if (!searchInput.value) {
    getData(1)
    return
  }

  getUser(searchInput.value).then(res => {
    if (res.data) {
      data.splice(0, data.length, ...[res.data])
      total.value = 1
    } else {
      ElMessage.error("该用户不存在！")
    }
  }).catch(err => {
    console.log(err)
    ElMessage.error("搜索失败")
  })
}

// 编辑相关
const isEdit = ref(false)
const editData: userI = reactive({
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
  createtime: "",
  religion: false,
})

function refreshData(redata: userI) {
  const index = data.findIndex(d => d.username === redata.username)
  if (index !== -1) {
    data[index] = redata
  }
}

function handleEdit(rowData: userI) {
  isEdit.value = true
  Object.assign(editData, rowData)
  editData.allergy = editData.allergy || []
  editData.disease = editData.disease || []
  editData.need = editData.need || []
}

// 删除相关
const isDel = ref(false)
const delName = ref('')

function handleDelete(rowData: userI) {
  delName.value = rowData.username
  isDel.value = true
}

function onDelVerify() {
  delUser(delName.value).then(res => {
    if (res.status == 200) {
      const index = data.findIndex(d => d.username === delName.value)
      if (index !== -1) {
        data.splice(index, 1)
        total.value--
      }
      ElMessage.success("删除成功！")
    } else {
      ElMessage.error("删除失败，请重试！")
    }
  }).catch(err => {
    ElMessage.error("删除失败，请重试！")
    console.log(err)
  })
  isDel.value = false
}

function onDelCancel() {
  isDel.value = false
}

// 筛选方法
const onFilter = (
  value: string,
  row: userI,
  column: TableColumnCtx<userI>
) => {
  const property = column['property']
  // @ts-ignore
  return row[property] === value
}
</script>

<style scoped>
#foodTable {
  width: 85vw;
  height: 89vh;
}

#pagination {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}

.detailsDiv {
  margin-left: 80px;
  display: flex;
  width: 450px;
}

.detailsDivv {
  flex: 1;
}

.upSpan {
  color: #c45656;
}

.downSpan {
  color: #529b2e;
}
</style>
