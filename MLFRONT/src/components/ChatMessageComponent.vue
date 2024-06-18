<template>
    <div v-if="is_user" class="custom-gradient p-3 rounded-start-4 rounded-top-4 ms-5">
        {{ message }}
    </div>
    <div v-if="!is_user" class="bg-info p-3 rounded-end-4 rounded-top-4 me-5 custom-reversed-gradient">
        <div class="animated-dots-container">
            <div v-if="!message" class="animated-dots">{{ dots }}</div>
            <div v-else class="display-text">{{ message }}</div>
        </div>
    </div>
</template>

<script>
    export default {
      name: 'ChatMessageComponent',
      props: {
        message: String,
        is_user: Boolean,
      },
      data() {
        return {
          dots: 'Ooo',
          intervalId: null
        };
      },
        watch: {
        message(newVal) {
          if (newVal) {
            clearInterval(this.intervalId);
          } else {
            this.startAnimation();
          }
        }
      },
      methods: {
        startAnimation() {
          const dotSequences = ['Ooo', 'oOo', 'ooO'];
          let currentIndex = 0;
          this.intervalId = setInterval(() => {
            this.dots = dotSequences[currentIndex];
            currentIndex = (currentIndex + 1) % dotSequences.length;
          }, 500);
        }
      },
      mounted() {
        this.startAnimation();
      },
      beforeUnmount() {
        clearInterval(this.intervalId);
      }
    }

</script>

<style>
    .custom-gradient {
        background: linear-gradient(to right, #FF33CC, #0066CC);
    }
    .custom-reversed-gradient {
        background: linear-gradient(to right, #0066CC, #FF33CC);
    }
    .animated-dots-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .animated-dots {
        animation: fade 1.5s infinite;
    }

    @keyframes fade {
        0%, 100% {
            opacity: 1;
        }

        50% {
            opacity: 0.5;
        }
    }

    .display-text {
        animation: fadeIn 1s;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }

        to {
            opacity: 1;
        }
    }
</style>