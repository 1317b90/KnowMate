<template>
  <div id="container">
    <div class="hero">
      <h1>欢迎来到知料</h1>
      <h3>智能识别配料表，为您提供健康饮食建议</h3>
    </div>
    <div class="features">
      <div class="feature">
        <i class="el-icon-camera"></i>
        <h4>智能识别</h4>
        <p>上传配料表图片，自动识别配料信息</p>
      </div>
      <div class="feature">
        <i class="el-icon-data-analysis"></i>
        <h4>深度解析</h4>
        <p>智能分析每项配料，提供详细解释</p>
      </div>
      <div class="feature">
        <i class="el-icon-apple"></i>
        <h4>饮食建议</h4>
        <p>根据配料分析结果，给出个性化饮食建议</p>
      </div>
    </div>
    <div class="buttons">
      <el-button type="primary" size="large" @click="router.push('/')">前往使用</el-button>
      <el-button size="large" @click="router.push('/login')">登录用户</el-button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const startAnalysis = () => {
  router.push('/parsing');
};
</script>

<style scoped>
#container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 60px);
  width: 100vw;
  gap: 40px;

}

.hero {
  text-align: center;
}

h1 {
  font-size: 3rem;
  color: #409EFF;
  margin-bottom: 1rem;
}

h3 {
  font-size: 1.5rem;
  color: #606266;
}

.features {
  display: flex;
  justify-content: space-around;
  width: 80%;
  max-width: 1200px;
}

.feature {
  text-align: center;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.feature:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15);
}

.feature i {
  font-size: 3rem;
  color: #409EFF;
  margin-bottom: 1rem;
}

.feature h4 {
  font-size: 1.2rem;
  color: #303133;
  margin-bottom: 0.5rem;
}

.feature p {
  color: #606266;
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

@media (max-width: 768px) {
  .features {
    flex-direction: column;
    gap: 20px;
  }
}
</style>
