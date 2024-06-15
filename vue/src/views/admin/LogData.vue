<template>
  <el-table id="foodTable" :data="data" stripe :default-sort="{ prop: 'time', order: 'descending' }">
    <el-table-column type="expand">
      <template #default="props">
        <el-text>{{ props.row.output }} </el-text>
      </template>
    </el-table-column>

    <el-table-column prop="id" label="id" align="center" />
    <el-table-column prop="time" label="time" align="center" sortable />


    <el-table-column prop="type" label="type" align="center" :filters="[
      { text: '解析', value: 'parsing' },
      { text: '总结', value: 'feadr' }
    ]" :filter-method="typeFilter">

    </el-table-column>


    <el-table-column prop="username" label="username" align="center" />
    <el-table-column prop="ip" label="ip" align="center" />
    <el-table-column prop="input" label="input"  />

    <el-table-column prop="state" label="state" align="center">
      <template #default="props" >
        <el-icon v-if="props.row.state" color="#529b2e">
          <CircleCheck />
        </el-icon>
        <el-icon v-else color="#c45656">
          <CircleClose />
        </el-icon>
      </template>

    </el-table-column>
  </el-table>

  <!-- :pager-count="11" -->
  <div id="pagination">
    <el-pagination :page-size="pageSize" layout="total,prev, pager, next" :total="total"
      @current-change="currentChange" />
  </div>



</template>

<script lang="ts" setup>
import { ref, reactive } from "vue"
import { getLogTotal, getLogPage } from '@/request/api'
import type { logI } from '@/interfaces'
import type { TableColumnCtx, TableInstance } from 'element-plus'

import {
  CircleCheck,
  CircleClose
} from '@element-plus/icons-vue'

// 一页的个数
let pageSize = 14

// 总页数
let total = ref(0)

// 显示数据
let data = reactive<logI[]>([])

// 获取总页数
getLogTotal().then(res => {
  total.value = res.data
  // totalPages.value=Math.ceil(res.data/20)
}).catch(err => { })

// 获取数据函数
function getData(page: number = 0, ps: number = pageSize) {
  getLogPage(page, ps).then(res => {
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

// 筛选
const typeFilter = (
  value: string,
  row: logI,
  column: TableColumnCtx<logI>
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
