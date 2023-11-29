<template>
    <div v-for="textbook in textbooks">
        <h1>{{ textbook.id }} {{ textbook.name }} {{ textbook.author }}</h1>
    </div>
</template>

<script>
export default {
    props: {
      textbooks: {
        type: Array,
        required: true
      }
    }
}
</script>

<style lang="scss" scoped>

</style>