<template>
  <el-table id="foodTable" :data="data" stripe :default-sort="{ prop: 'createtime', order: 'ascending' }">

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

          <h4 class="detailsTitle">不适宜人群：</h4>
          <el-text>{{ props.row.intro }}</el-text>

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


    <el-table-column prop="harmType" label="健康影响类型" align="center" :filters="[
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
  <div id="pagination">
    <el-pagination :page-size="pageSize" layout="total,prev, pager, next" :total="total"
      @current-change="currentChange" />
  </div>


  <!-- 编辑抽屉 -->
  <!-- 为什么加上v-if？ 让抽屉重新渲染 -->
  <el-drawer v-model="isEdit" title="配料编辑" direction="rtl" size="45%" v-if="isEdit">
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
import { getFoodTotal, getFoodPage, getFood, delFood } from '@/request/api'
import type { foodI } from '@/interfaces'
import type { TableColumnCtx, TableInstance } from 'element-plus'
import editView from './FoodEditModel.vue'

// 一页的个数
let pageSize = 17

// 总页数
let total = ref(0)

// 数据
let data = reactive<foodI[]>([])

// 获取总页数
getFoodTotal().then(res => {
  total.value = res.data
  // totalPages.value=Math.ceil(res.data/20)
}).catch(err => { })

// 获取数据函数
function getData(page: number = 0, ps: number = pageSize) {
  getFoodPage(page, ps).then(res => {
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
  getFood(searchInput.value).then(res => {
    if (res.data) {
      data.splice(0, data.length, ...[res.data]);
    } else {
      ElMessage.error("该配料不存在！")
    }
  }).catch(err => { console.log(err) })
}

// 筛选有害或有益
const onFilter = (
  value: string,
  row: foodI,
  column: TableColumnCtx<foodI>
) => {
  const property = column['property']
  // @ts-ignore
  return row[property] === value
}


// 是否编辑？
let isEdit = ref(false)
// 编辑的数据
let editData: foodI = reactive({
  name: ""
})


// 获取子模版修改后的数据
function refreshData(redata: foodI) {

  data.forEach((food, index) => {
    if (food.name == redata.name) {
      data[index] = redata
    }
  });
}

// 点击编辑后
function handleEdit(data: foodI) {
  isEdit.value = true
  Object.assign(editData, data)
  console.log(editData)
}

// 是否删除？
let isDel = ref(false)
let delName = ref('')

// 点击删除后
function handleDelete(data: foodI) {
  delName.value = data.name
  isDel.value = true
}

// 确认删除
function onDelVerify() {
  delFood(delName.value).then(res => {
    if (res.status == 200) {
      data.forEach((d, index) => {
        if (d.name == delName.value) {
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
