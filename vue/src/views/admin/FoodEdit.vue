<template>
    <div id="editAll">
        <div id="editDiv">
            <h3 style="text-align: center; margin-bottom: 15px;">增加配料数据</h3>
            <editView />
        </div>
    </div>

</template>


<script setup lang="ts">
import editView from './FoodEditModel.vue'

</script>

<style scoped>
#editAll {
    width: 100%;
    display: flex;
    justify-content: center;
}

#editDiv {
    width: 500px;
    padding: 30px;
    border-radius: 10px;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 0px 5px 0px;
}
</style>