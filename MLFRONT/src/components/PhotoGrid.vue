<template>
    <div class="overflow-auto" style="height:100%">
        <div class="row">
            <div class="col-md-2 nested rounded" v-for="(image, index) in sortedImages" :key="index">
                <NestedImage :link="image.path" @image-clicked="showPhotoDetails(image)" style="cursor: pointer;"/>
            </div>
        </div>
        <PhotoDetails v-if="selectedImage" :link="selectedImage.path" :name="selectedImage.filename"  @close-overlay="hidePhotoDetails" />
    </div>
</template>

<script>
    import NestedImage from './NestedImage.vue';
    import PhotoDetails from './PhotoDetails.vue';

    // Create a context for all images in the assets/generated directory
    const requireContext = require.context('@/assets/generated', false, /\.(png|jpe?g|svg)$/);


    const images = requireContext.keys().map(key => ({
        path: requireContext(key),
        filename: key
    }));

    export default {
        name: 'GridComponent',
        components: {
            NestedImage,
            PhotoDetails
        },
        data() {
            return {
                images,
                selectedImage: null,
                prompts: null,
            };
        },
        computed: {
            sortedImages() {
                // Sort images based on the timestamp in their filenames
                return images.sort((a, b) => {
                    const timestampA = a.filename.match(/\d{8}_\d{6}/)[0];
                    const timestampB = b.filename.match(/\d{8}_\d{6}/)[0];
                    return timestampB.localeCompare(timestampA);
                });
            }
        },
        methods: {
            showPhotoDetails(image) {
                this.selectedImage = image;
            },
            hidePhotoDetails() {
                this.selectedImage = null;
            }
        }
    };
</script>

<style scoped>
    .nested {
        margin: 1.5%;
        background: linear-gradient(to right, #FF33CC, #0066CC);
        height: 15vh;
        padding: 3px;
        transition: all 0.3s ease;
    }

        .nested:hover {
            padding: 10px;
        }
</style>