export default {
  framework: {
    name: '@storybook/html-vite',
    options: {}
  },
  stories: ['../stories/**/*.stories.@(js|jsx|ts|tsx)'],
  addons: ['@storybook/addon-essentials'],
  core: { disableTelemetry: true }
};

