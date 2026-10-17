import { Badge, Flex, SegmentedControl, Select, Text } from "@radix-ui/themes";
import { useStore, type View } from "./data/store";
import { INSURER_LIST } from "./data/insurers";
import type { InsurerId } from "./data/schema";
import { ConsumerView } from "./views/consumer/ConsumerView";
import { HandlerView } from "./views/handler/HandlerView";

export function App() {
  const { view, setView, insurer, setInsurer } = useStore();

  return (
    <div className="app">
      <header className="topbar">
        <Flex align="center" gap="3">
          <span className="wordmark">
            <span className="wordmark-dot" />
            keelwater
          </span>
          <Badge color="gray" variant="solid" highContrast={false} radius="full">
            Prototype
          </Badge>
        </Flex>

        <SegmentedControl.Root value={view} onValueChange={(v) => setView(v as View)} size="2" radius="full">
          <SegmentedControl.Item value="consumer">Claimant view</SegmentedControl.Item>
          <SegmentedControl.Item value="handler">Handler view</SegmentedControl.Item>
        </SegmentedControl.Root>

        <Flex justify="end" align="center" gap="3">
          {view === "handler" && (
            <>
              <Text size="2" style={{ color: "rgba(255,255,255,0.7)" }}>
                Insurer
              </Text>
              <Select.Root value={insurer} onValueChange={(v) => setInsurer(v as InsurerId)} size="2">
                <Select.Trigger variant="surface" />
                <Select.Content>
                  {INSURER_LIST.map((i) => (
                    <Select.Item key={i.id} value={i.id}>
                      {i.name} ({i.market})
                    </Select.Item>
                  ))}
                </Select.Content>
              </Select.Root>
            </>
          )}
        </Flex>
      </header>

      {view === "consumer" ? <ConsumerView /> : <HandlerView />}
    </div>
  );
}
