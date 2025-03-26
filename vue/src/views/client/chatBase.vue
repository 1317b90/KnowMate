<template>
    <t-chat ref="chatRef" :clear-history="chatList.length > 0 && !isStreamLoad" @clear="clearConfirm">
        <template v-for="(item, index) in chatList" :key="index">
            <t-chat-item v-if="!item.isHide" :avatar="item.avatar" :name="item.name" :role="item.role"
                :datetime="item.datetime" variant="base" :content="item.content" text>
                <template v-if="!isStreamLoad || item.role == 'error'" #actions>
                    <t-chat-action :is-good="isGood" :is-bad="isBad" :content="item.content"
                        @operation="(type, { e }) => handleOperation(type, { e, index })" />
                </template>
            </t-chat-item>
        </template>
        <template #footer>
            <t-chat-input :stop-disabled="isStreamLoad" @send="inputEnter" @stop="onStop"> </t-chat-input>
        </template>
    </t-chat>
</template>
<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import {
    Chat as TChat,
    ChatAction as TChatAction,
    ChatContent as TChatContent,
    ChatInput as TChatInput,
    ChatItem as TChatItem,
} from '@tdesign-vue-next/chat';
import { streamChat } from '@/request/api';
import { baseUrl } from '@/request';
import type { chatItemI } from '@/interfaces';
const propsData = defineProps(['question'])

const controller = ref<AbortController | null>(null);
const loading = ref(false);
const isStreamLoad = ref(false);
const isGood = ref(false);
const isBad = ref(false);
const chatRef = ref(null);

// 聊天记录
const chatList = ref<any[]>([]);

// 从本地存储加载聊天记录
onMounted(() => {
    const savedChat = localStorage.getItem('chatHistory');
    if (savedChat) {
        chatList.value = JSON.parse(savedChat);
    } else {
        chatList.value = [
            {
                content: `快来和小知玩呀~`,
                role: 'model-change',
            }
        ];
    }

    // 如果有传入的问题，自动输入并发送
    if (propsData.question) {
        inputEnter(propsData.question);
    }
});

// 保存聊天记录到本地存储
const saveChatHistory = () => {
    localStorage.setItem('chatHistory', JSON.stringify(chatList.value));
};

// 滚动到底部
const backBottom = () => {
    if (chatRef.value) {
        chatRef.value.scrollToBottom({
            behavior: 'smooth',
        });
    }
};

// 清空聊天记录
const clearConfirm = function () {
    chatList.value = [];
    localStorage.removeItem('chatHistory');
};

// 中断请求
const onStop = function () {
    if (controller.value) {
        controller.value.abort();
        controller.value = null;
        loading.value = false;
        isStreamLoad.value = false;
    }
};
// 处理反馈操作
const handleOperation = function (type: 'good' | 'bad' | 'replay', options: { e?: Event; index: number }) {
    console.log('handleOperation', type, options);
    const { index } = options;
    if (type === 'good') {
        isGood.value = !isGood.value;
        isBad.value = false;
    } else if (type === 'bad') {
        isBad.value = !isBad.value;
        isGood.value = false;
    } else if (type === 'replay') {
        // 直接重置当前AI回复的内容
        chatList.value[index].content = '';
        isStreamLoad.value = true;
        handleData(index);
    }
};

// 处理用户输入
const inputEnter = function (inputValue: string) {
    if (isStreamLoad.value) {
        return;
    }
    if (!inputValue) return;
    const params = {
        avatar: baseUrl + 'images/web/aj.jpg',
        name: '自己',
        datetime: new Date().toLocaleString(),
        content: inputValue,
        role: 'user',
        isHide: inputValue === propsData.question
    };
    chatList.value.unshift(params);
    // 空消息占位
    const params2 = {
        avatar: baseUrl + 'images/web/rd.jpg',
        name: '小知',
        datetime: new Date().toLocaleString(),
        content: ' ',
        role: 'assistant',
    };
    chatList.value.unshift(params2);
    saveChatHistory();
    handleData();
    backBottom();
};

// 处理聊天请求和响应
const handleData = async (replayIndex = 0) => {
    loading.value = true;
    isStreamLoad.value = true;
    const lastItem = replayIndex !== undefined ? chatList.value[replayIndex] : chatList.value[0];

    // 准备聊天历史记录
    const messages: chatItemI[] = [];
    for (let i = chatList.value.length - 1; i >= 0; i--) {
        const item = chatList.value[i];
        if (item.role === 'user' || item.role === 'assistant') {
            if (replayIndex !== undefined && i <= replayIndex && item.role === 'assistant' && item.content === '') {
                // 跳过当前正在重新生成的空回复
                continue;
            }
            messages.push({
                role: item.role,
                content: item.content
            });
        }
    }

    controller.value = new AbortController();

    try {
        for await (const chunk of streamChat(messages, controller.value.signal)) {
            if (chunk) {
                lastItem.content += chunk;
                chatList.value = [...chatList.value];
                await nextTick();
                backBottom();
            }
        }
    } catch (error: any) {
        if (error.name !== 'AbortError') {
            console.error('流式聊天错误:', error);
            lastItem.role = 'error';
            lastItem.content = '发生错误，请重试';
        }
    } finally {
        isStreamLoad.value = false;
        loading.value = false;
        saveChatHistory();
        controller.value = null;
    }
};
</script>
<style scoped></style>
