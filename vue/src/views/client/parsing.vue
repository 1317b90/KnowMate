<template>
  <!-- 上传图片前 -->
  <div v-if="!isInputImage" id="upfileBefore">

    <h1>上传一张配料表图片</h1>

    <!-- 上传图片框 -->
    <div id="upfileDiv">
      上传图片
      <input type="file" id="inputBtn" accept="image/png,image/jpeg,image/jpg,image/bmp" @change="onInputImage" />
    </div>

    <el-text>要求图片尽量清晰,格式为png,jpg,jpeg,bmp,大小不超过10Mb </el-text>

    <h3>没有图片？可以试试这些配料表：</h3>

    <div id="testDiv">
      <img class="testImg" src="@/assets/testImages/2.jpeg" alt="" @click="onTestImage(2)">
      <img class="testImg" src="@/assets/testImages/3.jpg" alt="" @click="onTestImage(3)">
      <img class="testImg" src="@/assets/testImages/4.jpeg" alt="" @click="onTestImage(4)">
    </div>

  </div>

  <!-- 上传图片后 -->
  <div id="upfileAfter" v-else>
    <!-- 左上 图片展示 -->
    <div id="left1" class="feaCard">
      <el-image id="showImg" :src="imageUrl" :zoom-rate="1.2" :max-scale="7" :min-scale="0.2"
        :preview-src-list="[imageUrl]" show-progress :initial-index="0" fit="cover" />
      <el-button id="reInputButton" type="primary" plain :icon="RefreshLeft" @click="onRefreshImage">重新上传图片</el-button>
    </div>

    <!-- 右上 配料选择 -->
    <div id="right1" class="feaCard">
      <div class="headTitleDiv">
        <div class="headQ"></div>
        <el-text class="headTitle">选择配料</el-text>
      </div>

      <el-text>识别结果可能存在误差,双击可修改配料名称</el-text>

      <!-- 配料标签框 -->
      <div id="tagDiv">
        <el-tag class="elTag" v-for="(tag, index) in foodTags" :key="index" closable :disable-transitions="false"
          @close="handleClose(index)" @click="setTag(index)" size="large">
          <!-- 标签名称展示 -->
          <el-text truncated v-if="!tag.editing">{{ tag.name }}</el-text>
          <!-- 标签编辑输入框 -->
          <input v-else class="tagInput" v-model="tag.name" @blur="saveTag(index)" @keyup.enter="saveTag(index)"
            :autofocus="true" />

        </el-tag>

        <!-- 新增标签输入框 -->
        <el-input id="addInput" v-if="addInputShow" ref="addInputRef" v-model="addInputValue"
          style="width: 100px;margin-bottom: 10px;" @keyup.enter="addTag" @blur="addTag" />

        <!-- 新增标签按钮 -->
        <el-button v-else id="addButton" @click="onAdd">
          + 增加配料
        </el-button>
      </div>

      <!-- 开始解析按钮 -->
      <el-button type="primary" :icon="Aim" @click="onParsing" id="parsingButton">开始解析</el-button>
    </div>

    <!-- 左下 依次解析  -->
    <div id="left2" class="feaCard" v-if="isParsing">
      <el-tabs :tab-position="tabPosition" :stretch="true" @tab-click="onTab" :lazy="true">
        <el-tab-pane v-for="data in parsingData" :key="data.name" :label="data.name">
          <div v-if="isParsingLoading">
            <img class="loadingImg" src="@/assets/loading.gif" alt="">
            <el-text class="headTitle">正在解析 {{ data.name }} ......</el-text>
          </div>
          <showView v-else :Food="data" class="showDiv" />

        </el-tab-pane>
      </el-tabs>


    </div>

    <!-- 右下 配料问答  -->
    <div id="right2" class="feaCard" v-if="isParsing">
      <div class="headTitleDiv">
        <div class="headQ"></div>
        <el-text class="headTitle">配料问答</el-text>
      </div>

      <Chat :question="chatQuestion" style="height: 600px" />
    </div>

  </div>

</template>

<script lang="ts" setup>
import { ref, nextTick, reactive, onMounted, onUnmounted } from 'vue'
import { Aim, RefreshLeft, ArrowRight } from '@element-plus/icons-vue'
import type { foodTagsI, foodI } from '@/interfaces'
import { getImage, requirePath, suppleFormat } from '@/randomImage'
import { ocr, parsing, getUser } from '@/request/api'
import showView from './show.vue'

import Chat from './chatBase.vue'


// 获取cookies中的username，如果不存在，则赋值为访客
const username = sessionStorage.getItem('username') || '访客'

// 上传图片的链接
let imageUrl = ref('')

// 配料标签列表
let foodTags = ref<foodTagsI[]>([])

// 配料名称列表
let foodList: string[] = []

// 配料解析数据
let parsingData = ref<foodI[]>([])

// 总结文本
let feadrText = ref()

// 聊天问题
let chatQuestion = ref('')

// 图片是否上传成功？
let isInputImage = ref(false)

// 上传图片后
function onInputImage(event: Event) {
  const loading = ElLoading.service({
    lock: true,
    text: '正在识别配料表图片......',
    background: 'rgba(0, 0, 0, 0.7)',
  })

  const inputFile = event.target as HTMLInputElement;
  const inputImage = inputFile.files?.item(0);
  if (inputImage) {
    if (inputImage.size / (1024 * 1024) > 10) {
      ElMessage.error('图片大小不能超过10MB')
    } else {
      const imageData = new FormData()
      imageData.append('file', inputImage)
      ocr(imageData).then(res => {
        // 使用URL.createObjectURL创建链接
        imageUrl.value = URL.createObjectURL(inputImage)
        foodTags.value = suppleFormat(res.data)
        isInputImage.value = true

      }).catch(err => {
        ElMessage.error("识别出错," + err)
        onRefreshImage()
      }).finally(() => {
        loading.close()
      })
    }
  } else {
    ElMessage.error("请上传图片")
  }
}


// 点击上传测试图片
function onTestImage(testid: number) {
  const testImage = getImage(testid)
  imageUrl.value = requirePath(testImage.imageUrl)
  foodTags.value = suppleFormat(testImage.foodTags)
  isInputImage.value = true
}


// 点击重新上传图片
function onRefreshImage() {
  imageUrl.value = ''
  isInputImage.value = false
  isParsing.value = false
  foodTags.value = []
  parsingData.value = []
  feadrText.value = ""
  foodList = []
}

// 是否显示新增输入框
const addInputShow = ref(false)

// 新增输入框内容
const addInputValue = ref('')

// 新增输入框返回值
const addInputRef = ref()

// 删除标签
const handleClose = (index: number) => {
  foodTags.value.splice(index, 1)
}

// 点击新增配料按钮，显示新增输入框
const onAdd = () => {
  addInputShow.value = true

  nextTick(() => {
    addInputRef.value!.input!.focus()
  })
}

// 增加配料
const addTag = () => {
  if (addInputValue.value) {
    if (addInputValue.value.length > 15) {
      ElMessage.error("配料名称过长！")
    } else {
      const newTag: foodTagsI = {
        id: foodTags.value.length,
        name: addInputValue.value,
        editing: false
      }
      foodTags.value.push(newTag)
    }

  }
  addInputShow.value = false
  addInputValue.value = ''
}

// 点击标签 修改配料
const setTag = (index: number) => {
  foodTags.value[index].editing = true
}

// 保存标签的修改
const saveTag = (index: number) => {
  foodTags.value[index].editing = false
}


// 记录是否点击开始解析按钮
let isParsing = ref(false)


// 是否正在解析单项配料
const isParsingLoading = ref(false)

// 解析单个配料
async function onlyParsing(foodName: string) {
  // 判断是否已经解析过
  if (!("intro" in parsingData.value[foodList.indexOf(foodName)])) {
    // 解析前重置状态

    isParsingLoading.value = true
    let errorText = ""
    await parsing(foodName, username).then(res => {
      if (res.status === 200) {
        let resFood: foodI = res.data
        parsingData.value[foodList.indexOf(foodName)] = resFood
      } else {
        errorText = "解析失败"
        console.log(res)
      }

    }).catch(err => {

      if (err.response.status === 444) {
        errorText = "解析失败，配料名称有误"
      } else {
        errorText = "解析失败"
      }
      parsingData.value[foodList.indexOf(foodName)] = {
        name: foodName,
        error: errorText
      }

    }
    ).finally(() => {
      isParsingLoading.value = false
    })
  }
}

// 点击切换配料后
function onTab(pane: any) {
  onlyParsing(foodList[pane.index])
}

// 单击解析按钮后
async function onParsing() {
  isParsing.value = false
  // 初始化
  parsingData.value = []
  foodList = []
  feadrText.value = ""

  // 将名称存储到foodlist
  for (const foodTag of foodTags.value) {
    parsingData.value.push({
      name: foodTag.name
    })
    foodList.push(foodTag.name)

  }

  // 设置聊天问题
  getQuestion()
  isParsing.value = true
  try {
    // 默认预先解析第一项配料
    await onlyParsing(foodList[0])
  } catch (err) {
    ElMessage.error("解析出错，" + err)
  }
}


// 写提示词
const getQuestion = () => {
  chatQuestion.value = "# 配料表 \n" + foodList.toString() + "\n# 流程\n请基于食品配料表，用100字以内总结该食品整体健康程度（如：高糖/高盐/添加剂情况、营养价值等），直接给出结论（如'较健康，可适量食用'或'不健康，建议少吃'），避免重复单一项分析。"
  if (username != '访客') {
    getUser(username).then(res => {
      console.log(res.data)
    }).catch(err => { })
  }
}


// 存储屏幕宽度
let tabPosition = ref("right")

// 更新屏幕宽度的函数
const updateScreenWidth = () => {
  if (window.innerWidth < 767) {
    tabPosition.value = "top"
  } else {
    tabPosition.value = "right"
  }
};

// 组件挂载时添加事件监听器
onMounted(() => {
  updateScreenWidth()
  window.addEventListener('resize', updateScreenWidth);
});

// 组件卸载时移除事件监听器
onUnmounted(() => {
  window.removeEventListener('resize', updateScreenWidth);
});

</script>


<style src="@/assets/bus.css"></style>

<style scoped>
#upfileBefore {
  display: flex;
  flex-direction: column;
  /* 纵向排列 */
  justify-content: center;
  /* 垂直居中 */
  align-items: center;
  /* 水平居中 */
  height: calc(100vh - 60px);
  width: 100vw;
  gap: 20px;
}


/* 上传图片框 */
#upfileDiv {
  padding: 10px 30px;
  position: relative;
  display: grid;
  place-items: center;
  overflow: hidden;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  background-color: #0f70e6;
  font-size: 20px;
  color: white;
}

/* 上传图片框悬停效果 */
#upfileDiv:hover {
  background-color: #1a7ff0;
  /* 稍微深一点的蓝色 */
  box-shadow: 0 0 10px rgba(15, 112, 230, 0.5);
  /* 添加淡蓝色阴影 */
  transform: scale(1.05);
  /* 轻微放大效果 */
  transition: all 0.3s ease;
  /* 平滑过渡效果 */
}


/* 隐藏上传文件的控件 */
#inputBtn {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  outline: none;
  background-color: transparent;
  filter: alpha(opacity=0);
  opacity: 0;
  cursor: pointer
}


/* 测试图片div */
#testDiv {
  width: 100%;
  height: 180px;
  display: flex;
  flex-direction: row;
  gap: 15px;
  align-items: center;
  justify-content: center;
  overflow-x: auto;
}

/* 测试图片 */
.testImg {
  height: 80%;
  width: auto;
  object-fit: contain;
  border-radius: 10px;
}

/* 测试图片悬停效果 */
.testImg:hover {
  transform: scale(1.05);
  /* 轻微放大效果 */
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
  /* 添加阴影效果 */
  cursor: pointer;
  /* 鼠标变为手型 */
  transition: all 0.3s ease;
  /* 平滑过渡效果 */
}

#left1 {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 20px;
}


/* 配料标签最外层div */
#tagDiv {
  margin-top: 10px;
}

/* 配料标签框 */
.elTag {
  margin-right: 12px;
  margin-bottom: 12px;
  padding: 8px 12px;
  transition: all 0.2s ease;
}

.elTag:hover {
  transform: translateY(-1px);
}

/* 配料标签文本 */
.elTag .el-text {
  max-width: 150px;
  color: rgb(64, 158, 255);
}

/* 新增标签按钮 */
#addButton {
  margin-bottom: 12px;
  height: 32px;
  transition: all 0.3s ease;
}

#addButton:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 新增输入框背景 */
#addInputTag {
  margin-bottom: 10px;
}

/* 编辑和新增输入框 */
.tagInput {
  background-color: transparent;
  /* 背景透明 */
  border: none;
  /* 取消边框 */
  padding: 0;
  /* 根据需要调整内边距 */
  width: 80px;
}

/* 如果需要取消输入框聚焦时的边框，可以添加以下样式 */
.tagInput:focus {
  outline: none;
  /* 取消聚焦时的边框 */
  box-shadow: none;
  /* 取消聚焦时的阴影 */
}

/* 开始解析按钮 */
#parsingButton {
  margin-top: auto;
  /* 把按钮推到底部 */
  margin-bottom: 10px;
}

/* 加载图标 */
.loadingImg {
  float: left;
  height: 25px;
  width: 25px;
}

#feadrTextDiv {
  margin-top: 10px;
}

#showImg {
  height: 500px;
  width: 100%;
  object-fit: contain;
}

/* 桌面设备样式 */
@media (min-width: 768px) {
  #upfileAfter {
    display: grid;
    grid-template-columns: calc(50vw - 50px) calc(50vw - 50px);
    grid-gap: 40px;
    grid-auto-rows: auto;
    width: 100vw;
    padding: 20px;
  }

  .feaCard {
    padding: 25px;
    background-color: white;
    border-radius: 20px;
  }

  #reInputButton {
    width: 100%;
    margin-top: 15px;
    height: 40px;
    font-weight: 500;
  }

  #parsingButton {
    width: 100%;
    height: 45px;
    margin-top: 20px;
    font-size: 16px;
    font-weight: 500;
  }

  .el-drawer__body {
    display: grid;
    grid-template-columns: calc(50vw - 50px) calc(50vw - 50px);
    grid-gap: 40px;
    padding: 20px;
  }
}

/* 移动设备样式 */
@media (max-width: 767px) {
  #upfileAfter {
    width: 100vw;
    padding: 15px;
    display: flex;
    flex-direction: column;
    gap: 25px;
  }

  .feaCard {
    padding: 20px;
    background-color: white;
    border-radius: 15px;
  }

  #reInputButton {
    width: 100%;
    margin-top: 15px;
    height: 40px;
  }

  #parsingButton {
    width: 100%;
    height: 45px;
    margin-top: 15px;
    font-size: 16px;
  }

  .el-drawer__body {
    display: flex;
    flex-direction: column;
    gap: 25px;
    padding: 15px;
  }
}
</style>
