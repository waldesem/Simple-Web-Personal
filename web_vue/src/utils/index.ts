import { useStorage } from "@vueuse/core";

export const flag = useStorage("flag", false); // returns Ref<boolean>

export function localStr(data: string): string {
  return data ? new Date(data).toLocaleDateString() : "";
}

export function capitalize(str: string) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}
