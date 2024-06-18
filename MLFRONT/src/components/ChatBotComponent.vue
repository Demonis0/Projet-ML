<template>
  <div class="d-flex flex-column" style="height:100%">
    <div class="card-header border-bottom">Chat</div>
    <div class="overflow-auto" style="height:100%" ref="messagesContainer">
        <ul class="chat-list list-unstyled">
            <li v-for="(message, index) in messages" :key="message.id || index" class="m-3">
               <ChatMessageComponent :message="message.message" :is_user="message.is_user"/>
            </li>
        </ul>
    </div>
    <div class="input-group mb-2">
      <input type="text" class="form-control" placeholder="Message" aria-label="Message" aria-describedby="basic-addon2" v-model="newMessage" @keyup.enter="sendMessage" ref="sendInput">
      <div class="input-group-append">
        <button class="btn btn-outline-secondary send-btn" type="button" @click="sendMessage" ref="sendBtn">📩</button>
      </div>
    </div>
  </div>
</template>
<script>

import ChatMessageComponent from './ChatMessageComponent.vue';

export default {
  name: 'ChatBotComponent',
  components: {ChatMessageComponent},
  data() {
    return {
      loadingText: '',
      newMessage: '',
      messages: [
      ],
    };
  },

  computed: {
    getTimestamp() {
      let timestamp=this.link.match(/\d{8}_\d{6}/)[0];
      return timestamp.substring(0,4)+"/"+timestamp.substring(4,6)+"/"+timestamp.substring(6,8)+"("+timestamp.substring(9,11)+":"+timestamp.substring(11,13)+")";
    },
  },
  methods: {
    async sendPostRequest(url, data) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: data }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            // wait the response
            const responseData = await response.json();
            console.log(responseData);
            if(responseData.status==="success"){

                

                this.setprompt(responseData.filename,this.newMessage);

                console.log("TRUE")

                return true;
            } else {
                return false;
            }
        } catch (error) {
            console.error('Error:', error);
            return false;
        }
    },
    setprompt(imageName,p) {
      localStorage.setItem(imageName, JSON.stringify({ prompt: p}));

      return 0;
    },
    async sendMessage() {
        const sendBtn = this.$refs.sendBtn;
        const sendInput = this.$refs.sendInput;
      if (this.newMessage.trim() !== '') {
        this.messages.push({ message: this.newMessage, is_user: true });
        this.messages.push({ message: null, is_user: false });
        sendBtn.disabled = true;
        sendInput.disabled = true;
        this.scrollToBottom();
        // Simulate a bot response
        if(await this.sendPostRequest("http://localhost:5000/txttoimg",this.newMessage)==true){
          const lastMessageIndex = this.messages.length - 1;
          this.messages[lastMessageIndex].message = 'I generated you image! it\'s in the list here -->';
          this.newMessage = '';
          sendBtn.disabled = false;
          sendInput.disabled = false;
          this.scrollToBottom();
        } else {
          const lastMessageIndex = this.messages.length - 1;
          this.messages[lastMessageIndex].message = 'I couldn\'tgenerate your image check your network/request';
          sendBtn.disabled = false;
          sendInput.disabled = false;
          this.newMessage = '';
          this.scrollToBottom();
        }
      }
    },
    scrollToBottom() {
      if (this.messages.lenght > 7) {
        this.$nextTick(() => {
          const messagesContainer = this.$refs.messagesContainer;
          messagesContainer.scrollTop = messagesContainer.scrollHeight;
        });
      }
    }
  }
}

</script>

<style scoped>
.send-btn {
  border-top-left-radius: 0px;
  border-bottom-left-radius: 0px;
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
}
body{
  background:#eee;
}
.chat-list {
  padding: 0;
  font-size: .8rem;
}

.chat-list li {
  margin-bottom: 10px;
  color: #ffffff;
}

.card-header:first-child {
  -webkit-border-radius: 0.3rem 0.3rem 0 0;
  -moz-border-radius: 0.3rem 0.3rem 0 0;
  border-radius: 0.3rem 0.3rem 0 0;
}
.card-header {
  border: 0;
  font-size: 1rem;
  padding: .65rem 1rem;
  font-weight: 600;
  color: #ffffff;
}
</style>