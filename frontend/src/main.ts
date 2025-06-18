import { createApp, ref } from 'vue'
import KarmaPopover from './KarmaPopover.vue'

interface CommentData {
  id: number
  karmaScore: number
  userReaction: number | null
}

// Create a simple karma management system
class KarmaManager {
  private popoverVisible = ref(false)
  private currentCommentId = ref<number | null>(null)
  private popoverPosition = ref({ x: 0, y: 0 })
  private comments = ref<Map<number, CommentData>>(new Map())

  constructor() {
    this.initializeComments()
    this.setupEventListeners()
  }

  private initializeComments() {
    // Find all karma displays and initialize comment data
    const karmaDisplays = document.querySelectorAll('.karma-display')
    karmaDisplays.forEach((element) => {
      const commentId = parseInt(element.getAttribute('data-comment-id') || '0')
      const karmaScore = parseInt(element.getAttribute('data-karma-score') || '0')
      
      this.comments.value.set(commentId, {
        id: commentId,
        karmaScore,
        userReaction: null
      })
      
      // Load current user reaction
      this.loadUserReaction(commentId)
    })
  }

  private async loadUserReaction(commentId: number) {
    try {
      const response = await fetch(`/api/karma/${commentId}/`)
      if (response.ok) {
        const data = await response.json()
        const comment = this.comments.value.get(commentId)
        if (comment) {
          comment.userReaction = data.user_reaction
          comment.karmaScore = data.karma_score
        }
      }
    } catch (error) {
      console.error('Failed to load user reaction:', error)
    }
  }

  private setupEventListeners() {
    document.addEventListener('mouseover', (event) => {
      const target = event.target as HTMLElement
      if (target.classList.contains('karma-display')) {
        const commentId = parseInt(target.getAttribute('data-comment-id') || '0')
        this.showPopover(commentId, event)
      }
    })

    document.addEventListener('mouseout', (event) => {
      const target = event.target as HTMLElement
      if (target.classList.contains('karma-display')) {
        // Add a small delay before hiding to allow moving to popover
        setTimeout(() => {
          if (!this.isMouseOverPopover()) {
            this.hidePopover()
          }
        }, 200)
      }
    })

    // Hide popover when clicking outside
    document.addEventListener('click', (event) => {
      const target = event.target as HTMLElement
      if (!target.closest('.karma-popover') && !target.classList.contains('karma-display')) {
        this.hidePopover()
      }
    })
  }

  private isMouseOverPopover(): boolean {
    // Simple check - in a real implementation you'd want more sophisticated hover detection
    return document.querySelector('.karma-popover:hover') !== null
  }

  private showPopover(commentId: number, event: MouseEvent) {
    const rect = (event.target as HTMLElement).getBoundingClientRect()
    this.popoverPosition.value = {
      x: rect.left,
      y: rect.bottom + 5
    }
    this.currentCommentId.value = commentId
    this.popoverVisible.value = true
  }

  private hidePopover() {
    this.popoverVisible.value = false
    this.currentCommentId.value = null
  }

  async handleVote(commentId: number, reaction: number) {
    try {
      const response = await fetch('/api/karma/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken(),
        },
        body: JSON.stringify({
          comment_id: commentId,
          reaction: reaction
        })
      })

      if (response.ok) {
        const data = await response.json()
        
        // Update comment data
        const comment = this.comments.value.get(commentId)
        if (comment) {
          comment.karmaScore = data.karma_score
          comment.userReaction = data.user_reaction
        }

        // Update display in DOM
        this.updateKarmaDisplay(commentId, data.karma_score)
        
      } else {
        const errorData = await response.json()
        console.error('Vote failed:', errorData)
        alert('Failed to vote. Please make sure you are logged in.')
      }
    } catch (error) {
      console.error('Network error:', error)
      alert('Network error. Please try again.')
    }
  }

  private updateKarmaDisplay(commentId: number, newScore: number) {
    const display = document.querySelector(`[data-comment-id="${commentId}"]`)
    if (display) {
      display.textContent = `Karma: ${newScore}`
      display.setAttribute('data-karma-score', newScore.toString())
    }
  }

  private getCSRFToken(): string {
    const cookie = document.cookie
      .split(';')
      .find(c => c.trim().startsWith('csrftoken='))
    return cookie ? cookie.split('=')[1] : ''
  }

  // Getters for Vue component
  get isVisible() { return this.popoverVisible }
  get commentId() { return this.currentCommentId }
  get position() { return this.popoverPosition }
  get currentComment() {
    const id = this.currentCommentId.value
    return id ? this.comments.value.get(id) : null
  }
}

// Initialize the karma system
const karmaManager = new KarmaManager()

// Create and mount Vue app for the popover
const app = createApp({
  components: {
    KarmaPopover
  },
  setup() {
    return {
      isVisible: karmaManager.isVisible,
      commentId: karmaManager.commentId,
      position: karmaManager.position,
      currentComment: karmaManager.currentComment,
      handleVote: karmaManager.handleVote.bind(karmaManager)
    }
  },
  template: `
    <KarmaPopover
      v-if="currentComment"
      :comment-id="currentComment.id"
      :is-visible="isVisible"
      :position="position"
      :karma-score="currentComment.karmaScore"
      :user-reaction="currentComment.userReaction"
      @vote="handleVote"
    />
  `
})

app.mount('#karma-app')

