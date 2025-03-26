<template>
  <el-table id="foodTable" :data="data" stripe :default-sort="{ prop: 'createtime', order: 'ascending' }">
    <!-- 表格列定义保持不变 -->
    <el-table-column type="expand">
      <template #default="props">
        <div class="detailsDiv">
          <h4 class="detailsTitle">简介：</h4>
          <el-text>{{ props.row.intro }}</el-text>
          <br />
          <h4 class="detailsTitle">作用：</h4>
          <el-text>{{ props.row.effect }}</el-text>

          <h4 class="detailsTitle">健康影响说明：</h4>
          <el-text>{{ props.row.harmReason }}</el-text>

          <h4 class="detailsTitle">风险提示：</h4>
          <el-text>{{ props.row.risk }}</el-text>

          <h4 class="detailsTitle">法律法规：</h4>
          <ul>
            <li v-for="ruler in props.row.ruler"> <a :href="ruler.url" target="_blank" class="rulerA"><el-text>《{{
              ruler.title
                  }}》</el-text></a></li>
          </ul>
        </div>
      </template>
    </el-table-column>

    <el-table-column prop="name" label="名称" align="center" />
    <el-table-column prop="type" label="类型" align="center" />

    <el-table-column prop="harmType" label="健康影响" align="center" width="150" :filters="[
      { text: '有害', value: '有害' },
      { text: '有益', value: '有益' },
      { text: '不确定', value: '不确定' },
    ]" :filter-method="onFilter">
      <template #default="scope">
        <el-tag v-if="scope.row.harmType == '有益'" type="success">{{ scope.row.harmType }}</el-tag>
        <el-tag v-else-if="scope.row.harmType == '有害'" type="danger">{{ scope.row.harmType }}</el-tag>
        <el-tag v-else type="info">{{ scope.row.harmType }}</el-tag>
      </template>
    </el-table-column>


    <el-table-column prop="createtime" label="创建时间" sortable />
    <el-table-column prop="modiftime" label="修改时间" sortable />

    <el-table-column label="操作" width="150">
      <template #header>
        <el-input v-model="searchInput" size="small" placeholder="搜索配料" @keyup.enter="searchFuntion" />
      </template>
      <template #default="scope">
        <el-button size="small" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
        <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <div id="pagination">
    <el-pagination :page-size="pageSize" :current-page="currentPage" layout="total, prev, pager, next" :total="total"
      @current-change="currentChange" />
  </div>

  <el-drawer v-model="isEdit" title="配料编辑" direction="rtl" size="45%" v-if="isEdit">
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
import { getFoods, getFood, delFood } from '@/request/api'
import type { foodI } from '@/interfaces'
import type { TableColumnCtx, TableInstance } from 'element-plus'
import editView from './FoodEditModel.vue'

// 分页相关参数
const pageSize = 17
const currentPage = ref(1)
const total = ref(0)
const data = reactive<foodI[]>([])

// 获取数据函数
function getData(page: number = 1) {
  getFoods(page - 1, pageSize).then(res => {
    // 更新总数和数据
    total.value = res.data.total
    data.splice(0, data.length, ...res.data.data)
  }).catch(err => {
    console.log(err)
    ElMessage.error('获取数据失败,' + err)
  })
}

// 默认获取第一页数据
getData()

// 切换页码
function currentChange(value: number) {
  currentPage.value = value
  getData(value)
}

// 搜索配料
const searchInput = ref('')
function searchFuntion() {
  getFood(searchInput.value).then(res => {
    if (res.data) {
      data.splice(0, data.length, ...[res.data])
    } else {
      ElMessage.error("该配料不存在！")
    }
  }).catch(err => {
    console.log(err)
    ElMessage.error("搜索失败")
  })
}

// 筛选功能
const onFilter = (
  value: string,
  row: foodI,
  column: TableColumnCtx<foodI>
) => {
  const property = column['property']
  return row[property as keyof foodI] === value
}

// 编辑相关
const isEdit = ref(false)
const editData: foodI = reactive({
  name: ""
})

function refreshData(redata: foodI) {
  const index = data.findIndex(food => food.name === redata.name)
  if (index !== -1) {
    data[index] = redata
  }
}

function handleEdit(rowData: foodI) {
  isEdit.value = true
  Object.assign(editData, rowData)
}

// 删除相关
const isDel = ref(false)
const delName = ref('')

function handleDelete(rowData: foodI) {
  delName.value = rowData.name
  isDel.value = true
}

function onDelVerify() {
  delFood(delName.value).then(res => {
    if (res.status == 200) {
      const index = data.findIndex(d => d.name === delName.value)
      if (index !== -1) {
        data.splice(index, 1)
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
</script>

<style scoped>
#foodTable {
  width: 85vw;
  height: 89vh;
}

#pagination {
  width: 85vw;
  display: flex;
  justify-content: flex-end;
}

.detailsDiv {
  margin-left: 8vw;
  margin-right: 8vw;
  width: 65vw;
}

.detailsTitle {
  margin-top: 10px;
}
</style>
