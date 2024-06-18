<template>
    <body>
        <MainVue/>
    </body>
</template>

<script>
import MainVue from './components/MainVue.vue'
export default {
  name: 'App',
  components: {
    MainVue
  }
}
</script>

<style>
    .gallery {
        background-color: #212123;
    }
    header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1000
    }
</style>