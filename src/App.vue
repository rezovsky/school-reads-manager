<template>
  <TextbookList v-bind:textbooks="textbooks"/>
</template>

<script>
import TextbookList from "@/components/TextbookList.vue";
export default {
  components: {
    TextbookList
  },
  data() {
    return {
        textbooks: [
            {
                id: 1,
                name: 'Textbook 1',
                author: 'Author 1',
            },
            {
                id: 2,
                name: 'Textbook 2',
                author: 'Author 2',
            }
        ]
    }
  }
}
</script>

<style>

</style>