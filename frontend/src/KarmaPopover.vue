<template>
  <div 
    class="karma-popover"
    :class="{ 'visible': isVisible }"
    :style="{ left: position.x + 'px', top: position.y + 'px' }"
  >
    <div class="karma-buttons">
      <button 
        class="karma-btn upvote"
        :class="{ 'active': userReaction === 1 }"
        @click="handleVote(1)"
        :disabled="loading"
      >
        👍 {{ upvotes }}
      </button>
      <button 
        class="karma-btn downvote"
        :class="{ 'active': userReaction === -1 }"
        @click="handleVote(-1)"
        :disabled="loading"
      >
        👎 {{ downvotes }}
      </button>
    </div>
    <div class="karma-score">
      Total Karma: {{ karmaScore }}
    </div>
    <div v-if="loading" class="loading">Updating...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  commentId: number
  isVisible: boolean
  position: { x: number; y: number }
  karmaScore: number
  userReaction: number | null
}

interface Emits {
  (e: 'vote', commentId: number, reaction: number): void
  (e: 'close'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const loading = ref(false)

const upvotes = computed(() => {
  // This is a simplified calculation - in reality you'd want to track actual vote counts
  return Math.max(0, Math.ceil(props.karmaScore / 2))
})

const downvotes = computed(() => {
  return Math.max(0, Math.abs(Math.floor(props.karmaScore / 2)))
})

const handleVote = async (reaction: number) => {
  if (loading.value) return
  
  loading.value = true
  try {
    emit('vote', props.commentId, reaction)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.karma-popover {
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  opacity: 0;
  transform: translateY(-10px);
  transition: all 0.2s ease;
  pointer-events: none;
  min-width: 200px;
}

.karma-popover.visible {
  opacity: 1;
  transform: translateY(0);
  pointer-events: all;
}

.karma-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.karma-btn {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.karma-btn:hover {
  background: #f5f5f5;
}

.karma-btn.active.upvote {
  background: #28a745;
  color: white;
  border-color: #28a745;
}

.karma-btn.active.downvote {
  background: #dc3545;
  color: white;
  border-color: #dc3545;
}

.karma-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.karma-score {
  text-align: center;
  font-weight: bold;
  color: #333;
  font-size: 14px;
}

.loading {
  text-align: center;
  color: #666;
  font-size: 12px;
  margin-top: 5px;
}
</style>

