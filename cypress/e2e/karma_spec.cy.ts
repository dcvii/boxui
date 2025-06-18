describe('Karma System E2E Tests', () => {
  beforeEach(() => {
    // Reset database state and create test data
    cy.task('db:seed')
    cy.visit('/')
  })

  it('should display karma popover on comment hover', () => {
    // Navigate to an article with comments
    cy.get('a').contains('Test Article').click()
    
    // Find a comment and hover over its karma display
    cy.get('.karma-display').first().trigger('mouseover')
    
    // Verify popover appears
    cy.get('.karma-popover').should('be.visible')
    cy.get('.karma-btn.upvote').should('be.visible')
    cy.get('.karma-btn.downvote').should('be.visible')
  })

  it('should allow authenticated user to upvote a comment', () => {
    // Login as test user
    cy.login('testuser', 'testpass123')
    
    // Navigate to article
    cy.visit('/articles/test-article/')
    
    // Hover over karma display to show popover
    cy.get('.karma-display').first().trigger('mouseover')
    
    // Get initial karma score
    cy.get('.karma-display').first().invoke('text').then((initialText) => {
      const initialScore = parseInt(initialText.match(/\d+/)?.[0] || '0')
      
      // Click upvote button
      cy.get('.karma-btn.upvote').click()
      
      // Verify karma score increased
      cy.get('.karma-display').first().should('contain', (initialScore + 1).toString())
      
      // Verify button shows as active
      cy.get('.karma-btn.upvote').should('have.class', 'active')
    })
  })

  it('should allow authenticated user to downvote a comment', () => {
    // Login as test user
    cy.login('testuser', 'testpass123')
    
    // Navigate to article
    cy.visit('/articles/test-article/')
    
    // Hover over karma display to show popover
    cy.get('.karma-display').first().trigger('mouseover')
    
    // Get initial karma score
    cy.get('.karma-display').first().invoke('text').then((initialText) => {
      const initialScore = parseInt(initialText.match(/\d+/)?.[0] || '0')
      
      // Click downvote button
      cy.get('.karma-btn.downvote').click()
      
      // Verify karma score decreased
      cy.get('.karma-display').first().should('contain', (initialScore - 1).toString())
      
      // Verify button shows as active
      cy.get('.karma-btn.downvote').should('have.class', 'active')
    })
  })

  it('should toggle vote when clicking same button twice', () => {
    // Login as test user
    cy.login('testuser', 'testpass123')
    
    // Navigate to article
    cy.visit('/articles/test-article/')
    
    // Hover over karma display to show popover
    cy.get('.karma-display').first().trigger('mouseover')
    
    // Get initial karma score
    cy.get('.karma-display').first().invoke('text').then((initialText) => {
      const initialScore = parseInt(initialText.match(/\d+/)?.[0] || '0')
      
      // Click upvote button
      cy.get('.karma-btn.upvote').click()
      
      // Verify score increased
      cy.get('.karma-display').first().should('contain', (initialScore + 1).toString())
      
      // Click upvote again to toggle off
      cy.get('.karma-btn.upvote').click()
      
      // Verify score returned to initial value
      cy.get('.karma-display').first().should('contain', initialScore.toString())
      
      // Verify button is no longer active
      cy.get('.karma-btn.upvote').should('not.have.class', 'active')
    })
  })

  it('should prevent multiple votes per user per comment', () => {
    // Login as test user
    cy.login('testuser', 'testpass123')
    
    // Navigate to article
    cy.visit('/articles/test-article/')
    
    // Hover over karma display to show popover
    cy.get('.karma-display').first().trigger('mouseover')
    
    // Click upvote
    cy.get('.karma-btn.upvote').click()
    
    // Verify upvote is active
    cy.get('.karma-btn.upvote').should('have.class', 'active')
    
    // Click downvote (should change from upvote to downvote)
    cy.get('.karma-btn.downvote').click()
    
    // Verify downvote is now active and upvote is not
    cy.get('.karma-btn.downvote').should('have.class', 'active')
    cy.get('.karma-btn.upvote').should('not.have.class', 'active')
  })

  it('should require authentication for voting', () => {
    // Visit article without logging in
    cy.visit('/articles/test-article/')
    
    // Hover over karma display to show popover
    cy.get('.karma-display').first().trigger('mouseover')
    
    // Try to click upvote
    cy.get('.karma-btn.upvote').click()
    
    // Should show error message or redirect to login
    cy.on('window:alert', (alertText) => {
      expect(alertText).to.contains('Please make sure you are logged in')
    })
  })

  it('should update karma display in real-time', () => {
    // Login as test user
    cy.login('testuser', 'testpass123')
    
    // Navigate to article
    cy.visit('/articles/test-article/')
    
    // Get comment ID for API testing
    cy.get('.karma-display').first().invoke('attr', 'data-comment-id').then((commentId) => {
      // Hover and vote
      cy.get('.karma-display').first().trigger('mouseover')
      cy.get('.karma-btn.upvote').click()
      
      // Verify the karma display updates immediately
      cy.get('.karma-display').first().should('not.contain', 'Karma: 0')
      
      // Verify the change persists on page reload
      cy.reload()
      cy.get(`[data-comment-id="${commentId}"]`).should('not.contain', 'Karma: 0')
    })
  })
})

