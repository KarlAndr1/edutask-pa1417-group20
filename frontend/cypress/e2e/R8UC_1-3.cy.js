describe("R8UC 1-3, managing tasks", () => {

	let uid, email
	before(() => {
		cy
			.fixture("user.json") // Reuse the user detils that are used for in login.cy.js
			.then(user => {				
				cy.request({ 
					method: "POST", 
					url: "http://localhost:5000/users/create",
					form: true,
					body: user
				}).then(response => {
					uid = response.body._id.$oid
					email = user.email
				})
			})
	})
	
	let todo_desc, task_id
	beforeEach(() => {		
		cy
			.fixture("usertask.json")
			.then(task => {
				todo_desc = task.todos
				task.userid = uid,
				cy.request({
					method: "POST",
					url: "http://localhost:5000/tasks/create",
					form: true,
					body: task
				}).then(response => {
					console.log("TID", response.body)
					task_id = response.body[0]._id.$oid
				})
			})		
		
		cy.visit("http://localhost:3000")
		cy.contains("div", "Email Address").find("input[type=text]").type(email)
		cy.get("form").submit()
		
		cy.get("div .container-element > a").click()
	})
	
	afterEach(() => {
		cy.request({
			method: "DELETE",
			url: `http://localhost:5000/tasks/byid/${task_id}`
		})
	})
	
	after(() => {
			cy.request({ method: "DELETE", url: `http://localhost:5000/users/${uid}`})
	})
	
	describe("R8UC1", () => {
		it("Create to-do with description", () => {
			const desc = "A task description"
			
			//Action
			cy.get(".popup").find("input[type=text]").type(desc)
			cy.get(".popup").find("form").submit()
			
			//Result
			cy.get(".popup").find("li.todo-item").last().contains(desc).should("exist")
		})
		
		it("Create to-do without description; should not be possible (the button should be disabled)", () => {
			cy.get(".popup").find("input[type=submit]").should("have.property", "disabled")
		})
	})
	
	describe("R8UC2", () => {
		it("Mark todo item as complete", () => {
			cy.get(".popup").find("li.todo-item").contains(todo_desc).parent().as("todo-item")
			
			// Action
			cy.get("@todo-item").find(".checker.unchecked").click()
		
			// Result
			cy.get("@todo-item").contains(todo_desc).should("have.css", "text-decoration").should("to.match", /line-through/)
		})
		
		it("Mark todo item as incomplete", () => {
			cy.get(".popup").find("li.todo-item").contains(todo_desc).parent().as("todo-item")
			
			//Setup
			cy.get("@todo-item").find(".checker").click()
			cy.get("@todo-item").find(".checker.checked") // Wait for it to update, to enforce consitency
			
			// Action
			cy.get("@todo-item").find(".checker").click()
			
			//Result
			// https://stackoverflow.com/questions/70740557/cypress-check-color-of-css-background
			cy.get("@todo-item").contains(todo_desc).invoke("css", "text-decoration").should("not.to.match", /line-through/)
		})
	})
	
	describe("R8UC3", () => {
		it("Delete todo item", () => {
			cy.get(".popup").find("li.todo-item").find(".remover").click()
			cy.get(".popup").find("li.todo-item").should("not.exist")
		})
	})
})
