describe('R8 - Todo list manipulation', () => {
  let uid
  let name
  let email
  let taskTitle


  before(function () {
    cy.fixture('user.json')
        .then((user) => {
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/users/create',
            form: true,
            body: user
        }).then((response) => {
            uid = response.body._id.$oid
            name = user.firstName + ' ' + user.lastName
            email = user.email
        })
        })
    })


  beforeEach(function () {
    cy.viewport(1400, 1000)
    cy.visit('http://localhost:3000')

//Logging in (using the email from above)
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)
    //subbmitting the email
    cy.get('form').submit()


    //checks to see if its the right name for the user
    cy.get('h1')
      .should('contain.text', 'Your tasks, ' + name)


    //Make a task before each tests
    cy.fixture('task.json').then((task) => {
        taskTitle = task.title + ' ' + Date.now()
        cy.get('input').eq(0).type(taskTitle)
        cy.get('input').eq(1).type(task.url)
        cy.contains('Create').click()


    //Pressing the task that gets made
    cy.contains(taskTitle)
        .should('be.visible')
        .click()
    })


  })


  //The first test (creating a todo)
  it('R8UC1: Create a new todo item', () => {
    cy.fixture('task.json').then((task) => {
    cy.get('.inline-form input[type="text"]')
      .type(task.todos)


    cy.get('input[value="Add"]')
        .click()

    cy.contains(task.todos)
        .should('exist')

    cy.get('.todo-item')
        .last()
        .should('contain', task.todos)
    })
 })




  //The alternative test case
  //2.b If the description is empty then the “Add” button should remain disabled.
  it('R8UC1 alternative 2: Add button is disabled for empty input description ', () => {
    cy.get('.inline-form')
        .find('input[placeholder="Add a new todo item"]')
        .should('have.value', '')


    cy.get('.inline-form')
        .find('input[type="submit"]')
        .should('be.disabled')
  })


// Over to: R8UC2

  //Checks the todo list, and makes it "watched"
  it('R8UC2: The user "completes" a todo', () => {
    cy.get('.todo-item')
      .first()
      .find('.checker.unchecked')
      .click()

    // Find todo-item and check if its checked.
    cy.get('.todo-item')
      .first()
      .find('.checker.checked')
      .should('exist')
    
    //Then see if the task text struck through as stated in end-condition.
    cy.get('.todo-item')
      .first()
      .find('.editable')
      .should('have.css', 'text-decoration-line', 'line-through')
  })


  //The alternative test case
  //2.b If the todo item was previously done, it is set to active. The toggled todo item is not struck through anymore.


  it('R8UC2 alternative 2: The user "completes" a todo', () => {
    // First clikc on the item to make it "checked".
    cy.get('.todo-item')
        .first()
        .find('.checker.unchecked')
        .click()

    // Find the checked item (the one that we used clicked) and click it back to normal.
    cy.get('.todo-item')
        .first()
        .find('.checker.checked')
        .click()

    // Now see if its backed to unchecked.
    cy.get('.todo-item')
        .first()
        .find('.checker.unchecked')
        .should('exist')

    // Test if the text is back to normal (not struck).
    cy.get('.todo-item')
        .find('.editable')
        .should('have.css', 'text-decoration-line', 'none')
  })




  //Checks the todo list, and makes it "watched"
  it('R8UC3: Remove a todo', () => {
    cy.get('.todo-item')
        .first()
        .find('.remover')
        .click()
        //(Needed another click since it didnt seem to "register" on the first one sometimes)
        //tried it myself aswell and the first time i tried to delete an item i had to click twice, then it worked with one
        .click()


    //Verify that it got removed
    cy.get('.todo-item')
        .should('have.length', 0)
  })




  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})
