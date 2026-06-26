import { ref } from "vue";
import type { AlertProps, ToastProps } from "@nuxt/ui";
import { Icons, Titles, ToastComposable } from "@/types";

export function useToasts(toast: ToastComposable) {
  function create(
    status: ToastProps["color"] = "error",
    description: string = "Невозможно выполнить действие!",
  ) {
    toast.add({
      title: Titles[status],
      description: description,
      color: status,
      icon: Icons[status],
    });
  }
  return { create };
}

export function useAlert() {
  const alert = ref<AlertProps | null>(null);

  function update(
    status: AlertProps["color"] = "error",
    description: string = "Неизвестная ошибка.",
  ) {
    alert.value = {
      icon: Icons[status],
      color: status,
      title: Titles[status],
      description: description,
    };
  }
  return { alert, update };
}
