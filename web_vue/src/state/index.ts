import { useStorage } from "@vueuse/core"
import { Session } from "@/types"

export const session = useStorage("session", {} as Session, sessionStorage)
