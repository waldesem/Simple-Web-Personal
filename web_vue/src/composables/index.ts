import { useStorage } from "@vueuse/core";

export const useEdit = () => useStorage<boolean>("edit", () => false);
