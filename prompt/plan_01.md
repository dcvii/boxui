Here’s your expanded Claude prompt that includes Cypress for full end-to-end (E2E) testing, in addition to all previous requirements (Wagtail backend, Vue frontend, mouseover comment UI, and karma system):

⸻

✅ Expanded Prompt for Claude (with Cypress)

You’re acting as a senior Django/Wagtail and Vue developer. I want you to create a minimal Wagtail CMS app that supports the following:

⸻

1. Blog Article Pages (ArticlePage)
	•	Built using Wagtail’s Page model
	•	Should include a body field (RichTextField)
	•	Must support full-page rendering with comment components embedded

2. Comments
	•	Each comment is tied to a specific ArticlePage
	•	Each comment includes:
	•	User (author)
	•	Text
	•	Timestamp
	•	Karma score (initially 0)
	•	Model name: Comment

3. Karma System
	•	Use a model CommentInteraction with:
	•	ForeignKey to Comment
	•	ForeignKey to User
	•	A reaction field (integer: +1 for upvote, -1 for downvote)
	•	Enforce one vote per user per comment (unique_together)
	•	Backend logic to recalculate and store the current karma score for each comment

4. Frontend UI (Vue + TypeScript)
	•	Use Vue 3 with TypeScript
	•	Use Vite as the build system
	•	Create a reusable Vue component (e.g., KarmaPopover.vue) that:
	•	Is triggered on mouseover of a comment
	•	Displays buttons for 👍 Upvote, 👎 Downvote
	•	Sends interaction to backend via fetch() or Axios
	•	Updates displayed karma count
	•	Comments in the Django template should render with data-comment-id to allow Vue component to hook in

5. API Endpoint
	•	Create an API route (Django view or DRF) to handle POST requests:
	•	Accepts: user_id, comment_id, and reaction
	•	Updates or creates a CommentInteraction
	•	Returns updated karma value

6. Testing Stack
	•	Use Cypress for end-to-end testing
	•	Create E2E tests that simulate viewing an article, hovering over a comment, upvoting/downvoting, and seeing updated karma
	•	Simulate a logged-in user for these tests
	•	Also include:
	•	Django unit tests (models and views)
	•	Optional: pytest with pytest-django for additional test coverage

7. Mac Dev Environment
	•	Set up to run locally on a single Mac workstation
	•	Use:
	•	Python 3.12+
	•	SQLite for the database
	•	venv, poetry, or uv (whichever best fits with Django + Wagtail)
	•	Node.js 20+ for frontend
	•	Provide:
	•	Install and run instructions in a README.md
	•	Cypress test runner setup (cypress.config.ts)
	•	Example Cypress test (karma_spec.cy.ts)

8. Project Structure

wagtail_karma_blog/
├── home/                # Wagtail starter app
├── comments/            # Django app for Comment + Interaction models
├── frontend/            # Vite + Vue project
│   ├── KarmaPopover.vue
│   └── main.ts
├── cypress/
│   ├── e2e/
│   │   └── karma_spec.cy.ts
├── templates/
│   └── article_page.html
└── README.md

Please generate:
	•	Django model, view, and API code
	•	Wagtail page model
	•	Vue 3 + TypeScript component(s)
	•	API interaction logic
	•	Cypress test setup + one test
	•	All relevant package.json, vite.config.ts, and requirements.txt
	•	README with setup instructions for both backend and frontend
	•	Bonus if you scaffold Docker support or .env management
