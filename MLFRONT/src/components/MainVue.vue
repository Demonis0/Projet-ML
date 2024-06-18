<template>
    <div class="container-fluid vh-100">
        <div class="row h-100">
            <div class="col-2 color1 prompter" style="height:100%">
                <ChatBotComponent />
            </div>
            <div class="col-10 color2 photogrid" style="height:100%">
                <PhotoGrid/>
            </div>
        </div>
    </div>
</template>

<script>
    import ChatBotComponent from '../components/ChatBotComponent.vue'
    import PhotoGrid from '../components/PhotoGrid.vue'
    export default {
        name: 'MainVue',
        components: {
            ChatBotComponent,
            PhotoGrid
        },
        data() {
            return {
                scrolled: false
            };
        },
        
    };
</script>

<style scoped>
    .color1 {
        background-color: #25262B
    }
    .color2 {
        background-color: #1A1B1E
    }
    @media (max-width: 768px)  {
        .prompter {
            display: none
        }
        .photogrid{
            width:100%
        }
    }
</style>