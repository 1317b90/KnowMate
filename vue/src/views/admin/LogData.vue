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
    <el-table-column prop="input" label="input" />

    <el-table-column prop="state" label="state" align="center">
      <template #default="props">
        <el-icon v-if="props.row.state" color="#529b2e">
          <CircleCheck />
        </el-icon>
        <el-icon v-else color="#c45656">
          <CircleClose />
        </el-icon>
      </template>
    </el-table-column>
  </el-table>

  <div id="pagination">
    <el-pagination :page-size="pageSize" layout="total, prev, pager, next" :total="total"
      @current-change="currentChange" />
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from "vue"
import { getLogs } from '@/request/api'
import type { logI } from '@/interfaces'
import type { TableColumnCtx } from 'element-plus'

import {
  CircleCheck,
  CircleClose
} from '@element-plus/icons-vue'

// 一页的个数
const pageSize = 14

// 总页数
const total = ref(0)

// 显示数据
const data = reactive<logI[]>([])

// 获取数据函数
const getData = async (page: number = 1) => {
  try {
    const res = await getLogs(page - 1, pageSize)
    total.value = res.data.total
    // 使用 splice 替换 data 数组的内容,防止响应失效
    data.splice(0, data.length, ...res.data.data)
  } catch (err) {
    ElMessage.error('获取日志数据失败：'+err)
  }
}

// 切换页码后
const currentChange = (value: number) => {
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

// 组件挂载时获取第一页数据
onMounted(() => {
  getData()
})

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
