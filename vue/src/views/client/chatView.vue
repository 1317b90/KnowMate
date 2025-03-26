<template>
    <div id="container">
        <Chat />
    </div>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';
import Chat from './chatBase.vue';

</script>

<style scoped>
#container {
    height: calc(100vh - 60px);
    width: 100vw;
    padding: 40px 100px;
    background-color: white
}
</style>
