describe('Calendar app', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173')
  })
  it('displays the calendar by default', () => {
    cy.get('grid grid-cols-8 border-t border-l border-gray-800')
  })
})