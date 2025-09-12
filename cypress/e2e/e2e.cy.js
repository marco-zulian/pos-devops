describe('Flask Application E2E Test', () => {
  it('should load the main page and display content correctly', () => {
    cy.visit('/');

    cy.contains('h1', 'Funciona!').should('be.visible');

    cy.get('body').then(($body) => {
      if ($body.find('h2').length > 0) {
        cy.get('h2').first().should('be.visible');
        cy.log('User data found and displayed.');
      } else {
        cy.log('No user data found, which is an expected state for an empty DB.');
      }
    });
  });
});