# Provide Global Copy to Action Responses

The global copy feature provides a consistent way for users to copy information from UI components in Agentforce responses, enhancing usability and saving time. Previously, the ability to copy information was limited, often forcing users to manually retype details from record lists or complex messages.

To enable this feature in a custom Lightning Web Component (LWC) built using [Lightning Types](/docs/ai/agentforce/guide/lightning-types.md), a developer must implement a public `getFormattedValue()` method. When a user clicks the copy button, the system calls this method to get the content for the clipboard. This gives the developer full control over what gets copied and how it's formatted. The method must be decorated with `@api` and return a string, which can be either plain text or [rich text](https://help.salesforce.com/s/articleView?id=platform.fields_using_html_editor.htm).

**Lightning Web Component with Global Copy:**

![Global copy example](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/global-copy-example.png)

**Formatted Copy Value:**

![Global copy result](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/global-copy-result.png)

## Prerequisites

You must have a functional [Lightning Web Component (LWC)](https://developer.salesforce.com/docs/platform/lwc/overview) that is accessible to Agentforce using [Lightning Types](/docs/ai/agentforce/guide/lightning-types.md).

## Example

Here's an example of how to implement this copy functionality for complex data, such as a Salesforce record. It goes beyond a simple text summary and instead generates a rich HTML table using the `getFormattedValue()` method.

```javascript
/**
 * Returns a formatted HTML string representing the record data in a table format
 * @returns {string} Formatted HTML string
 */

@api
getFormattedValue = () {
  // Return table markup
  let table =
      '<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">';
  // Build header row using field labels.
  table += '<thead><tr>';
  this.fields.forEach((field) => {
      table += `<th style="background-color: #f2f2f2; text-align: left;">${field.label}</th>`;
  });
  table += '</tr></thead>';
  // Build table body.
  table += '<tbody>';
  this.records.forEach((record) => {
      table += '<tr>';
      this.fields.forEach((field) => {
          let cellValue = record.fields[field.apiName].value;
          table += `<td>${cellValue}</td>`;
      });
      table += '</tr>';
  });
  table += '</tbody></table>';
  return `${table}`;
}
```

## Implementation Guide

Here's a step-by-step breakdown of how that `getFormattedValue` method is implemented in the example.

### Step 1: Initialize the HTML Table

The process begins by creating a table string variable. This variable is initialized with the opening `<table>` tag, which includes inline CSS styles to define its border and collapse the cell spacing for a clean look.

```javscript
let table =
    '<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">';
```

### Step 2: Build the Table Header

Next, the code constructs the header row of the table. It loops through an array stored in `this.fields`. For each field object in the array, it creates a header cell (`<th>`) using the field.label property and adds some light gray background color for styling. All the header cells are wrapped in `<thead>` and `<tr>` tags.

```javascript
table += "<thead><tr>";
this.fields.forEach((field) => {
  table += `<th style="background-color: #f2f2f2; text-align: left;">${field.label}</th>`;
});
table += "</tr></thead>";
```

### Step 3: Build the Table Body

After the header is complete, the code starts building the body of the table. It iterates through an array stored in `this.records`. For each record object, it adds a new table row (`<tr>`) to contain that record's data.

```javascript
table += "<tbody>";
this.records.forEach((record) => {
  table += "<tr>";
  // ... cells are added here ...
  table += "</tr>";
});
table += "</tbody>";
```

### Step 4: Populate Data Cells

Inside the records loop, the code iterates through the `this.fields` array again for each record. This nested loop ensures that the data in each row aligns with the correct header column. It extracts the cell's value using the field.apiName to look up the data within the record object (`record.fields[field.apiName].value`) and places it inside a standard data cell (`<td>`).

```javascript
this.fields.forEach((field) => {
  let cellValue = record.fields[field.apiName].value;
  table += `<td>${cellValue}</td>`;
});
```

### Step 5: Finalize and Return the HTML

Once all the loops are finished, the code appends the closing `</table>` tag to complete the HTML structure. The complete HTML table string is then returned by the function.

```javascript
return `${table}`;
```

When a user clicks "copy" on this component, this method runs and provides the copy framework with a clean, well-structured HTML table of the record's details, ready to be pasted into an email, document, or another system.

## See Also

- [Custom Lightning Types Developer Guide](/docs/ai/agentforce/guide/lightning-types.md)
- [Lightning Web Component Developer Guide](https://developer.salesforce.com/docs/platform/lwc/overview)
- [Rich Text Editor](https://help.salesforce.com/s/articleView?id=platform.fields_using_html_editor.htm) in Salesforce Help
