<template>
    <div id="routerDiv">
        <RouterView />
    </div>

</template>


<script setup lang="ts">
import { RouterView } from 'vue-router'

</script>

<style scoped>
#routerDiv {
    height: 100vh;
    display: grid;
    place-items: center;
    background-image: url("@/assets/loginBg1.jpg");
    background-repeat: no-repeat;
    background-size: 100%;
}
</style>