<template>
    <div class="nested-component d-flex justify-content-center align-items-center" @click="handleClick">
        <img :src="link" class="nested " alt="img">
    </div>
</template>

<script>
    export default {
        name: 'NestedImage',
        props: {
            link: {
                type: String,
                required: true
            }
        },
        methods: {
            handleClick() {
                this.$emit('image-clicked', this.link);
            }
        }
    };
</script>

<style scoped>
    .nested-component {
        height: 100%; 
        background-color: #25262B;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .nested {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }
</style>