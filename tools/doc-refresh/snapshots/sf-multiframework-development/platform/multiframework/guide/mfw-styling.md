# Style Your Apps

React apps don't currently support Lightning base components and `lightning/*` modules, so they don't provide built-in Salesforce Lightning Design System (SLDS) styling. With React apps, there are several ways to match the Salesforce look-and-feel.

- Apply SLDS blueprints
- Import SLDS for React from @salesforce/design-system-react

Alternatively, use [shadcn](https://ui.shadcn.com/) to create building blocks that you can customize via Tailwind CSS based on your requirements.

:::tip
The styling examples in the [Multi-framework recipes repo](https://github.com/trailheadapps/multiframework-recipes) demonstrate how to use SLDS blueprints, SLDS for React, and shadcn components.
:::

## Apply SLDS Blueprints

To create UI components that match the Salesforce look-and-feel, use the SLDS blueprint for the component. For example, if you're creating a button, apply the [SLDS button blueprint](https://v1.lightningdesignsystem.com/components/buttons/) in your app. Unlike [Lightning base components](https://developer.salesforce.com/docs/platform/lightning-component-reference/guide/), you control the markup for your UI components but don't get the latest SLDS updates automatically.

```typescript
<section>
  <div className="flex flex-wrap gap-2">
    <button className="slds-button slds-button_neutral">Neutral</button>
    <button className="slds-button slds-button_brand">Brand</button>
  </div>
</section>
```

## Import SLDS for React

To apply SLDS styling to your UI components automatically, import SLDS for React in your app.

```typescript
import { Button } from "@salesforce/design-system-react";
export default function ButtonDSR() {
  return (
    <section>
      <h3 className="slds-text-heading_small slds-m-bottom_small">Disabled</h3>
      <div className="flex flex-wrap gap-2">
        <Button label="Neutral" variant="neutral" />
        <Button label="Brand" variant="brand" />
      </div>
    </section>
  );
}
```

SLDS for React comes with icons that you get via the `lightning-icon` LWC component. With shadcn, wrap your icon using `IconSettings` to configure the sprite base path.

```typescript
import { Icon, IconSettings } from "@salesforce/design-system-react";
export default function MyReactIcon() {
  return (
    <IconSettings iconPath="/assets/icons">
      <Icon assistiveText={{ label: name }} category="utility" name="edit" size="small" />
    </IconSettings>
  );
}
```

## Use shadcn Components

In LWC, styles are implemented in the base components and you apply SLDS design tokens to customize the styling. In a React app with shadcn, styling is applied globally. When you install a shadcn component, the source code is added to your project. You can then change the Tailwind classes directly in that file to alter the branding globally. For example, you can install the shadcn Button and Card components like this.

```javascript
import React from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
```

A React app uses a global CSS file to define styles that apply across the entire app. Use a `global.css` file as your design system entry point where you can define tokens and map them into Tailwind utilities. With this pattern, you can swap token values to rebrand without rewriting components.

### Import Tailwind and any shared styles

To create your global file, start with the Tailwind import and apply base defaults using `@layer`. Use `@layer base` to set app-wide defaults, such as for `min-h-screen, antialiasing, default borders, focus outlines, base bg/text`.

```css
/* global.css */
@import "tailwindcss";
@layer base {
  html,
  body,
  #root {
    @apply min-h-screen;
  }

  body {
    @apply antialiased bg-white;
  }
}
@import "tw-animate-css";
@import "shadcn/tailwind.css";
```

### Define semantic design tokens in :root

Brand your app by overriding tokens. The global CSS file is where you can define the app-level tokens. For example, you can add a `.dark` block for dark-mode token overrides, which cascades automatically.

```css
:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --border: oklch(0.922 0 0);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
}
```

### Map tokens into Tailwind theme variables

Use `@theme` inline to map semantic tokens to utility-facing names, such as `--color-primary` and `--color-background`. This lets you write classes like `bg-background`, `text-foreground`, `border-border` in components. For more information, see the [shadcn theming documentation](https://ui.shadcn.com/docs/theming).

```css
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
}
```

:::tip
The `global.css` example in the [Multi-framework recipes repo](https://github.com/trailheadapps/multiframework-recipes) demonstrates how to configure Tailwind CSS with custom theme variables by using CSS custom properties.
:::

## Example Conversion

Here's an example of a `lightning-card` component for LWC that we want to convert to a shadcn Card component.

```html
<template>
  <lightning-card title="Account Details" icon-name="standard:account">
    <lightning-button label="Edit" slot="actions"></lightning-button>
    <div class="slds-p-horizontal_small">
      <p>Account Name: Acme Corp</p>
      <p>Industry: Technology</p>
    </div>
    <p slot="footer">Last Updated: March 2026</p>
  </lightning-card>
</template>
```

Converting a `lightning-card` to a shadcn `Card` is a move from a **template-driven** approach to a **composition-driven** approach. In LWC, the structure is defined by slots (title, actions, footer). In React with shadcn, you explicitly render every piece of the card by using sub-components: `Card, CardHeader, CardTitle, CardDescription, CardContent,` and `CardFooter`.

```typescript
// MyComponent.tsx
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Building2 } from "lucide-react"; // Equivalent to standard:account

export default function AccountCard() {
  return (
    <Card className="w-[400px]">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <div className="flex items-center gap-2">
          <Building2 className="h-5 w-5 text-blue-600" />
          <div>
            <CardTitle className="text-lg font-bold">Account Details</CardTitle>
            <CardDescription>Customer Tier: Gold</CardDescription>
          </div>
        </div>
        {/* Replacing slot="actions" */}
        <Button variant="outline" size="sm">
          Edit
        </Button>
      </CardHeader>

      <CardContent>
        <div className="space-y-1">
          <p className="text-sm">Account Name: Acme Corp</p>
          <p className="text-sm">Industry: Technology</p>
        </div>
      </CardContent>

      <CardFooter className="border-t pt-4">
        <p className="text-xs text-muted-foreground">Last Updated: March 2026</p>
      </CardFooter>
    </Card>
  );
}
```

Consider several styling differences between SLDS and shadcn components.

- **Radius:** SLDS 1 uses a small border-radius (4px/0.25rem) for buttons and cards, while SLDS 2 uses a border-radius of 15rem. The default shadcn radius is 0.5rem.
- **The "ring" focus indicator color:** With SLDS, focus states are often the brand blue or similar to `#0176d3` so your shadcn inputs feel native to the Lightning experience.
- **Secondary colors:** SLDS uses light grays (`#f3f3f3`) for secondary backgrounds. shadcn's default `secondary` is often a darker gray. For more information, see the [SLDS Color Overview documentation](https://v1.lightningdesignsystem.com/guidelines/color/overview/).

## Utility Classes

To style your components, use [Tailwind CSS utility classes](https://tailwindcss.com/docs/styling-with-utility-classes). For example, you can use the [flexbox and grid](https://tailwindcss.com/docs/align-items) utility classes instead of the SLDS utility classes.

```html
<Card className="p-4 mb-3">
  <div className="flex items-start justify-between gap-4">
    <div className="flex items-start gap-3 flex-1">
      <span className="text-yellow-500 text-xl">🟡</span>
      <div className="flex-1 min-w-0">
        <h4 className="font-semibold text-gray-900 truncate">
          {application.applicantName} - {application.propertyAddress}
        </h4>
        <p className="text-sm text-gray-600 mt-1">Submitted: {application.submittedDate}</p>
      </div>
    </div>
  </div>
</Card>
```
