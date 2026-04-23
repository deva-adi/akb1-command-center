import { Card, CardHeader } from "@/components/ui/Card";

/**
 * Intentional placeholder for a Tab 12 section whose backend data
 * pipeline is not connected. Renders a dimmed card with the correct
 * section title and a short muted message so the page does not feel
 * broken or empty.
 *
 * Used by the three sections that were scoped out of the build: KPI
 * Board, Commercial Levers, and the LLM Narrative block.
 */

export type UnavailableSectionProps = {
  title: string;
};

export function UnavailableSection({ title }: UnavailableSectionProps) {
  return (
    <Card
      className="opacity-75"
      data-testid={`unavailable-section-${title
        .toLowerCase()
        .replace(/\W+/g, "-")
        .replace(/^-+|-+$/g, "")}`}
    >
      <CardHeader title={title} />
      <p className="text-sm text-navy/60 dark:text-navy-100/60">
        Data pipeline for this section is not yet connected.
      </p>
    </Card>
  );
}
