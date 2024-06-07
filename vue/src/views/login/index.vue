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
    height: 80vh;
    display: grid;
    place-items: center;
}
</style>