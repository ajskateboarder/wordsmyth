// Custom function to emit toast notifications
export function notify({
  message = "",
  variant = "primary",
  icon = "info-circle",
  duration = 3000,
  closable = false,
}) {
  const alert = Object.assign(document.createElement("sl-alert"), {
    variant,
    closable: closable,
    duration: duration,
    innerHTML: `
          <sl-icon name="${icon}" slot="icon"></sl-icon>
          ${message}
        `,
  });

  document.body.append(alert);
  return (alert as any).toast();
}
