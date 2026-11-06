# Test Your App

A Multi-Framework app is a standard React or Angular project, so you test it with your framework's usual tools. Each project template comes preconfigured for both unit tests and end-to-end tests, so you can verify your app locally and in your pipeline before you deploy it to an org.

This topic applies to both React and Angular apps. Run the commands from your UIBundle directory (`<source>/uiBundles/<appName>/`), where your app's `package.json` and test configuration live.

## Run Unit Tests

Each template includes a `test` script. From your UIBundle directory, run:

```bash
npm run test
```

- **React** apps use [Vitest](https://vitest.dev/) with [Testing Library](https://testing-library.com/docs/react-testing-library/intro/) and a jsdom environment. The template configures this in `vitest.config.ts` and `vitest.setup.ts`. Put a test file next to the component it covers, such as `MyComponent.test.tsx`. `npm run test` starts Vitest in watch mode and reruns tests as you edit. For a single pass, such as in CI, run `npm run test -- run`.
- **Angular** apps use `ng test`, which runs Angular's built-in unit test runner against your `*.spec.ts` files.

## Run End-to-End Tests

Each template includes [Playwright](https://playwright.dev/) for browser-based end-to-end tests, with a `playwright.config.ts` file and an `e2e` directory that holds a sample `app.spec.ts`. The Playwright configuration starts a local static server that serves your compiled app and runs the tests against it, so the tests don't need a connection to a Salesforce org.

Build your app for end-to-end testing first. This command builds your production assets and rewrites their paths so that Playwright can serve them:

```bash
npm run build:e2e
```

Then run the tests:

- **React**: `npx playwright test`
- **Angular**: `npm run e2e`

## Test Before You Deploy

Run your unit and end-to-end tests as part of your build, before you deploy the UIBundle to an org. Because the app is source-format metadata in your Salesforce DX project, you can run these tests as a step in the same CI/CD pipeline that deploys your app. See [Deploy and Publish a UIBundle](/docs/platform/multiframework/guide/mfw-deploy.md).

## See Also

- [Preview and Run Your App Locally](/docs/platform/multiframework/guide/mfw-preview.md)
- [Deploy and Publish a UIBundle](/docs/platform/multiframework/guide/mfw-deploy.md)
