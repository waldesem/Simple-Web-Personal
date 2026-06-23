import { useStorage } from "@vueuse/core";
import { Session } from "@/types";

export const session = useStorage("session", {} as Session, sessionStorage);

export const access = useStorage("access", "" as string, sessionStorage);

export const refresh = useStorage("refresh", "" as string, localStorage);
