<template>
  <el-table id="foodTable" :data="data" stripe :default-sort="{ prop: 'createtime', order: 'ascending' }">
    <el-table-column type="expand">
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
        <el-button size="small" type="primary" @click="handleEdit(scope.row)">
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
  <el-drawer v-model="isEdit" title="用户编辑" direction="rtl" size="30%" v-if="isEdit">
    <editView :data="editData" :refreshData="refreshData" />
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

import {
  Select,
  CloseBold,
  SemiSelect
} from '@element-plus/icons-vue'

// 一页的个数
let pageSize = 20

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

// 搜索用户
let searchInput = ref()
function searchFuntion() {
  getUser(searchInput.value).then(res => {
    if (res.data) {
      data.splice(0, data.length, ...[res.data]);
    } else {
      ElMessage.error("该用户不存在！")
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
  createtime: "",
  religion: false,
})

// 获取子模版修改后的数据
function refreshData(redata: userI) {
  data.forEach((d, index) => {
    if (d.username == redata.username) {
      data[index] = redata
    }
  });
}

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
      data.forEach((d, index) => {
        if (d.username == delName.value) {
          data.splice(index, 1);
        }
      }
      )
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

// 取消删除
function onDelCancel() {
  isDel.value = false
}


// 筛选性别
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
