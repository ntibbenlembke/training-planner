import React from 'react'
import GeneratePlan from './GeneratePlan'

describe('<GeneratePlan />', () => {
  it('renders', () => {
    // see: https://on.cypress.io/mounting-react
    cy.mount(<GeneratePlan />)
  })
})