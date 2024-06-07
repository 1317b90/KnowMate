<template>
  <!-- 上传图片前 -->
  <div v-if="!imageUrl">
    <!-- 上传图片框 -->
    <div id="inputDiv">
      <UploadFilled style="width: 3em; height: 3em" />
      <h2>上传配料表图片</h2>
      <el-text>要求图片尽量清晰,格式为png,jpg,jpeg,bmp,大小不超过20Mb </el-text>
      <br>
      <input type="file" id="inputBtn" accept="image/png,image/jpeg,image/jpg,image/bmp" @change="onInputImage" />
    </div>

    <!-- 使用测试图片 -->
    <el-button id="testButton" type="primary" plain text bg :icon="PictureRounded"
      @click="onTestImage">使用测试图片</el-button>
  </div>

  <!-- 上传图片后 -->
  <div id="all" v-if="imageUrl">
    <!-- 左上 图片展示 -->
    <div id="left1" class="feaCard" v-loading="inputLoading" element-loading-text="正在识别图片中的配料名称 ...">
      <!-- 图片展示 -->
      <img id="showImg" :src="imageUrl">
      <br>
      <!-- 重新上传按钮 v-if="isInputImage" -->
      <el-button id="reInputButton" type="primary" plain :icon="RefreshLeft" @click="onRefreshImage">重新上传图片</el-button>

    </div>

    <!-- 右上 配料选择 -->
    <div id="right1" class="feaCard" v-if="isInputImage">
      <!-- 配料标签上面的提示 -->
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
      <el-button type="primary" :icon="Aim" @click="onParsing" id="parsingButton"
        :loading="parsingLoading">开始解析</el-button>
    </div>

    <!-- 左下 食品评价与饮食建议  -->
    <div id="left2" class="feaCard" v-if="isParsing">
      <div class="headTitleDiv" v-if="feadrText">
        <div class="headQ"></div>
        <el-text class="headTitle">食品评价与饮食建议</el-text>
      </div>

      <div v-else>
        <img class="loadingImg" src="@/assets/loading.gif" alt="">
        <el-text class="headTitle">正在对食品整体进行解析 ......</el-text>
      </div>

      <div v-html="feadrText" v-if="feadrText" id="feadrTextDiv"></div>

    </div>

    <!-- 右下 依次解析  -->
    <div id="right2" class="feaCard" v-if="isParsing">
      <el-tabs :tab-position="tabPosition" :stretch="true" @tab-click="onTab" :lazy="true">
        <el-tab-pane v-for="data in parsingData" :key="data.name" :label="data.name">
          <showView v-if="'intro' in data" :Food="data" class="showDiv" />
          <div v-else>
            <img class="loadingImg" src="@/assets/loading.gif" alt="">
            <el-text class="headTitle">正在解析 {{ data.name }} ......</el-text>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

  </div>

</template>

<script lang="ts" setup>
import { ref, nextTick, reactive, onMounted, onUnmounted } from 'vue'
import { UploadFilled, Aim, PictureRounded, RefreshLeft } from '@element-plus/icons-vue'
import type { foodTagsI, foodI } from '@/interfaces'
import { randomImage, requirePath } from '@/randomImage'
import { ocr, parsing, feadr } from '@/request/api'
import { marked } from 'marked'
import showView from './show.vue'

// 获取cookies中的username，如果不存在，则赋值为访客
const username = sessionStorage.getItem('username') || '访客'

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

// 上传图片的链接
let imageUrl = ref('')

// 配料标签列表
let foodTags = ref<foodTagsI[]>([])

// 配料名称列表
let foodList: string[] = []

// 配料解析数据
let parsingData = reactive<foodI[]>([])

// 评分文本
let feadrText = ref()


// 上传图片的加载状态
let inputLoading = ref(false)

// 图片是否上传成功？
let isInputImage = ref(false)

// 点击上传图片后
async function onInputImage(event: Event) {
  inputLoading.value = true
  const inputFile = event.target as HTMLInputElement;
  const inputImage = inputFile.files?.item(0);
  if (inputImage) {
    if (inputImage.size / (1024 * 1024) > 20) {
      ElMessage.error('图片大小不能超过20MB')
    } else {
      // 使用URL.createObjectURL创建链接
      imageUrl.value = URL.createObjectURL(inputImage)

      const imageData = new FormData()
      imageData.append('file', inputImage)

      await ocr(imageData).then(res => {
        if (res.status === 200) {
          foodTags.value = res.data
          isInputImage.value = true
          inputLoading.value = false
        }
      }).catch(err => {
        ElMessage.error("识别出错,请重新上传图片!")
        onRefreshImage()
        console.log(err)
        inputLoading.value = false
      }
      )
    }
  }
}


// 点击上传测试图片
function onTestImage() {
  const testImage = randomImage()
  imageUrl.value = requirePath(testImage.imageUrl)
  foodTags.value = testImage.foodTags
  isInputImage.value = true
}

// 点击重新上传图片
function onRefreshImage() {
  imageUrl.value = ''
  isInputImage.value = false
  isParsing.value = false
  foodTags = ref<foodTagsI[]>([])
  parsingData = reactive<foodI[]>([])
  feadrText = ref()
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

// 解析按钮的加载状态
let parsingLoading = ref(false)

// 记录是否点击开始解析按钮
let isParsing = ref(false)

// 解析单个配料
async function onlyParsing(foodName: string) {
  // 判断是否已经解析过
  if (!("intro" in parsingData[foodList.indexOf(foodName)])) {
    await parsing(foodName, username).then(res => {
      console.log(res)
      if (res.status === 200) {
        parsingData[foodList.indexOf(foodName)] = res.data
      }else{
        console.log(res)
      }
    }).catch(err => {
      let errorText = ""
      if (err.response.status === 444) {
        errorText = "解析失败，配料名称有误"
      } else {
        errorText = "解析失败"
      }
      parsingData[foodList.indexOf(foodName)] = {
        name: foodName,
        error: errorText
      }
      console.log(err)
    }
    )
  }
}

// 点击tabs配料后
function onTab(pane: any) {
  onlyParsing(foodList[pane.index])
}

// 单击解析按钮后
async function onParsing() {
  // 初始化
  isParsing.value = true
  parsingData = reactive<foodI[]>([])
  foodList = []

  // 将名称存储到foodlist
  for (const foodTag of foodTags.value) {
    parsingData.push({
      name: foodTag.name
    })
    foodList.push(foodTag.name)
  }
  // 所有配料名称连接
  let foodListText: string = foodList.toString()

  // 食品评价与建议
  await feadr(foodListText, username).then(res => {
    feadrText.value = marked(res.data)
  }).catch(err => {
    console.log(err)
  })


  // 默认预先解析第一项配料
  await onlyParsing(foodList[0]).then(res => { }).catch(err => { })
}


</script>

<style src="@/assets/bus.css"></style>

<style scoped>
/* 上传图片框 */
#inputDiv {
  padding: 20px;
  position: relative;
  display: grid;
  place-items: center;
  overflow: hidden;
  border: dashed 1px #7EA9FF;
  border-radius: 10px;
  cursor: pointer
}

/* 上传文件标题 */
#inputDiv h2 {
  color: #7EA9FF;
  font-weight: 450;
  letter-spacing: 1px;
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

/* 使用测试图片的按钮 */
#testButton {
  margin-top: 10px;
  width: 100%;
}

/* 配料标签最外层div */
#tagDiv {
  margin-top: 10px;
}

/* 配料标签框 */
.elTag {
  margin-right: 10px;
  margin-bottom: 10px;
}

/* 配料标签文本 */
.elTag .el-text {
  max-width: 150px;
  color: rgb(64, 158, 255);
}

/* 新增标签按钮 */
#addButton {
  margin-bottom: 10px;
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


/* 桌面设备样式 */
@media (min-width: 768px) {
  #inputDiv {
    width: 430px;
  }

  #all {
    display: grid;
    grid-template-columns: 40vw 50vw;
    grid-gap: 20px;
    grid-auto-rows: auto;
    width: 92vw;
  }

  #showImg {
    width: 37vw;
  }

  #reInputButton {
    width: 37vw;
  }

  .feaCard {
    /* border: solid 1px darkgray; */
    box-shadow: rgba(0, 0, 0, 0.3) 0px 0px 6px 0px;
    padding: 20px;
  }

  #right2 {
    padding-right: 0px;
  }

  .showDiv {
    padding-left: 10px;
    padding-right: 10px;
  }
}

/* 移动设备样式 */
@media (max-width: 767px) {
  #inputDiv {
    width: 90vw;
  }

  #all {
    width: 90vw;
  }

  #showImg {
    width: 90vw;
  }

  #reInputButton {
    width: 90vw;
  }

  #right1 {
    margin-top: 20px;
    width: 90vw;
  }

  #parsingButton {
    margin-top: 10px;
    width: 90vw;
  }

  .showDiv {
    width: 90vw;
  }

  #left2 {
    margin-top: 10px;
  }

  #right2 {
    margin-top: 10px;
  }
}
</style>