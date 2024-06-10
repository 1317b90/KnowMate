<template>
  <div id="all">
    <div id="a" class="gridDiv">
      <div class="gridTitle">
        <h4>访问量</h4>
        <el-divider />
      </div>

      <div id="viewsDiv" class="gridMain">
        <img class="icon" src="@/assets/viewsIcon.png" alt="">
        <el-statistic title="日访问量" :value="coolDayViews" />
        <el-statistic title="总访问量" :value="coolAllViews" />
      </div>

    </div>

    <div id="b" class="gridDiv">
      <div class="gridTitle">
        <h4>配料数据</h4>
        <el-divider />
      </div>
      <div class="chartDiv" ref="foodRef"></div>
    </div>

    <div id="c" class="gridDiv">
      <div class="gridTitle">
        <h4>用户数据</h4>
        <el-divider />
      </div>
      <el-tabs v-model="userTabsValue" lazy="true">
        <el-tab-pane label="性别" name="gender">
          <div class="userChartDiv" ref="userRef1"></div>
        </el-tab-pane>
        <el-tab-pane label="过敏原" name="allergy">
          <div class="userChartDiv" ref="userRef2"></div>
        </el-tab-pane>
        <el-tab-pane label="病史" name="disease">
          <div class="userChartDiv" ref="userRef3"></div>
        </el-tab-pane>
        <el-tab-pane label="营养需求" name="need">
          <div class="userChartDiv" ref="userRef4"></div>
        </el-tab-pane>
        <el-tab-pane label="体重目标" name="goals">
          <div class="userChartDiv" ref="userRef5"></div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <div id="d" class="gridDiv">
      <div class="gridTitle">
        <h4>配料解析量</h4>
        <el-divider />
      </div>
      <div id="parsingDiv" class="gridMain">
        <img class="icon" src="@/assets/parsingIcon.png" alt="">
        <el-statistic title="日解析量" :value="coolDayParsing" />
        <el-statistic title="总解析量" :value="coolAllParsing" />
      </div>
      <el-progress :percentage="parsingA" :format="progressFormat" id="parsingProgress" />
    </div>


    <div id="e" class="gridDiv">
      <div class="gridTitle">
        <h4>流量趋势</h4>
        <el-divider />
      </div>
      <div class="chartDiv" ref="fluxRef"></div>
    </div>

    <div id="f" class="gridDiv">
      <div class="gridTitle">
        <h4>用户身高体重分布</h4>
        <el-divider />
      </div>
      <div class="chartDiv" ref="userRef6"></div>
    </div>

  </div>

</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

import { useTransition } from '@vueuse/core'

import * as echarts from 'echarts/core';

import {
  PieChart,
  LineChart,
  BarChart,
  ScatterChart
} from 'echarts/charts';

import {
  GridComponent,
  TooltipComponent,
  TitleComponent,
  VisualMapComponent,
  LegendComponent,
  ToolboxComponent
} from 'echarts/components';

import { LabelLayout } from 'echarts/features';

import { UniversalTransition } from 'echarts/features';

import { CanvasRenderer } from 'echarts/renderers';
import { formatter } from 'element-plus';

// 使用刚指定的组件和渲染器注册 echarts
echarts.use(
  [TitleComponent,
    LegendComponent,
    LabelLayout,
    TooltipComponent,
    GridComponent,
    ToolboxComponent,
    PieChart,
    CanvasRenderer,
    LineChart,
    VisualMapComponent,
    BarChart,
    ScatterChart,
    UniversalTransition
  ]
);

// 日访问量

const dayViews = ref(0)
const coolDayViews = useTransition(dayViews, {
  duration: 1500,
})


// 总访问量
const allViews = ref(0)
const coolAllViews = useTransition(allViews, {
  duration: 1500,
})
allViews.value = 1547


// 成功解析率
let parsingA = ref(99)
let parsingB = ref(100)

// 日解析量
const dayParsing = ref(0)
const coolDayParsing = useTransition(dayParsing, {
  duration: 1500,
})



// 总解析量
const allParsing = ref(0)
const coolAllParsing = useTransition(allParsing, {
  duration: 1500,
})

allParsing.value = 2069


// 返回近30天数据
function getLast30Days(): string[] {
  const dates: string[] = [];
  const today = new Date();

  for (let i = 30; i >= 0; i--) {
    const pastDate = new Date(today);
    pastDate.setDate(today.getDate() - i);
    const year = pastDate.getFullYear();
    const month = String(pastDate.getMonth() + 1).padStart(2, '0'); // getMonth() returns 0-based month
    const day = String(pastDate.getDate()).padStart(2, '0');
    dates.push(`${year}-${month}-${day}`);
  }

  return dates;
}
let fluxX = getLast30Days()

let fluxParsingY = [
  11,
  7,
  35,
  15,
  40,
  26,
  40,
  39,
  33,
  30,
  13,
  25,
  18,
  27,
  38,
  12,
  42,
  38,
  19,
  30,
  1,
  1,
  30,
  20,
  35,
  36,
  41,
  39,
  14,
  13,
  19
]
let fluxViewsY = [
  3,
  18,
  1,
  26,
  28,
  28,
  26,
  10,
  2,
  9,
  24,
  20,
  5,
  13,
  28,
  12,
  9,
  28,
  24,
  7,
  11,
  26,
  13,
  17,
  9,
  10,
  24,
  26,
  8,
  26,
  36
]

dayViews.value = fluxParsingY[fluxParsingY.length - 1]
dayParsing.value = fluxViewsY[fluxViewsY.length - 1]

let userTabsValue = ref("gender")


// 配料图表

let foodRef = ref(null)
let fluxRef = ref(null)
let userRef1 = ref(null)
let userRef2 = ref(null)
let userRef3 = ref(null)
let userRef4 = ref(null)
let userRef5 = ref(null)
let userRef6 = ref(null)

// 用户数据
let userData1 = [
  { value: 10, name: '男' },
  { value: 12, name: '女' },
  { value: 8, name: '空白' },
]

let userData2 = [
  { value: 2, name: '蛋白质' },
  { value: 2, name: '海鲜' },
  { value: 1, name: '坚果' },
  { value: 1, name: '豆制品' },
  { value: 24, name: '其他' },
]

let userData3 = [
  { value: 2, name: '糖尿病' },
  { value: 1, name: '高血压' },
  { value: 0, name: '心脏病' },
  { value: 2, name: '肠胃敏感' },
  { value: 1, name: '肾病' },
  { value: 24, name: '其他' },
]

let userData4 = [
  { value: 1, name: '增重' },
  { value: 8, name: '减肥' },
  { value: 21, name: '无' },
]

let userData5 = [
  { value: 2, name: '高蛋白' },
  { value: 5, name: '低碳水化合物' },
  { value: 8, name: '低脂饮食' },
  { value: 18, name: '其他' },
]
// 用户饼图配置
function getUserOption(data: any) {
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)',
      backgroundColor: 'rgba(255,255,255,0.85)'
    },
    series: [
      {
        name: '',
        type: 'pie',
        radius: ['20%', '80%'],
        labelLine: {
          length: 30
        },
        label: {
          show: true,  // 显示标签
          formatter: '{b}\n{c} {d}%',  // 自定义标签格式
          position: 'outside'
        },
        data: data,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 5
        }
      }
    ]
  }
}


onMounted(() => {
  let foodInstance = echarts.init(foodRef.value);
  const foodOption = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)',
      backgroundColor: 'rgba(255,255,255,0.85)'
    },
    series: [
      {
        name: '健康影响类型',
        type: 'pie',
        selectedMode: 'single',
        radius: [0, '30%'],
        label: {
          position: 'inner',
          fontSize: 14
        },
        labelLine: {
          show: false
        },
        data: [
          { value: 154, name: '有益' },
          { value: 20, name: '有害' },
          { value: 69, name: '不确定', selected: true }
        ],
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
        }
      },
      {
        name: '配料类型',
        type: 'pie',
        radius: ['45%', '80%'],
        labelLine: {
          length: 30
        },
        label: {
          show: true,  // 显示标签
          formatter: '{b}\n{c} {d}%',  // 自定义标签格式
          position: 'outside'
        },
        data: [
          { value: 104, name: '食品添加剂' },
          { value: 33, name: '普通食品原料' },
          { value: 31, name: '营养强化剂' },
          { value: 25, name: '新食品原料' },
          { value: 23, name: '提取物' },
          { value: 14, name: '保健食品' },
          { value: 84, name: '其他' },
        ],
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 5
        }
      }
    ]
  }

  foodInstance.setOption(foodOption);


  // 流量图表初始化

  let fluxInstance = echarts.init(fluxRef.value);

  let fluxOption = {
    color: ['#80FFA5', '#00DDFF', '#37A2FF', '#FF0087', '#FFBF00'],
    tooltip: {
      trigger: 'axis',

      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: '#6a7985'
        }
      }
    },
    legend: {
      data: ['访问量', '解析量'],
      top: 10,
      right: 10,
    },
    grid: {
      left: '3%',
      right: '3%',
      bottom: '3%',
      top: '8%',
      containLabel: true
    },
    xAxis: [
      {
        type: 'category',
        boundaryGap: false,
        data: fluxX
      }
    ],
    yAxis: [
      {
        type: 'value'
      }
    ],
    series: [
      {
        name: '访问量',
        type: 'line',
        stack: 'Total',
        smooth: true,
        lineStyle: {
          width: 0
        },
        showSymbol: false,
        areaStyle: {
          opacity: 0.8,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: 'rgb(128, 255, 165)'
            },
            {
              offset: 1,
              color: 'rgb(1, 191, 236)'
            }
          ])
        },
        emphasis: {
          focus: 'series'
        },
        data: fluxViewsY
      },
      {
        name: '解析量',
        type: 'line',
        stack: 'Total',
        smooth: true,

        lineStyle: {
          width: 0
        },
        showSymbol: false,
        areaStyle: {
          opacity: 0.8,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: 'rgb(0, 221, 255)'
            },
            {
              offset: 1,
              color: 'rgb(77, 119, 255)'
            }
          ])
        },
        emphasis: {
          focus: 'series'
        },
        data: fluxParsingY
      },
    ]
  };
  fluxInstance.setOption(fluxOption);



  // 用户图表
  echarts.init(userRef1.value).setOption(getUserOption(userData1))
  echarts.init(userRef2.value).setOption(getUserOption(userData2))
  echarts.init(userRef3.value).setOption(getUserOption(userData3))
  echarts.init(userRef4.value).setOption(getUserOption(userData4))
  echarts.init(userRef5.value).setOption(getUserOption(userData5))


  let userInstance6 = echarts.init(userRef6.value);

  // 身高体重数据
  var hwdata = [
    [50, 155],
    [68, 181],
    [77, 177],
    [74, 171],
    [61, 169],
    [80, 173],
    [46, 156],
    [50, 164],
    [71, 182],
    [63, 168],
    [49, 159],
    [66, 174],
    [48, 157],
    [66, 168],
    [72, 173],
    [65, 172],
    [45, 152],
    [49, 160],
    [57, 165],
    [52, 163],
    [43, 156],
    [45, 158],
    [62, 169],
    [65, 176],
    [62, 171],
    [47, 166],
    [56, 163],
    [80, 185],
    [55, 157]
  ]


  // 指定图表的配置项和数据
  let userOption = {
    grid: {
      containLabel: true,
      left: '3%',
      right: '4%',
      bottom: '3%',
      containGrid: false
    },
    xAxis: {
      type: 'value',
      splitLine: {
        show: false
      },
      min: 'dataMin', // 体重最小值
    },
    yAxis: {
      type: 'value',
      splitLine: {
        show: false
      },
      min: 'dataMin', // 身高最小值
    },
    series: [{
      name: '身高体重分布',
      type: 'scatter',
      data: hwdata
    }],
    // 提示框
    tooltip: {
      trigger: 'axis',

      axisPointer: {
        type: 'cross',

      },
      formatter: '{c}',
    },

    visualMap: {
      type: 'continuous',
      min: 140,
      max: 200,
      calculable: false,
      inRange: {
        color: ['#5ce0da', '#5dadff', "#7d70ee", "#f49e4e"], // 颜色范围
      },
      // orient: 'horizontal', // 调整图例的方向为水平
      right: '0%',
      top: '15%'
    }
  };

  userInstance6.setOption(userOption);

});


// 进度条文本格式
const progressFormat = (percentage: any) => (`解析成功率: ${percentage}%`)

</script>

<style scoped>
#all {
  width: 100%;
  height: 100%;

  display: grid;
  grid-template-columns: 25% 36% 36%;
  grid-template-rows: 23% 28% 44%;
  grid-row-gap: 20px;
  grid-column-gap: 20px;
  grid-template-areas: 'a b c'
    'd b c'
    'e e f';
}

#a {
  grid-area: a;
}

#b {
  grid-area: b;
}

#c {
  grid-area: c;
}

#d {
  grid-area: d;
}

#e {
  grid-area: e;
}

#f {
  grid-area: f;
}

/* 每个单元格边框 */
.gridDiv {
  height: 100%;
  width: 100%;
  box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.12);
  padding: 10px;
}

/* 每个单元格标题 */
.gridTitle {
  height: 30px;
}

/* 标题下面的分割线 */
.gridTitle>.el-divider {
  margin: 10px 10px 10px 0px;
}

/* 单元格主要内容 */
.gridMain {
  width: 100%;
  height: 110%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 图表内容 */
.chartDiv {
  height: 90%;
  width: 100%;
}

/* 访问量内容框框 */
#viewsDiv {
  gap: 40px;
}

#parsingDiv {
  gap: 40px;
  height: 80%;
}

#parsingProgress {
  margin-left: 10px;
  height: 0%;
  width: 90%;
}

/* 数字显示 */
::v-deep .el-statistic__number {
  font-size: 25px;
  font-weight: 500;
}

.icon {
  width: 60px;
}

.userChartDiv {
  height: 35vh;
  width: 30vw;
}
</style>
