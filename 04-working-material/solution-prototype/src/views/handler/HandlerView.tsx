import type { ReactNode } from "react";
import { Badge, Card, Flex, Grid, Heading, Text } from "@radix-ui/themes";
import { ArchiveIcon, MagicWandIcon, Share2Icon, TableIcon } from "@radix-ui/react-icons";
import { useStore, type HandlerPage } from "../../data/store";
import { INSURERS } from "../../data/insurers";

type NavItem = { page: HandlerPage; label: string; phase: string; icon: ReactNode };

const NAV: NavItem[] = [
  { page: "inbox", label: "Inbox", phase: "Current", icon: <ArchiveIcon /> },
  { page: "bulk", label: "Bulk sorting", phase: "Phase 1", icon: <TableIcon /> },
  { page: "workflow", label: "Workflow builder", phase: "Phase 2", icon: <Share2Icon /> },
  { page: "agent", label: "Hyper-operator agent", phase: "Phase 3", icon: <MagicWandIcon /> },
];

const PAGE_INFO: Record<HandlerPage, { title: string; description: string; step: number }> = {
  inbox: {
    title: "Inbox",
    description: "How sorting works today: every claim arrives here and a handler opens and sorts each one by hand.",
    step: 2,
  },
  bulk: {
    title: "Bulk sorting",
    description: "A table of every claim with filters and multi-select. Every filter and bulk action is captured to inform automation rules.",
    step: 3,
  },
  workflow: {
    title: "Workflow builder",
    description: "Rules learned from handler behaviour, arranged into a drag-and-drop workflow per insurer.",
    step: 5,
  },
  agent: {
    title: "Hyper-operator agent",
    description: "An AI layer over all claim and workflow data: answers questions about any claim and proposes workflow improvements for a human to approve.",
    step: 6,
  },
};

export function HandlerView() {
  const { page, setPage, claims, insurer } = useStore();
  const info = PAGE_INFO[page];
  const mine = claims.filter((c) => c.insurer === insurer);
  const waiting = mine.filter((c) => c.missingInfo.length > 0).length;
  const unsorted = mine.filter((c) => !c.pile).length;

  return (
    <div className="handler">
      <nav className="sidebar" aria-label="Sorting product">
        {NAV.map((item) => (
          <div key={item.page}>
            <div className="nav-group-label">{item.phase}</div>
            <button className="nav-item" data-active={page === item.page} onClick={() => setPage(item.page)}>
              <span aria-hidden style={{ display: "flex" }}>{item.icon}</span>
              {item.label}
            </button>
          </div>
        ))}
      </nav>

      <main className="main">
        <div className="page">
          <Flex direction="column" gap="1" mb="5">
            <Text size="2" color="gray">
              {INSURERS[insurer].name} · {INSURERS[insurer].segment}
            </Text>
            <Heading size="7">{info.title}</Heading>
            <Text color="gray" style={{ maxWidth: 720 }}>
              {info.description}
            </Text>
          </Flex>

          <Grid columns="3" gap="4" mb="5" style={{ maxWidth: 720 }}>
            <Stat label="Claims" value={mine.length} />
            <Stat label="Not sorted yet" value={unsorted} />
            <Stat label="Missing information" value={waiting} />
          </Grid>

          <Card size="3" style={{ maxWidth: 720 }}>
            <Flex gap="2" align="center">
              <Badge>Step {info.step}</Badge>
              <Text size="2" color="gray">
                This screen is built in step {info.step} of the plan.
              </Text>
            </Flex>
          </Card>
        </div>
      </main>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <Card>
      <Text as="div" size="2" color="gray">
        {label}
      </Text>
      <Text as="div" size="7" weight="bold">
        {value}
      </Text>
    </Card>
  );
}
