<template>
  <div id="container">
    <div class="hero">
      <h1 class="animated-text">欢迎来到知料</h1>
      <h3>智能识别配料表，为您提供健康饮食建议</h3>
    </div>
    <div class="features">
      <div class="feature">
        <div class="feature-icon">
          <el-icon>
            <Camera />
          </el-icon>
        </div>
        <h4>智能识别</h4>
        <p>上传配料表图片，自动识别配料信息</p>
      </div>
      <div class="feature">
        <div class="feature-icon">
          <el-icon>
            <DataAnalysis />
          </el-icon>
        </div>
        <h4>深度解析</h4>
        <p>智能分析每项配料，提供详细解释</p>
      </div>
      <div class="feature">
        <div class="feature-icon">
          <el-icon>
            <Apple />
          </el-icon>
        </div>
        <h4>饮食建议</h4>
        <p>根据配料分析结果，给出个性化饮食建议</p>
      </div>
    </div>
    <div class="buttons">
      <el-button type="primary" size="large" @click="router.push('/parsing')" class="action-button">立即体验</el-button>
      <el-button size="large" @click="router.push('/login')" class="login-button">登录账户</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Camera, DataAnalysis, Apple } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router';
const router = useRouter()
</script>

<style scoped>
#container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 60px);
  width: 100%;
  gap: 50px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4edf9 100%);
  padding: 0 20px;
}

.hero {
  text-align: center;
  max-width: 800px;
}

.hero-image {
  margin-top: 30px;
  max-width: 400px;
  margin: 30px auto 0;
}

.hero-image img {
  width: 100%;
  height: auto;
}

h1 {
  font-size: 3.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1rem;
  background: linear-gradient(to right, #409EFF, #36D1DC);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.animated-text {
  animation: fadeInDown 1.2s ease-out;
}

h3 {
  font-size: 1.6rem;
  color: #5c6a79;
  font-weight: 400;
  animation: fadeIn 1.5s ease-out;
}

.features {
  display: flex;
  justify-content: space-around;
  width: 90%;
  max-width: 1200px;
  gap: 30px;
  margin: 0 auto;
}

.feature {
  text-align: center;
  padding: 30px 20px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  flex: 1;
}

.feature:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 35px rgba(64, 158, 255, 0.2);
}

.feature-icon {
  width: 80px;
  height: 80px;
  background: rgba(64, 158, 255, 0.1);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto 20px;
}

.feature-icon .el-icon {
  font-size: 2.5rem;
  color: #409EFF;
}

.feature h4 {
  font-size: 1.4rem;
  color: #2c3e50;
  margin-bottom: 1rem;
  font-weight: 600;
}

.feature p {
  color: #5c6a79;
  font-size: 1.1rem;
  line-height: 1.6;
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 25px;
  margin-top: 20px;
}

.action-button {
  padding: 12px 30px;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 50px;
  box-shadow: 0 8px 15px rgba(64, 158, 255, 0.2);
  transition: all 0.3s ease;
}

.action-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 20px rgba(64, 158, 255, 0.3);
}

.login-button {
  padding: 12px 30px;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 50px;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }

  100% {
    opacity: 1;
  }
}

@keyframes fadeInDown {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 992px) {
  .features {
    width: 95%;
  }
}

@media (max-width: 768px) {
  .features {
    flex-direction: column;
    gap: 25px;
  }

  h1 {
    font-size: 2.8rem;
  }

  h3 {
    font-size: 1.4rem;
  }

  .hero-image {
    max-width: 300px;
  }

  #container {
    height: auto;
    padding: 60px 20px;
  }
}
</style>