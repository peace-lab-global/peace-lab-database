function visitVisualization() {
  const baseUrl = Cypress.config('baseUrl');
  const fileUrl = Cypress.env('E2E_FILE_URL');

  if (baseUrl) {
    cy.visit('/');
    return;
  }

  cy.visit(fileUrl);
}

function assertSidebarScrollable() {
  cy.get('#sidebar').should($el => {
    expect($el[0].scrollHeight).to.be.greaterThan($el[0].clientHeight);
  });
}

describe('领域框架交互与滚动', () => {
  const viewports = [
    { name: 'Desktop 1920x1080', w: 1920, h: 1080 },
    { name: 'Desktop 1366x768', w: 1366, h: 768 },
    { name: 'Tablet landscape', w: 1024, h: 768 },
    { name: 'Tablet portrait', w: 768, h: 1024 },
    { name: 'Mobile portrait', w: 390, h: 844 },
    { name: 'Mobile landscape', w: 844, h: 390 }
  ];

  viewports.forEach(vp => {
    it(vp.name, () => {
      cy.viewport(vp.w, vp.h);
      visitVisualization();

      if (vp.w <= 760) {
        cy.get('#sidebar-toggle').click();
        cy.get('#sidebar').should('have.class', 'open');
      }

      assertSidebarScrollable();

      cy.get('#sidebar').scrollTo('bottom');
      cy.get('#sidebar').should($el => {
        expect($el[0].scrollTop).to.be.greaterThan(0);
      });

      cy.get('#sidebar').scrollTo('top');
      cy.contains('button.legend-item', '01 智慧传承').focus().click();
      cy.get('#detail-panel').should('have.class', 'open');
      cy.get('#detail-name').should('contain', '智慧传承');

      cy.get('#detail-close').click();
      cy.get('#detail-panel').should('not.have.class', 'open');

      cy.get('#graph-svg circle').first().trigger('pointerenter', { clientX: 200, clientY: 200, bubbles: true });
      cy.get('#tooltip').should('be.visible');
      cy.get('#graph-svg circle').first().trigger('pointerleave', { clientX: 200, clientY: 200, bubbles: true });
      cy.get('#tooltip').should('not.be.visible');
    });
  });
});

