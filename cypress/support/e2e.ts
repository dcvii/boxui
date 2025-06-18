// cypress/support/e2e.ts

// Custom commands for authentication
Cypress.Commands.add('login', (username: string, password: string) => {
  cy.visit('/admin/login/')
  cy.get('input[name="username"]').type(username)
  cy.get('input[name="password"]').type(password)
  cy.get('input[type="submit"]').click()
})

// Custom command to create test data
Cypress.Commands.add('createTestUser', () => {
  cy.request({
    method: 'POST',
    url: '/api/test/create-user/',
    body: {
      username: 'testuser',
      password: 'testpass123',
      email: 'test@example.com'
    }
  })
})

// Declare the custom commands for TypeScript
declare global {
  namespace Cypress {
    interface Chainable {
      login(username: string, password: string): Chainable<void>
      createTestUser(): Chainable<void>
    }
  }
}

