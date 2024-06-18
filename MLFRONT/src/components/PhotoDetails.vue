<template>
    <div class="overlay-component" @click.self="hideOverlay">
        <div class="" @click.self="hideOverlay" style="color:white;position:absolute;bottom:10px"><h2 @click.self="hideOverlay">click here to go back</h2></div>
        <div class="overlay-content">
            <div class="row h-100">
                <div class="col-3 color1 rounded-left" style="height:100%">
                    <div class="" style="height:100%">
                        <div class="" style="height:80%">
                            <div class="p-2" style="max-height:25%">
                                <div class="border-bottom text-white" style="height:100%">
                                    <!-- First part -->
                                    <h4>Generated :</h4>
                                    <p>{{getTimestamp}}</p>
                                </div>
                            </div>
                            <div class="p-2 border-bottom text-white" style="max-height:75%;margin-top:10px;">
                                    <!-- Second part -->
                                    <h4>Prompt:</h4>
                                    <p class="overflow-auto" style="max-height:30vh">{{getPrompt}}</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-9 color2 rounded-right" style="height:100%">
                    <div class="nested-component d-flex justify-content-center align-items-center" style="height:100%">
                        <img :src="link" class="rounded" alt="img" style="max-height:90%;max-width:90%">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
        name: 'PhotoDetails',
        props: {
            link: {
                type: String,
                required: true
            },
            name: {
                type: String,
                required: true
            }
        },
        methods: {
            hideOverlay() {
                this.$emit('close-overlay');
            }
        },
        computed: {
            getTimestamp() {
                let timestamp=this.link.match(/\d{8}_\d{6}/)[0];
                return timestamp.substring(0,4)+"/"+timestamp.substring(4,6)+"/"+timestamp.substring(6,8)+"("+timestamp.substring(9,11)+":"+timestamp.substring(11,13)+")";
            },
            getPrompt() {
                return JSON.parse(localStorage.getItem(this.name.split("/").pop())).prompt;
            }
        }
};
</script>

<style scoped>
    .custom-gradient {
        background: linear-gradient(to right, #FF33CC, #0066CC);
    }
    .overlay-component {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5); 
        z-index: 9999; 
        display: flex;
        justify-content: center; 
        align-items: center; 
    }

    .overlay-content {
        width: 75%;
        height:75%;
        background-color: #fff; 
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    }
    .color1 {
        background-color: #25262B
    }
    .text-white{
        color:white
    }
    .color2 {
        background-color: #1A1B1E
    }
    .rounded-left {
        border-top-left-radius: 20px;
        border-bottom-left-radius: 20px;
    }
    .rounded-right {
        border-top-right-radius: 20px; 
        border-bottom-right-radius: 20px; 
    }
    .separator {
        border-left: 1px solid #dee2e6;
        height: 100%;
    }
    .border-right {
        border-right: 1px solid #dee2e6; /* Bootstrap's border color */
    }
    .center-btn {
        display: flex;
        justify-content: center;
        align-items: center;
        vertical-align: middle;
    }
    .dl-button {
        height: max-content;
        width: max-content;
        color: white;
        border: none;
        cursor: pointer;
        font-size: 8vw;
        border-radius: 5px;
        vertical-align: middle;
        line-height: 1.5;
    }

        .dl-button:hover {
            background-color: darkred;
        }
    @media (max-width: 768px) {
        .dl-button {
            display: none
        }
        .rounded-left{
            display:none
        }
        .rounded-right {
            width: 100%;
            border-top-left-radius: 20px;
            border-bottom-left-radius: 20px;
        }
    }
</style>