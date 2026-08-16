import CommonCard from "#/components/common/CommonCard";
import { createFileRoute } from "@tanstack/react-router";
export const Route = createFileRoute("/")({ component: App });

function App() {
  return (
    <div>
      <CommonCard />
      <CommonCard />
      <CommonCard />
      <CommonCard />
      <CommonCard />
      <CommonCard />
      <CommonCard />
      <CommonCard />
    </div>
  );
}