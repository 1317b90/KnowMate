<template>
<div id="editDiv">
    <editView/>
</div>

</template>


<script setup lang="ts">
import editView from './FoodEditModel.vue'

</script>

<style scoped>
#editDiv{
    width: 500px;
    padding: 30px;
    border-radius: 10px;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 0px 5px 0px;
}
</style>