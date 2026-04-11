import { defineConfig } from 'cypress';
import path from 'node:path';

export default defineConfig({
  video: false,
  screenshotOnRunFailure: true,
  e2e: {
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: false,
    baseUrl: process.env.E2E_BASE_URL || undefined,
    setupNodeEvents(on, config) {
      const projectRoot = config.projectRoot || process.cwd();
      const indexPath = path.resolve(projectRoot, 'index.html');
      config.env = {
        ...(config.env || {}),
        E2E_FILE_URL: new URL(`file://${indexPath}`).toString()
      };
      return config;
    }
  }
});
