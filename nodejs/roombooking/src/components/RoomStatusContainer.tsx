// src/components/RoomStatusContainer.tsx
export default function RoomStatusContainer({
  status,
  children,
}: {
  status: "free" | "soon" | "busy";
  children: React.ReactNode;
}) {
  const borderColor =
    status === "free" ? "border-lime-500" :
    status === "soon" ? "border-yellow-400" :
    "border-red-600";

  return (
    <div className={`h-screen w-screen border-[64] ${borderColor} overflow-hidden box-border`}>
      {children}
    </div>
  );
}
