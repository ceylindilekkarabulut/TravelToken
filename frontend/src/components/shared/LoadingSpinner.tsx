export function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center p-12">
      <div className="w-8 h-8 border-2 border-brand-light border-t-transparent rounded-full animate-spin" />
    </div>
  );
}
