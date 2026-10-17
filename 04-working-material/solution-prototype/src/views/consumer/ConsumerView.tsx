import { Box, Button, Card, Container, Flex, Heading, Text } from "@radix-ui/themes";

export function ConsumerView() {
  return (
    <div className="consumer">
      <div className="insurer-brand-bar">
        <span aria-hidden>⚓</span> Harbour Mutual
        <Text size="2" weight="regular" style={{ opacity: 0.75, marginLeft: 8 }}>
          Car insurance
        </Text>
      </div>
      <Container size="2" px="5" py="8">
        <Card size="4">
          <Flex direction="column" gap="3">
            <Heading size="7">Make a car insurance claim</Heading>
            <Text color="gray">
              Tell us what happened. It takes about 5 minutes, and you can add photos and documents as you go.
            </Text>
            <Box>
              <Button size="3" disabled>
                Start your claim
              </Button>
            </Box>
            <Text size="1" color="gray">
              Step 1 builds the claim form and the live data schema panel.
            </Text>
          </Flex>
        </Card>
      </Container>
    </div>
  );
}
