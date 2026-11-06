# Styling, third-party libraries, Agentforce Conversation Client

Sources: `mfw-styling`, `mfw-third-party-libraries`, `reactdev-acc`, plus the ACC part of `mfw-setup`.

## Styling

React apps can't use Lightning base components or `lightning/*`, so they don't get SLDS styling for free. There are three options; the recipes repo (`trailheadapps/multiframework-recipes`) demos all three.

### 1. SLDS blueprints (you own the markup; no automatic SLDS updates)

```tsx
<section>
  <div className="flex flex-wrap gap-2">
    <button className="slds-button slds-button_neutral">Neutral</button>
    <button className="slds-button slds-button_brand">Brand</button>
  </div>
</section>
```

### 2. SLDS for React (`@salesforce/design-system-react`)

```tsx
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

Icons: wrap in `IconSettings` with the sprite base path.

```tsx
import { Icon, IconSettings } from "@salesforce/design-system-react";
export default function MyReactIcon() {
  return (
    <IconSettings iconPath="/assets/icons">
      <Icon assistiveText={{ label: name }} category="utility" name="edit" size="small" />
    </IconSettings>
  );
}
```

### 3. shadcn + Tailwind (styling is global; component source is copied into your project)

```tsx
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
```

`global.css` is the design-system entry point. Change the token values to rebrand without touching components:

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

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
}
```

`@layer base` holds app-wide defaults (min-h-screen, antialiasing, borders, focus outlines, base bg/text). `@theme inline` maps tokens to utilities (`bg-background`, `text-foreground`, `border-border`).

### LWC → shadcn conversion

Converting goes from template/slot-driven to composition-driven: `lightning-card` (title, `slot="actions"`, `slot="footer"`) becomes `Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, `CardFooter`.

```tsx
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Building2 } from "lucide-react"; // ≈ standard:account

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
        <Button variant="outline" size="sm">Edit</Button> {/* replaces slot="actions" */}
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

To make shadcn look like Lightning:
- **Radius**: SLDS 1 uses 4px/0.25rem; SLDS 2 uses 15rem (pill); shadcn's default is 0.5rem.
- **Focus ring**: brand blue around `#0176d3`.
- **Secondary**: SLDS light gray `#f3f3f3`; shadcn's `secondary` is darker.
- Layout: use Tailwind utilities (flex/grid) instead of SLDS utility classes.

## Third-party JavaScript libraries (CSP)

The app runs under a CSP that **blocks scripts from external domains** (e.g. an analytics `<script src="https://...">` snippet). Serve the library **and everything it loads** from Salesforce so it counts as first-party. If a loader pulls more files at runtime (e.g. jQuery), serve those from Salesforce too and point the loader at them.

Adding the domain to **Trusted URLs** in Setup or to Experience Builder CSP settings **does not** allow the script in a UIBundle.

| Option | App types | Updating it |
|---|---|---|
| Bundle with the app (npm / copy into the project so the build includes it) | Internal **and** external | Rebuild + redeploy the UIBundle |
| Static resource | **External only** | Update without redeploying the bundle |

**Internal apps must bundle.** For external apps, upload each file as a static resource (Setup or `StaticResource` metadata) and load it from the site URL:

```text
SITE_DOMAIN/SITE_PATH_PREFIX/sfsites/c/resource/RESOURCE_NAME
```

```html
<script src="https://MyDomainName.my.site.com/shop/sfsites/c/resource/gtagloader"></script>
```

## Agentforce Conversation Client (ACC) in React (internal apps)

For an **external** React app with a **Service Agent**, use Enhanced Chat v2 instead. For a standalone app hosted outside Salesforce, see the ACC Developer Guide. To open/close the native side panel from an LWC, use the ACC API (`lightning/accApi`). The separate `agentforce-conversation-client` skill covers those cases in depth.

ACC is built on Lightning Out 2.0 as an LWC Interface (LWCI). It provides token streaming with progress status, a floating action button (FAB) entry point with a welcome message, Lightning Types rendering (input/output/list/picklist, standard and custom), dynamic UI from planner responses, brand styling hooks and SDK style tokens, and **inline mode** (renders inside a parent container).

### Org setup

1. At least one **Agentforce Employee Agent** with topics and actions; Setup → **Agentforce Agents** → enable the **Agentforce** preference.
2. Setup → **My Domain** → Routing and Policies: **deselect "Require first-party use of Salesforce cookies"** (needed for session persistence).
3. Setup → **Session Settings** → **Trusted Domains for Inline Frames** → **Add Domain**: your app's origin, e.g. `http://localhost:5173` for dev. iFrame type **Lightning Out**.

### Manual integration (`@salesforce/agentforce-conversation-client`)

The prose in the docs says `createAccWidget`; the code (and the ACC SDK) uses `embedAgentforceClient`.

```tsx
import { useEffect, useRef } from "react";
import { embedAgentforceClient } from "@salesforce/agentforce-conversation-client";

export function AgentforceConversation() {
  const containerRef = useRef<HTMLDivElement>(null); // docs sample is mangled as `useRef < HTMLDivElement > null`

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    embedAgentforceClient({
      container,
      frontdoorUrl: "https://...", // only when embedding outside Salesforce / no org session
      agentforceClientConfig: {
        agentId: "YOUR_AGENT_ID",            // required
        agentLabel: "Support",               // optional
        renderingConfig: { mode: "floating" }, // or "inline" + width/height
      },
    });

    return () => {
      container.replaceChildren();
    };
  }, []);

  // For mode "inline", give the wrapper a real height (flex parent or fixed height)
  return <div ref={containerRef} style={{ width: "100%", height: "100%" }} />;
}
```

Agentforce Vibes can also add ACC from a prompt (it updates `index.tsx` and installs the npm dependency) and restyle it through the SDK's style tokens.
