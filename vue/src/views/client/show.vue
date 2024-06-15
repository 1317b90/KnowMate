<template>
  <el-space direction="vertical" alignment="normal">
    <!-- 标题与头 -->
    <div class="headTitleDiv">
      <div class="headQ"></div>
      <el-text class="headTitle">{{ Food.name }}</el-text>
      <!-- 如果配料的类型存在，则渲染 -->
      <el-tag v-if="Food.type" class="foodType">{{ Food.type }}</el-tag>
      <!-- 如果配料解析出错了，则将错误原因展示 -->
      <el-tag v-else class="foodType" type="danger">{{ Food.error }}</el-tag>
    </div>

    <!-- 简介 -->
    <div v-if="Food.intro" class="foodCard "><el-text>{{ Food.intro }}</el-text></div>

    <!-- 在食物中的作用 -->
    <div v-if="Food.effect" class="foodCard BCb_">
      <div class="headTitleDiv">
        <div class="headQ_ BCb"></div>
        <el-text class="headTitle_">在食物中的作用</el-text>
      </div>

      <el-text>{{ Food.effect }}</el-text>
    </div>

    <!-- 有害或有益的原因 -->
    <div v-if="Food.harmReason" :class="harmClass">
      <div class="headTitleDiv">
        <div :class="harmQClass"></div>
        <el-text class="headTitle_">{{ harmTitle }}</el-text>
      </div>
      <el-text>{{ Food.harmReason }}</el-text>
    </div>

    <!-- 不适宜人群 -->
    <div v-if="Food.out" class="foodCard BCr_">
      <div class="headTitleDiv">
        <div class="headQ_ BCr"></div>
        <el-text class="headTitle_">不适宜人群</el-text>
      </div>

      <el-text>{{ Food.out }}</el-text>
    </div>

    <!-- 法律法规 -->
    <div v-if="Food.ruler" class="foodCard BCa_">
      <div class="headTitleDiv">
        <div class="headQ_ BCb"></div>
        <el-text class="headTitle_">相关标准法规和信息</el-text>
      </div>

      <a v-for="ruler in Food.ruler" :href="ruler.url" target="_blank" class="rulerA"><el-text>《{{ ruler.title
          }}》</el-text></a>
    </div>
  </el-space>
</template>

<script lang="ts" setup>

const propsData = defineProps(['Food'])
const Food = propsData.Food
let harmClass = "foodCard BCa_"
let harmQClass = "headQ_ BCb"
let harmTitle = "对人体健康是否有益"


if (Food.harmType == "有害") {
  harmClass = "foodCard BCy_"
  harmQClass = "headQ_ BCy"
  harmTitle = "对人体健康可能有害"
} else if (Food.harmType == "有益") {
  harmClass = "foodCard BCg_"
  harmQClass = "headQ_ BCg"
  harmTitle = "对人体健康可能有益"
}

</script>

<style src="@/assets/bus.css"></style>

<style scoped>
.foodType {
  margin-left: 15px;
}

.rulerA {
  display: inline-block;
}
</style>
