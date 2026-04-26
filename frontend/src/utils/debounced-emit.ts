export function debouncedEmit<T>(emitFn: (value: T) => void, delay = 600): (value: T) => void {
  let timer: ReturnType<typeof setTimeout> | null = null;
  return (value: T) => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => emitFn(value), delay);
  };
}
